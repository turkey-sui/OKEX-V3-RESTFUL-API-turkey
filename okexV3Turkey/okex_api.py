# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 02:26:24 2019

@author: pc
"""
import time
import numpy as np
import pandas as pd
import datetime
import requests
import hashlib
import json
from . import CONSTANT
from . import CONSTANT as c
from . CONSTANT import *
from . import utils

class Exchange:
    
    def __init__(self,api_key=None,secret=None,use_server_time=False,load_markets=True):
#        
#        self.exchange = ccxt.okex()
#        self.exchange_swap = ccxt.okex3()
        self.API_KEY = CONSTANT.V3_API_KEY
        self.API_SECRET_KEY = CONSTANT.V3_SECRET
        self.PASSPHRASE = CONSTANT.V3_PASSPHRASE
        
        self.okex_url = 'https://www.okex.me'
        
        self.OHLCVs = dict()
        self.instruments = pd.DataFrame(columns=['instrument_id','api_type','futures_type'])
        self.use_server_time = use_server_time
        
        if load_markets:
            self.load_markets()
        
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
            # async with aiohttp.ClientSession() as session:
            response = requests.get(url, headers=header,timeout=1)
        elif method == c.POST:
            response = requests.post(url, data=body, headers=header,timeout=1)
            #response = requests.post(url, json=body, headers=header)
        elif method == c.DELETE:
            response = requests.delete(url, headers=header)
        #print(header)
        header['OK-ACCESS-SIGN'] = header['OK-ACCESS-SIGN'].decode()
        

        # if method == c.GET:
        #     # async with aiohttp.ClientSession() as session:
        #     #     async with session.get(url, headers = header, timeout=2) as r:
        #     #         print(r.status)
        #     #         response_json = await r.json()
        #     #         print(response_json)
        #     #         response = r.json(encoding = 'utf-8')
        #     return {'method':'GET','headers':header,'url':url}
                    
        #     #        return response
                    
        # elif method == c.POST:
        #     # async with aiohttp.ClientSession() as session:
        #     #     async with session.post(url, headers = header, data=body, timeout=2) as r:
        #     #         response = r.text(encoding = 'utf-8')
        #     return {'method':'POST','headers':header,'url':url,'data':body}
                    
        # elif method == c.DELETE:
        #     # async with aiohttp.ClientSession() as session:
        #     #     async with session.delete(url, headers=header, timeout=2) as r:
        #     #         response = r.text(encoding = 'utf-8')
        #     return {'method':'DELETE','headers':header,'url':url}
                    
        # exception handleA
#        if not str(response.status_code).startswith('2'):
#            raise exceptions.OkexAPIException(response)
        try:
            #res_header = r.headers
            pass
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
    
    def buildMySign(self, params):
        
        secretKey= self.secret
        
        sign = ''
        
        for key in sorted(params.keys()):
            sign += key + '=' + str(params[key]) +'&'
            
        data = sign+'secret_key='+secretKey
        return hashlib.md5(data.encode("utf8")).hexdigest().upper()
    
    def load_markets(self,Type='all'):
        
        if(not len(self.instruments) and Type=='all'):
            self.instruments = pd.DataFrame(columns=['instrument_id',
                                                     'api_type',
                                                     'futures_type'])
        
        if(Type == 'all'):
            for market_type in ['spot','futures','swap']:    
                self.load_markets(Type = market_type)
        
        if(Type in ['futures','swap']):
            
            json_text = pd.DataFrame(
                json.loads(
                    requests.get(
                        self.okex_url 
                        + '/api/%s/v3/instruments' 
                        % (Type)).content)).instrument_id
            json_list = list(json_text)
            count = 0
            for i in json_list: 
                init_contract_states = ['TW','NW','TQ','NQ']
                waiting_add_item = (i,Type,i[:-6] + init_contract_states[count % 4] if Type=='futures' else None)
                if not waiting_add_item in self.instruments:    
                    self.instruments.loc[len(self.instruments)] = waiting_add_item
                else:
                    pass
                count += 1
            
        if(Type in ['spot']):
            
            json_text = pd.DataFrame(
                json.loads(
                    requests.get(
                        self.okex_url +  
                        '/api/swap/v3/instruments').content)).instrument_id
            json_list = list(json_text)
            for i in json_list:
                corrective_i = i[:-5] 
                if corrective_i[-1] == 'T':
                    waiting_add_item = (corrective_i,Type,None)
                    if not waiting_add_item in self.instruments:
                        self.instruments.loc[ len (self.instruments) ] = (corrective_i,Type,None)
                else:
                    pass
        
        self.instruments = self.instruments.drop_duplicates()
        self.instruments.set_index(keys='instrument_id')
        
        return True
        
    def get_wallet(self):
        '''
        获取资金账户所有资产列表，查询各币种的余额、冻结和可用等信息。
        '''
        return self._request_without_params(GET, WALLET_INFO)
    
    def post_transfer(self,currency,amount,From,to,instrument_id,to_instrument_id):
        '''
        currency: 货币币种代码
        amount: 转账数量
        from: 转出账户代码
        to: 转入账户代码
            0:子账户
            1:币币
            3:合约
            4:C2C
            5:币币杠杆
            6:资金账户
            8:余币宝
            9:永续合约
            12:期权
        instrument_id: 具体交易对名称
        to_instrument_id: 具体交易对名称
        '''
        params = {}
        
        params['currency'] = currency
        params['amount'] = amount
        params['from'] = From
        params['to'] = to
        params['instrument_id'] = instrument_id
        params['to_instrument_id'] = to_instrument_id
        
        return self._request_with_params(POST, COIN_TRANSFER, params)
    
    def get_ledger(self,
                   currency=None,
                   after=None,
                   before=None,
                   limit=None,
                   Type=None):
        
        params = {}
        
        if currency:
            params['currency'] = currency
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
        if Type:
            params['type'] = Type
            
        return self._request_with_params(GET, LEDGER_RECORD, params)
        
        
    def get_asset_valuation(self,account_type = None,valuation_currency = None):
        
        params = {}
        
        if account_type:
            params['account_type'] = account_type
        if valuation_currency:
            params['valuation_currency'] = valuation_currency
            
        return self._request_with_params(GET, VALUATION_CURRENCY, params)
    
    
    def get_kline(self,Type, instrument_id, granularity='60', start='', end=''):
        
        params = {}
        
        if granularity:
            params['granularity'] = granularity
        if start:
            params['start'] = start
        if end:
            params['end'] = end
            
        if(Type in ['spot','lever','futures','swap','option']):
            KLINE_APIS ={
                    'spot':SPOT_KLINE,
                    'lever':SPOT_KLINE,
                    'futures':FUTURE_KLINE,
                    'swap':SWAP_INSTRUMENTS,
                    'option':OPTION_INSTRUMENTS
                    }
        else:
            print('Type error')
            return
        return self._request_with_params(GET, KLINE_APIS[Type]+'/'+str(instrument_id)+'/candles', params)

    
    
#    ——————————————————————————————————————————————————————————
    def create_future_order(self,instrument_id,otype,price,size, client_oid='',order_type='0', match_price='0'):
        #'client_oid': client_oid,
        params = { 'instrument_id': instrument_id, 
                  'type' : otype,
                  'price' : price,
                  'size' : size,
                  'client_oid'  : client_oid,
                  'order_type'  : order_type,
                  'match_price' : match_price,
                  }
        
        return self._request_with_params(POST, FUTURE_ORDER, params)
    
    def create_spot_order(self,  instrument_id, size, side, margin_trading='1', client_oid='', price='',order_type = '',otype = '',notional =''):
        params = {'type': otype, 
                  'side': side, 
                  'instrument_id': instrument_id, 
                  'size': size, 
                  'client_oid': client_oid,
                  'price': price,
                  'notional': notional,
                  'margin_trading': margin_trading,
                  'order_type':order_type}
        print(params)
        return self._request_with_params(POST, SPOT_ORDER, params)
    
    def create_lever_order(self, 
                           instrument_id, 
                           side, 
                           margin_trading, 
                           price, 
                           size, 
                           client_oid='', otype='limit', order_type='0', notional=''):
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
    
    def create_swap_order(self, 
                          instrument_id,
                          size,
                          otype,
                          price,
                          client_oid='',
                          order_type='0',
                          match_price=''):    #'client_oid': client_oid,
        params = { 'instrument_id': instrument_id, 
                  'type': otype, 
                  'price': price, 
                  'size': size, 
                  'match_price':match_price, 
                  'client_oid':client_oid,
                  'order_type': order_type,
                  }
        return self._request_with_params(POST, SWAP_ORDER, params)


    def create_option_order(self, 
                            instrument_id, 
                            side, 
                            price, 
                            size, 
                            client_oid='', 
                            order_type='0', 
                            match_price=''):
        params = {'instrument_id':instrument_id,
                  'side':side,
                  'price':price,
                  'size':size,
                  'client_oid':client_oid,
                  'order_type':order_type,
                  'match_price':match_price}
        return self._request_with_params(POST, OPTION_ORDER, params)
# ——————————————————————————————————————————————————————————————————————
        
    def get_depth(self,Type, instrument_id, size='', depth=''):
        
        print('start')
        params = {}
        if(size):
            params['size'] = size
        if(Type in ['spot','futures','swap','option']):
            ACCOUNTS_APIS ={
                    'spot':SPOT_DEPTH + str(instrument_id) + '/book',
                    'futures':FUTURE_DEPTH + str(instrument_id) + '/book',
                    'swap':SWAP_INSTRUMENTS+'/'+str(instrument_id)+'/depth',
                    'option':OPTION_INSTRUMENT + '/' + str(instrument_id) +'/book'
                    }
        else:
            print('Type error')
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
        if(Type in ['spot','lever','futures','swap','option']):
            ACCOUNTS_APIS ={
                    'spot':SPOT_ACCOUNT_INFO,
                    'lever':LEVER_ACCOUNT,
                    'futures':FUTURE_ACCOUNTS,
                    'swap':SWAP_ACCOUNTS,
                    'option':OPTION_ACCOUNTS_BTCUSD
                    }
        else:
            print('Type error')
            return
        
        return self._request_without_params(GET, ACCOUNTS_APIS[Type])
    
    def get_position(self,Type):
        if(Type in ['futures','swap','option']):
            POSITION_APIS ={
                    'spot':'',
                    'lever':'',
                    'futures':FUTURE_POSITION,
                    'swap':SWAP_POSITIONS,
                    'option':OPTION_POSITION_BTCUSD
                    }
        else:
            print('Type error')
            return
        
        return self._request_without_params(GET, POSITION_APIS[Type])
    
    def get_position_single(self,Type,instrument_id=None):
        if (Type in ['futures','swap','option']):
            POSITION_APIS = {
                'spot':'',
                'lever':'',
                'futures':FUTURE_SPECIFIC_POSITION,
                'swap':SWAP_POSITION,
                'option':OPTION_POSITION_BTCUSD
                }
        else:
            print('Type error')
        
        if instrument_id and Type != 'option':
            print(POSITION_APIS[Type] + instrument_id)
            return self._request_without_params(GET, POSITION_APIS[Type] + instrument_id +'/position')
        
        elif instrument_id and Type == 'option':
            params = {'instrument_id':instrument_id}
            return self._request_with_params(GET, POSITION_APIS[Type], params)
        
        return self._request_without_params(GET, POSITION_APIS[Type])
    
    def get_order_info(self,Type, instrument_id, order_id='',client_oid = ''):
        if order_id:
            url_suffix = str(instrument_id) + '/' + str(order_id)
            #return self._request_without_params(GET, SWAP_ORDERS+'/'+str(instrument_id)+'/'+str(order_id))
        elif client_oid:
            url_suffix =  str(instrument_id) + '/' + str(client_oid)
            #return self._request_without_params(GET, SWAP_ORDERS + '/' + str(instrument_id) + '/' + str(client_oid))
            
        else:
            url_suffix = str(instrument_id)
            
        if(Type in ['spot','lever','futures','swap','option']):
            ORDER_APIS ={
                    'spot':SPOT_ORDER_INFO,
                    'lever':LEVER_ORDER_INFO,
                    'futures':FUTURE_ORDER_INFO,
                    'swap':SWAP_ORDERS + '/',
                    'option':OPTION_ORDERS + '/'
                    }
        else:
            print('Type error')
            return
        
        print(ORDER_APIS[Type] + url_suffix)
        
        return self._request_without_params(GET, ORDER_APIS[Type] + url_suffix)
        

    def cancel_order(self,Type, instrument_id, order_id='',client_oid=''):
        
        params = {'instrument_id':instrument_id}
        
        if order_id:
            url_suffix = str(order_id)

        elif client_oid:
            url_suffix = str(client_oid)
        
            
        else:
            print('The attributes order_id and client_oid cannot all be empty')
            
        if(Type in ['spot','lever','futures','swap','option']):
            ORDER_CANCEL_APIS ={
                    'spot':SPOT_REVOKE_ORDER,
                    'lever':LEVER_REVOKE_ORDER,
                    'futures':FUTURE_REVOKE_ORDER,
                    'swap':SWAP_CANCEL_ORDER,
                    'option':OPTION_CANCEL_ORDER
                    }
        else:
            print('Type error')
            return
        print(ORDER_CANCEL_APIS[Type] + url_suffix)
        
        return self._request_with_params(POST, ORDER_CANCEL_APIS[Type] + url_suffix,params)
    
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
            print('Type error')
            return 
        
        return self._request_with_params(GET, FILLS_APIS[Type], params)
        
        
    def get_order_list(self, Type, instrument_id, state ,after='', before='',limit=''):
        '''
        Parameters
        ----------
        Type : TYPE
            DESCRIPTION.
        instrument_id : TYPE
            DESCRIPTION.
        state : TYPE, optional
            -2:失败
            -1:撤单成功
            0:等待成交
            1:部分成交
            2:完全成交
            3:下单中
            4:撤单中
            6: 未完成（等待成交+部分成交）
            7:已完成（撤单成功+完全成交）
        to : TYPE, optional
            DESCRIPTION. The default is ''.
        limit : TYPE, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        params = {'state': state,'instrument_id':instrument_id}
        
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if limit:
            params['limit'] = limit
            
        if(Type in ['spot','lever','futures','swap','option']):
            ORDER_LIST_APIS ={
                    'spot':SPOT_ORDERS_LIST,
                    'lever':LEVER_ORDER_LIST,
                    'futures':FUTURE_ORDERS_LIST,
                    'swap':SWAP_ORDERS,
                    }
            
        return self._request_with_params(GET, ORDER_LIST_APIS[Type], params)


    # query coin account info
    def get_coin_account(self, symbol):
        return self._request_without_params(GET, FUTURE_COIN_ACCOUNT + str(symbol))


    def get_usdt_rate(self):
        return self._request_without_params(GET, SWAP_RATE)
        
    def get_historical_funding_rate(self, instrument_id,limit=None):
        params = {}
#        if froms:
#            params['from'] = froms
#        if to:
#            params['to'] = to
        if limit:
            params['limit'] = limit
        return self._request_with_params(GET, SWAP_INSTRUMENTS + '/' + str(instrument_id) + '/historical_funding_rate', params)
        
    def _get_timestamp(self):
        url = c.API_URL + c.SERVER_TIMESTAMP_URL
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()['iso']
        else:
            return ""
        
    #_______OPTION BELOW 
        
    def get_option_summary(self, instrument_id, 
                           underlying='BTC-USD'):
        
        return self._request_without_params(GET, 
                                            OPTION_INSTRUMENT +
                                            underlying +
                                            '/summary/' +
                                            instrument_id)
    
    def get_option_list_by_delivery(self,delivery='',
                                    underlying='BTC-USD'):
        params = {}
        if delivery:
            params['delivery'] = delivery
        
        return self._request_with_params(GET,
                                         OPTION_INSTRUMENT +
                                         underlying,
                                         params)
        
        
        
        
if __name__ == '__main__':
    e = Exchange(use_server_time=True)
    
    
    # this is a create_spot_order example
    #a.create_spot_order('XRP-USDT','1','buy',price='0.23',order_type='0')



