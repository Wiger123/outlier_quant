from huobi.client.market import *
from huobi.exception.huobi_api_exception import HuobiApiException
import time

market_client = MarketClient()

start_time = 1621261620

finish_time = 1621310400

def callback_func(candlestick_event: 'CandlestickEvent'):
    candlestick_event.print_object()
    print("\n")

def error_func(e: 'HuobiApiException'):
    print(e.error_code + e.error_message)

from_time = start_time

# 300 per request
while from_time <= finish_time:
    end_time = from_time + 18000 - 60
    market_client.req_candlestick(symbols='dogeusdt', interval=CandlestickInterval.MIN1, from_ts_second=from_time, end_ts_second=end_time, callback=callback_func, error_handler=error_func)
    
    from_time += 18000
    time.sleep(2)

# 补充缺失数据
# from_time = 1619997360
# end_time = 1619997360
# market_client.req_candlestick(symbols='dogeusdt', interval=CandlestickInterval.MIN1, from_ts_second=from_time, end_ts_second=end_time, callback=callback_func, error_handler=error_func)
    
