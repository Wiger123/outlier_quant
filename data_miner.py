from selenium import webdriver
from selenium.webdriver import ActionChains
import time
from page_path import *
import pandas as pd

# 启动浏览器,并防止打印一些无用的日志,窗口最大化
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(chrome_options=option)
driver.maximize_window()

# 打开链接
link = huobi_link + symbol_link
driver.get(link)

# 等待
time.sleep(5)

# 选择 1min
time_location = driver.find_element_by_xpath(minute_button)
ActionChains(driver).move_to_element_with_offset(time_location, 15, 10).perform()

# 等待
time.sleep(0.2)

# 点击 1min
ActionChains(driver).click().perform()

# 等待
time.sleep(0.2)

# 数据计数器
count = 0

# 记录数据
data_list = []

# 快速拉动选择时间
for i in range(time_drag):
    # 拖动屏幕,防止数据抖动
    canvas_location = driver.find_element_by_xpath(minute_canvas)
    ActionChains(driver).move_to_element_with_offset(canvas_location, drag_start_x, drag_start_y).perform()

    # 按住 Canvas, 按一下拖不动，按两下才行
    ActionChains(driver).click_and_hold().perform()
    ActionChains(driver).click_and_hold().perform()

    # 根据轨迹执行滑动动作
    for i in range(drag_times):
        # 新建 ActionChains 对象防止累加位移
        action = ActionChains(driver)
        action.move_by_offset(xoffset = drag_offset, yoffset = 0).perform()
        time.sleep(0.1)

    #释放滑块
    ActionChains(driver).release().perform()
    time.sleep(0.1)

# 循环采集数据
while True:
    # 拖动屏幕,防止数据抖动
    canvas_location = driver.find_element_by_xpath(minute_canvas)
    ActionChains(driver).move_to_element_with_offset(canvas_location, drag_start_x, drag_start_y).perform()

    # 按住 Canvas, 按一下拖不动，按两下才行
    ActionChains(driver).click_and_hold().perform()
    ActionChains(driver).click_and_hold().perform()

    # 根据轨迹执行滑动动作
    for i in range(drag_times):
        # 新建 ActionChains 对象防止累加位移
        action = ActionChains(driver)
        action.move_by_offset(xoffset = drag_offset, yoffset = 0).perform()
        time.sleep(0.2)

    #释放滑块
    ActionChains(driver).release().perform()

    # 等待
    time.sleep(0.1)

    # 移动到右侧第二时间列
    action = ActionChains(driver)
    action.move_to_element_with_offset(canvas_location, 824, 215).perform()
    time.sleep(0.2)

    # 循环采集数据
    for i in range(once_len):
        # 新建 ActionChains 对象防止累加位移
        action = ActionChains(driver)
        action.move_by_offset(xoffset = data_offset, yoffset = 0).perform()

        # 采集数据
        time_data = driver.find_element_by_xpath(minute_data).text
        time_data = time_data.split(' ')
        data_list.append(time_data)
        time.sleep(0.1)

        # 数据数目增加
        count += 1

        # 判断采集数据是否达到 1000, 每 1000 条数据存储一次
        if count % 1000 == 0:
            # 存储 csv
            df_data = pd.DataFrame(data_list)
            df_data.to_csv(symbol_link + '.csv', mode = 'a+', header = False, encoding = 'utf_8_sig')

            # 数据清空
            data_list = []

            # 打印进度
            print('已采集 {0} 条数据'.format(count))
            time.sleep(5)