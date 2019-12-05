# -*- coding: utf-8 -*-

from websocket import create_connection
import gzip
import zlib
import time

def inflate(data):
    decompress = zlib.decompressobj(
            -zlib.MAX_WBITS  # see above
    )
    inflated = decompress.decompress(data)
    inflated += decompress.flush()
    return inflated

if __name__ == '__main__':
    while(1):
        try:
            ws = create_connection("wss://real.okex.com:8443/ws/v3")
            break
        except:
            print('connect ws error,retry...')
            time.sleep(5)

    # 订阅 KLine 数据
    
    tradeStr_kline="""
    {"sub": "market.BTC_CQ.kline.1min",  "id": "id1"}
    """

    # 订阅 Market Detail 数据
    tradeStr_marketDetail="""
    {"sub": "market.BTC_CQ.detail",  "id": "id6" }
    """

    # 订阅 Trade Detail 数据
    tradeStr_tradeDetail="""
    {"sub": "market.BTC_CQ.trade.detail", "id": "id7"}
    """

    # 请求 KLine 数据
    tradeStr_klinereq="""
    {"req": "market.BTC_CQ.kline.1min", "id": "id4"}
    """

    # 请求 Trade Detail 数据
    tradeStr_tradeDetail_req="""
    {"req": "market.BTC_CQ.trade.detail", "id": "id5"}
    """

    # 订阅 Market Depth 数据
    tradeStr_marketDepth="""
    {
        "sub": "market.BTC_CQ.depth.step0", "id": "id9"
    }
    """
    
    tradeStr_marketTicker="""
    {
         "op": "subscribe", "args": ["swap/ticker:BTC-USD-SWAP"]
    }
    """

    ws.send(tradeStr_marketTicker)
if(1):
    trade_id = ''
    while(1):
        compressData=ws.recv()
        result=inflate(compressData)
        if result[:7] == '{"ping"':
            ts=result[8:21]
            pong='{"pong":'+ts+'}'
            ws.send(pong)
            ws.send(tradeStr_marketTicker)
        else:
            try:
                if trade_id == result['data']['id']:
                    print('重复的id')
                    break
                else:
                    trade_id = result['data']['id']
            except Exception:
                pass
            print(result)

    
