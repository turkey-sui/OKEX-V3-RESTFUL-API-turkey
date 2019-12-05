# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 02:26:24 2019

@author: pc
"""

import threading

#import ccxt
import time
import numpy as np
import pandas as pd
import CONSTANT
from matplotlib import pyplot as plt
import datetime
import requests
import hashlib
import json
from . import CONSTANT as c
from CONSTANT import *
import utils

c = CONSTANT

class Exchange:
    
    def __init__(self,api_key=None,secret=None,use_server_time=False):
#        
#        self.exchange = ccxt.okex()
#        self.exchange_swap = ccxt.okex3()
        self.API_KEY = CONSTANT.V3_API_KEY
        self.API_SECRET_KEY = CONSTANT.V3_SECRET
        self.PASSPHRASE = CONSTANT.V3_PASSPHRASE
        
        self.okex_url = 'https://www.okex.me'
#        
#        self.exchange.API_SECRET_KEY = CONSTANT.API_KEY
#        self.exchange.secret = CONSTANT.SECRET
#        self.exchange_swap.API_SECRET_KEY = CONSTANT.V3_API_KEY
#        self.exchange_swap.secret = CONSTANT.V3_SECRET
        
        self.OHLCVs = dict()
        self.instruments = pd.DataFrame(columns=['instrument_id','api_type','futures_type'])
        self.use_server_time = use_server_time
        
        #markets_info = self.exchange.load_markets()
        #swap_info = self.exchange_swap.load_markets()
        
#        self.future_symbol = list(markets_info.keys())[-27:]
#        self.swap_symbol = list(swap_info.keys())[-9:]
#        self.spot_symbol = []
#        for i in ['BTC','ETH','LTC','EOS','XRP','BCH','BSV','TRX','ETC']:
#            self.spot_symbol.append(i + '/USDT')
        
    def _request(self, method, request_path, params, cursor=False):

        if method == c.GET:
            request_path = request_path + utils.parse_params_to_str(params)
        # url
        url = c.API_URL + request_path

        timestamp = utils.get_timestamp()
        # sign & header
        if self.use_server_time:
            timestamp = self._get_timestamp()
        body = json.dumps(params) if method == c.POST else ""

        sign = utils.sign(utils.pre_hash(timestamp, method, request_path, str(body)), self.API_SECRET_KEY)
        header = utils.get_header(self.API_KEY, sign, timestamp, self.PASSPHRASE)

        # send request
        response = None
        #print("url:", url)
        #print("headers:", header)
        #print("body:", body)
        if method == c.GET:
            response = requests.get(url, headers=header)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header)
            #response = requests.post(url, json=body, headers=header)
        elif method == c.DELETE:
            response = requests.delete(url, headers=header)

        # exception handle
#        if not str(response.status_code).startswith('2'):
#            raise exceptions.OkexAPIException(response)
        try:
            res_header = response.headers
            if cursor:
                r = dict()
                try:
                    r['before'] = res_header['OK-BEFORE']
                    r['after'] = res_header['OK-AFTER']
                except:
                    print("")
                return response.json() , r
            else:
                return response.json()
        except ValueError:
            raise Exception('Invalid Response: %s' % response.text)

    def _request_without_params(self, method, request_path):
        return self._request(method, request_path, {})

    def _request_with_params(self, method, request_path, params, cursor=False):
        return self._request(method, request_path, params, cursor)    
    
    
    
    def _addParams(self,url,param_name,param):
        new_url = url
        
        if ( url.count('?')==0 ):
            new_url = new_url + '?'
        
        if(new_url[-1] == '?'):
            new_url = new_url + param_name + '=' + param
        
        else:
            new_url = new_url + '&' + param_name + '=' + param
        
        return new_url
    
    def get_timestamp(self):
        base_url = '/api/general/v3/time'
        return json.loads(requests.get(self.okex_url + base_url).content)
    
    def buildMySign(params):
        
        secretKey=self.secret
        
        sign = ''
        
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) +'&'
            
        data = sign+'secret_key='+secretKey
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()
            
        
    def load_markets(self,Type='all'):
        
        if(Type == 'all'):
            for market_type in ['spot','futures','swap']:    
                self.load_markets(Type = market_type)
        
        if(Type in ['futures','swap']):
            
            json_text = pd.DataFrame(json.loads(requests.get(self.okex_url + '/api/%s/v3/instruments' % (Type)).content)).instrument_id
            json_list = list(json_text)
            count = 0
            for i in json_list:
                init_contract_states = ['TW','NW','TQ']
                self.instruments.loc[ len (self.instruments) ] = (i,Type,i[:-6] + init_contract_states[count%3] if Type=='futures' else None)
                count += 1
            
        if(Type in ['spot']):
            json_text = pd.DataFrame(json.loads(requests.get(self.okex_url +  '/api/swap/v3/instruments').content)).instrument_id
            json_list = list(json_text)
            for i in json_list:
                corrective_i = i[:-5] + 'T' 
                self.instruments.loc[ len (self.instruments) ] = (corrective_i,Type,None)
                
        self.instruments.set_index(keys='instrument_id')
        
        return True
            
#    def get_OHLCV(self,symbol):
#    
#        # markets trade pair information/
#        #print('loading trade pairs')
#        url_base = '/api/%s/v3/instruments/%s/candles'
#        
#        instruments_index_by_instruments_id = self.instruments
#        instruments_index_by_instruments_id.index = self.instruments['instrument_id']
#        
#        market_type = instruments_index_by_instruments_id.loc[symbol]['api_type']
#        
#        result = json.loads(requests.get(self.okex_url + url_base % (market_type,symbol)).content)
#        
#        return result
    
    def get_kline(self,Type, instrument_id, granularity='60', start='', end=''):
        
        params = {}
        
        if granularity:
            params['granularity'] = granularity
        if start:
            params['start'] = start
        if end:
            params['end'] = end
            
        if(Type in ['spot','lever','futures','swap']):
            KLINE_APIS ={
                    'spot':SPOT_KLINE,
                    'lever':SPOT_KLINE,
                    'futures':FUTURE_KLINE,
                    'swap':SWAP_INSTRUMENTS,
                    }
        else:
            error_logging('Type error')
            return
        return self._request_with_params(GET, KLINE_APIS[Type]+'/'+str(instrument_id)+'/candles', params)

#    def get_depth(self,symbol,size='50'):
#        
#        instruments_index_by_instruments_id = self.instruments
#        instruments_index_by_instruments_id.index = self.instruments['instrument_id']
#        
#        market_type = instruments_index_by_instruments_id.loc[symbol]['api_type']
#        
#        url_base = '/api/%s/v3/instruments/%s/book' if market_type in ['spot','futures'] else '/api/%s/v3/instruments/%s/depth'
#        
#        url_request = self.okex_url + url_base % (market_type,symbol)
#        
#        if(size):
#            url_request = self._addParams(url_request,'size',str(size))
#        
#        result = json.loads(requests.get(url_request).content)
#        print(url_request)
#        return result
#    '''
#    正常情况下不使用market下单，只使用可预料冲击成本的limit下单
#    '''
#    
    
    
    
#    ——————————————————————————————————————————————————————————
    def create_future_order(self,instrument_id,otype,price,size, client_oid='',order_type='0', match_price='0'):
        #'client_oid': client_oid,
        params = { 'instrument_id': instrument_id, 
                  'type': otype, 
                  'price': price, 
                  'size': size, 
                  'client_oid' : client_oid,
                  'order_type' : order_type,
                  'match_price': match_price,
                  }
        
        return self._request_with_params(POST, FUTURE_ORDER, params)
    
    def create_spot_order(self, otype, side, instrument_id, size, margin_trading=1, client_oid='', price='', funds='',order_type = ''):
        params = {'type': otype, 'side': side, 'instrument_id': instrument_id, 'size': size, 'client_oid': client_oid,
                  'price': price, 'funds': funds, 'margin_trading': margin_trading,'order_type':order_type}
        print(params)
        return self._request_with_params(POST, SPOT_ORDER, params)
    
    def create_lever_order(self, instrument_id, side, margin_trading, price, size, client_oid='', otype='limit', order_type='0', notional=''):
        params = {'instrument_id': instrument_id,
                  'type': otype, 
                  'side': side,
                  'client_oid': client_oid,
                  'order_type':order_type}
        if otype == 'limit':
            params['price'] = price
            params['size'] = size
        elif otype == 'market':
            if size:
                params['size'] = size
            if notional:
                params['notional'] = notional

        if margin_trading:
            params['margin_trading'] = margin_trading

        return self._request_with_params(POST, LEVER_ORDER, params)
    
    def create_swap_order(self, instrument_id,size,otype,price,client_oid='',order_type='0',match_price=''):    #'client_oid': client_oid,
        params = { 'instrument_id': instrument_id, 
                  'type': otype, 
                  'price': price, 
                  'size': size, 
                  'match_price':match_price, 
                  'client_oid':client_oid,
                  'order_type': order_type,
                  }
        return self._request_with_params(POST, SWAP_ORDER, params)
# ——————————————————————————————————————————————————————————————————————
        
    def get_depth(self,Type, instrument_id, size='', depth=''):
        
        params = {}
        if(size):
            params['size'] = size
        if(Type in ['spot','futures','swap']):
            ACCOUNTS_APIS ={
                    'spot':SPOT_DEPTH + str(instrument_id) + '/book',
                   # 'lever':LEVER_ACCOUNT,
                    'futures':FUTURE_DEPTH + str(instrument_id) + '/book',
                    'swap':SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth',
                    }
        else:
            error_logging('Type error')
            return
        
        return self._request_with_params(GET, ACCOUNTS_APIS[Type] ,params)
#    
#    def get_future_depth(self, instrument_id, size):
#        params = {'size': size}
#        return self._request_with_params(GET, FUTURE_DEPTH + str(instrument_id) + '/book', params)
#        
#    def get_swap_depth(self, instrument_id, size):
#        if size:
#            params={'size': size}
#            return self._request_with_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth', params)
#        return self._request_without_params(GET, SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth')

#————————————————————————————————————————————————————————————————————————
    
    def get_accounts(self,Type):
        if(Type in ['spot','lever','futures','swap']):
            ACCOUNTS_APIS ={
                    'spot':SPOT_ACCOUNT_INFO,
                    'lever':LEVER_ACCOUNT,
                    'futures':FUTURE_ACCOUNTS,
                    'swap':SWAP_ACCOUNTS,
                    }
        else:
            error_logging('Type error')
            return
        
        return self._request_without_params(GET, ACCOUNTS_APIS[Type])
    
    def get_position(self,Type):
        if(Type in ['futures','swap']):
            POSITION_APIS ={
                    'spot':'',
                    'lever':'',
                    'futures':FUTURE_POSITION,
                    'swap':SWAP_POSITIONS,
                    }
        else:
            error_logging('Type error')
            return
        
        return self._request_without_params(GET, POSITION_APIS[Type])
    

    def get_order_info(self,Type, instrument_id, order_id='',client_oid = ''):
        if order_id:
            url_suffix = str(instrument_id) + '/' + str(order_id)
            #return self._request_without_params(GET, SWAP_ORDERS+'/'+str(instrument_id)+'/'+str(order_id))
        elif client_oid:
            url_suffix =  str(instrument_id) + '/' + str(client_oid)
            #return self._request_without_params(GET, SWAP_ORDERS + '/' + str(instrument_id) + '/' + str(client_oid))
            
        else:
            error_logging('The attributes order_id and client_oid cannot all be empty')
        if(Type in ['spot','lever','futures','swap']):
            ORDER_APIS ={
                    'spot':SPOT_ORDER_INFO,
                    'lever':LEVER_ORDER_INFO,
                    'futures':FUTURE_ORDER_INFO,
                    'swap':SWAP_ORDERS + '/',
                    }
        else:
            error_logging('Type error')
            return
        
        print(ORDER_APIS[Type] + url_suffix)
        
        return self._request_without_params(GET, ORDER_APIS[Type] + url_suffix)
        

    def cancel_order(self,Type, instrument_id, order_id='',client_oid=''):
        
        if order_id:
            url_suffix = str(instrument_id) + '/' + str(order_id)

        elif client_oid:
            url_suffix =  str(instrument_id) + '/' + str(client_oid)
            
        else:
            error_logging('The attributes order_id and client_oid cannot all be empty')
            
        if(Type in ['spot','lever','futures','swap']):
            ORDER_CANCEL_APIS ={
                    'spot':SPOT_REVOKE_ORDER,
                    'lever':LEVER_REVOKE_ORDER,
                    'futures':FUTURE_REVOKE_ORDER,
                    'swap':SWAP_CANCEL_ORDER,
                    }
        else:
            error_logging('Type error')
            return

        return self._request_without_params(POST, ORDER_CANCEL_APIS[Type] + url_suffix)
    
    def get_fills(self, Type, instruments_id ,order_id='', client_oid='', froms='', to='', limit=''):
        
        params = {'instrument_id':str(instruments_id),}
        
        if order_id:
            params['order_id'] = str(order_id)

        elif client_oid:
            params['client_oid'] = str(client_oid)
            
        else:
            pass
        
        if froms:
            params['froms'] = str(froms)
            
        if to:
            params['to'] = str(to)
            
        if limit:
            params['limit'] = str(limit)
            
        if(Type in ['spot','lever','futures','swap']):
            FILLS_APIS ={
                    'spot':SPOT_FILLS,
                    'lever':LEVER_FILLS,
                    'futures':FUTURE_FILLS,
                    'swap':SWAP_FILLS,
                    }
        else:
            error_logging('Type error')
            return 
        
        return self._request_with_params(GET, FILLS_APIS[Type], params)
        
        
#    def get_order_list(self, status, instrument_id, froms='', to='', limit=''):
#        params = {'status': status}
#        if froms:
#            params['from'] = froms
#        if to:
#            params['to'] = to
#        if limit:
#            params['limit'] = limit
#        return self._request_with_params(GET, SWAP_ORDERS+'/'+str(instrument_id), params)


    # query coin account info
    def get_coin_account(self, symbol):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(symbol))

    
    
#    def get_swap_futures_spread(self,symbol='BSV',contract_type='191227'):
#        
#        # init params for depth()
#        swap_params = [symbol + '-USD-SWAP','swap',10]
#        futures_params = [symbol + '-USD-' + contract_type,'futures',10]
#        
#        # receive depth() returns 
#        swap_depth = self.get_depth(*swap_params)
#        futures_depth = self.get_depth(*futures_params)
#        
#        # print returns for depth()
#        print(swap_depth['asks'][0])
#        print(futures_depth['bids'][0])
#        long_price = - swap_depth['asks'][0][0] + futures_depth['bids'][0][0]
#        print('long SWAP: price', long_price)
#        print()        
#        short_price = - swap_depth['bids'][0][0] + futures_depth['asks'][0][0]
#        print(swap_depth['bids'][0])
#        print(futures_depth['asks'][0])
#        print('short SWAP: price', short_price)
        
    def get_usdt_rate(self):
        return self._request_without_params(GET, SWAP_RATE)
        
    def get_historical_funding_rate(self, instrument_id):
        params = {}
#        if froms:
#            params['from'] = froms
#        if to:
#            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/historical_funding_rate', params)

#    def get_account(self,symbol,Type):
#        if(Type in ['swap','spot','futures']):
#            url = 'http://www.okex.me/api/' + Type + '/v3/accounts/'
#        else:
#            raise Exception('the type wrong')
#        result = requests.get(url + symbol)
#        return result.content
        
    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['iso']
        else:
            return ""
        
if __name__ == '__main__':
    e = Exchange(use_server_time=True)
    e.load_markets()
    e.get_depth('swap','BSV-USD-SWAP')