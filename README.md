# RESTFUL-API框架 for OKEX v3 接口文档

## Object: okex_api.Exchange()
默认调用 CONSTANT.V3_API_KEY\V3_SECRET\V3_PASSPHRASE

###  Exchange.get_timestamp()
​    功能：获取服务端的时间戳
​    参数 ：None
​    返回类型 : dict('iso','epoch')
​    返回数据样例：

```
{'iso': '2019-12-04T12:13:50.689Z', 'epoch': '1575461630.689'}
```


###  Exchange.load_markets(Type: str)
​    功能：加载市场中的交易对信息，并将其写入self.instruments中，self.instruments为DataFrame格式。
​    参数：Type(), 可选('all','spot','futures','swap')
​    返回类型：bool (Ture)表示获取成功
​    返回数据样例：

| instrument_id   | api_type | futures_type |
| --------------- | -------- | ------------ |
| BTC-USDT        | spot     |              |
| LTC-USDT        | spot     |              |
| ETH-USDT        | spot     |              |
| ETC-USDT        | spot     |              |
| XRP-USDT        | spot     |              |
| EOS-USDT        | spot     |              |
| BCH-USDT        | spot     |              |
| BSV-USDT        | spot     |              |
| TRX-USDT        | spot     |              |
| BTC-USDTT       | spot     |              |
| ETH-USDTT       | spot     |              |
| EOS-USDTT       | spot     |              |
| XRP-USD-191206  | futures  | XRP-USD-TW   |
| XRP-USD-191213  | futures  | XRP-USD-NW   |
| XRP-USD-191227  | futures  | XRP-USD-TQ   |
| BTC-USD-191206  | futures  | BTC-USD-TW   |
| BTC-USD-191213  | futures  | BTC-USD-NW   |
| BTC-USD-191227  | futures  | BTC-USD-TQ   |
| BTC-USDT-191206 | futures  | BTC-USDT-TW  |
| BTC-USDT-191213 | futures  | BTC-USDT-NW  |
| BTC-USDT-191227 | futures  | BTC-USDT-TQ  |
| LTC-USD-191206  | futures  | LTC-USD-TW   |
| LTC-USD-191213  | futures  | LTC-USD-NW   |
| LTC-USD-191227  | futures  | LTC-USD-TQ   |
| LTC-USDT-191206 | futures  | LTC-USDT-TW  |
| LTC-USDT-191213 | futures  | LTC-USDT-NW  |
| LTC-USDT-191227 | futures  | LTC-USDT-TQ  |
| ETH-USD-191206  | futures  | ETH-USD-TW   |
| ETH-USD-191213  | futures  | ETH-USD-NW   |
| ETH-USD-191227  | futures  | ETH-USD-TQ   |
| ETH-USDT-191206 | futures  | ETH-USDT-TW  |
| ETH-USDT-191213 | futures  | ETH-USDT-NW  |
| ETH-USDT-191227 | futures  | ETH-USDT-TQ  |
| ETC-USD-191206  | futures  | ETC-USD-TW   |
| ETC-USD-191213  | futures  | ETC-USD-NW   |
| ETC-USD-191227  | futures  | ETC-USD-TQ   |
| BCH-USD-191206  | futures  | BCH-USD-TW   |
| BCH-USD-191213  | futures  | BCH-USD-NW   |
| BCH-USD-191227  | futures  | BCH-USD-TQ   |
| BCH-USDT-191206 | futures  | BCH-USDT-TW  |
| BCH-USDT-191213 | futures  | BCH-USDT-NW  |
| BCH-USDT-191227 | futures  | BCH-USDT-TQ  |
| BSV-USD-191206  | futures  | BSV-USD-TW   |
| BSV-USD-191213  | futures  | BSV-USD-NW   |
| BSV-USD-191227  | futures  | BSV-USD-TQ   |
| EOS-USDT-191206 | futures  | EOS-USDT-TW  |
| EOS-USDT-191213 | futures  | EOS-USDT-NW  |
| EOS-USDT-191227 | futures  | EOS-USDT-TQ  |
| XRP-USDT-191206 | futures  | XRP-USDT-TW  |
| XRP-USDT-191213 | futures  | XRP-USDT-NW  |
| XRP-USDT-191227 | futures  | XRP-USDT-TQ  |
| ETC-USDT-191206 | futures  | ETC-USDT-TW  |
| ETC-USDT-191213 | futures  | ETC-USDT-NW  |
| ETC-USDT-191227 | futures  | ETC-USDT-TQ  |
| EOS-USD-191206  | futures  | EOS-USD-TW   |
| EOS-USD-191213  | futures  | EOS-USD-NW   |
| EOS-USD-191227  | futures  | EOS-USD-TQ   |
| TRX-USD-191206  | futures  | TRX-USD-TW   |
| TRX-USD-191213  | futures  | TRX-USD-NW   |
| TRX-USD-191227  | futures  | TRX-USD-TQ   |
| BTC-USD-SWAP    | swap     |              |
| LTC-USD-SWAP    | swap     |              |
| ETH-USD-SWAP    | swap     |              |
| ETC-USD-SWAP    | swap     |              |
| XRP-USD-SWAP    | swap     |              |
| EOS-USD-SWAP    | swap     |              |
| BCH-USD-SWAP    | swap     |              |
| BSV-USD-SWAP    | swap     |              |
| TRX-USD-SWAP    | swap     |              |
| BTC-USDT-SWAP   | swap     |              |
| ETH-USDT-SWAP   | swap     |              |
| EOS-USDT-SWAP   | swap     |              |

###  Exchange.get_kline(Type: str, instrument_id: str, granularity='60', start='', end='')

 	功能：加载市场中的Kline数据（OHLCV），V3的Kline最大limit在spot、futures中应该是300根，但是我觉得就尼玛离谱，swap类型却最多能返回200根，真的想不明白是怎么整的。
    参数：

1. Type: str, 可选('spot','futures','swap')
2. instrument_id: str，为交易标的名称（如BTC-USDT，BTC-USD-191227，BTC-SWAP）
3. granularity: str，为K线长度（如60为60秒K线，3600为3600秒K线，分别对应一分钟和一小时，以此类推）
4. start: str，为调用K线的开端时间，与end不可同时使用
5. end: str，为调用K线最后一根的时间，与start不可同时使用

​    返回类型：list(list)，二维数组,表示获取成功
​    返回数据样例：

> ```
>  [['2019-12-05T04:40:00.000Z', '94.88', '96.15','94.88', '95.35', '3491', '364.9753'],
>  ['2019-12-05T04:39:00.000Z',  '94.8',  '94.88',  '94.8',  '94.88',  '48',  '5.0613'],
>  ['2019-12-05T04:38:00.000Z',  '94.65',  '94.65',  '94.65', '94.65',  '89',  '9.403'],
>  ['2019-12-05T04:37:00.000Z', '94.6', '94.6', '94.6', '94.6', '5', '0.5285'],
>  ['2019-12-05T04:36:00.000Z', '94.61', '94.61', '94.61', '94.61', '0', '0']]
> ```

###  Exchange.get_depth(Type: str, instrument_id: str, size='', depth='')

功能：获取深度数据

参数：

1. `Type`: str, 可选('spot','futures','swap')
2. `instrument_id`: str，为交易标的名称（如BTC-USDT，BTC-USD-191227，BTC-SWAP）
3. `size`: str，为深度数，默认为1
4. `depth`: str，只在spot数据里有，没整明白是什么玩意，估计和size是一样的，只传一个就行了

返回类型：dict{'asks','bids','timestamp'}

返回数据样例：

```
{'asks': [['7295.6', '0.00274196', '1'], ['7296', '0.001', '1']],
 'bids': [['7295.5', '12.23757225', '13'], ['7295.3', '0.004', '1']],
 'timestamp': '2019-12-05T08:11:15.379Z'}
```

###  Exchange.create_future_order(instrument_id: str, type: str, price: str, size: str, client_oid='',order_type='0', match_price='0')

功能：交割期货下单。

参数：

1. `instrument_id`: str，为交易标的名称（如BTC-USD-191227）

2. `type`: str, 

   `1`:开多
   `2`:开空
   `3`:平多
   `4`:平空

3. `size`: str, 下单数量

4. `price`: str,  委托价格

5. `client_oid`: str, 由您设置的订单ID来识别您的订单 ,类型为字母（大小写）+数字或者纯字母（大小写），1-32位字符

6. `order_type`: str, 

   `0`：普通委托（order type不填或填0都是普通委托）
   `1`：只做Maker（Post only）
   `2`：全部成交或立即取消（FOK）
   `3`：立即成交并取消剩余（IOC）

7. `match_price`: str，是否以对手价下单(`0`:不是; `1`:是)，默认为`0`，当取值为`1`时，price字段无效。当以对手价下单，`order_type`只能选择`0`（普通委托）

返回类型：dict{'asks','bids','timestamp'}

返回数据样例：

```
{'asks': [['7295.6', '0.00274196', '1'], ['7296', '0.001', '1']],
 'bids': [['7295.5', '12.23757225', '13'], ['7295.3', '0.004', '1']],
 'timestamp': '2019-12-05T08:11:15.379Z'}
```

###  Exchange.create_spot_order(instrument_id: str, side: str, client_oid='', type='limit', order_type='0')

功能：现货下单。

参数：

1. `instrument_id`: str，为交易标的名称（如BTC-USD-191227）

2. `side`: str

   `buy`: 买入

   `sell`: 卖出

3. `type`: str, 

   `limit`: 限价单
   `market`: 市价单

4. `size`: str, 下单数量

5. `price`: str,  委托价格

6. `client_oid`: str, 由您设置的订单ID来识别您的订单 ,类型为字母（大小写）+数字或者纯字母（大小写），1-32位字符

7. `order_type`: str, 

   `0`：普通委托（order type不填或填0都是普通委托）
   `1`：只做Maker（Post only）
   `2`：全部成交或立即取消（FOK）
   `3`：立即成交并取消剩余（IOC）

8. `notional`: str, 买入金额，市价买入时必填`notional`

返回类型：dict()

返回数据样例：

```
{
    "client_oid":"oktspot79",
    "error_code":"",
    "error_message":"",
    "order_id":"2510789768709120",
    "result":true
}
```

###  Exchange.create_lever_order(instrument_id: str, side: str, margin_trading: str, price: str, size: str, client_oid='', type='limit', order_type='0', notional='')

功能：现货杠杆下单。

参数：

1. `instrument_id`: str，为交易标的名称（如BTC-USD-191227）

2. `side`: str

   `buy`: 买入

   `sell`: 卖出

3. `margin_trading`: str，默认为2

4. `client_oid`: str, 由您设置的订单ID来识别您的订单 ,类型为字母（大小写）+数字或者纯字母（大小写），1-32位字符

5. `order_type`: str, 

   `0`：普通委托（order type不填或填0都是普通委托）
   `1`：只做Maker（Post only）
   `2`：全部成交或立即取消（FOK）
   `3`：立即成交并取消剩余（IOC）

6. `type`: str, 

   `limit`: 限价单
   `market`: 市价单

7. `price`: str, 价格

8. `size`: str, 交易数量

9. `notional`: str, 买入金额，市价买入时必填`notional`

返回类型：dict()

返回数据样例：

```
{
    "client_oid":"oktlever50",
    "error_code":"",
    "error_message":"",
    "order_id":"2512084870235136",
    "result":true
}
```

###  Exchange.create_swap_order(instrument_id: str,size: str,otype: str,price: str ,client_oid='',order_type='0',match_price='')

功能：现货杠杆下单。

参数：

1. `instrument_id`: str，为交易标的名称（如BTC-USD-SWAP）

2. `otype`: str，

    可填参数： `1`:开多 `2`:开空 `3`:平多 `4`:平空

3. `client_oid`: str, 由您设置的订单ID来识别您的订单 ,类型为字母（大小写）+数字或者纯字母（大小写），1-32位字符

4. `order_type`: str, 

   `0`：普通委托（order type不填或填0都是普通委托）
   `1`：只做Maker（Post only）
   `2`：全部成交或立即取消（FOK）
   `3`：立即成交并取消剩余（IOC）

5. `price`: str, 价格

6. `size`: str, 交易数量

7. `match_price`: str, 是否以对手价下单。
   `0`:不是; `1`:是。当以对手价下单，`order_type`只能选择`0`（普通委托）

返回类型：dict()

返回数据样例：

```
{
    "error_message":"",
    "result":"true",
    "error_code":"0",
    "client_oid":"oktswap6",
    "order_id":"6a-d-54dcc6543-0"
}
```

###  Exchange.get_position(Type: str)

功能：加载市场中的交易对信息，并将其写入self.instruments中，self.instruments为DataFrame格式。
参数：Type(), 可选(spot','lever','futures','swap')
返回类型：dict('result','holding'), result: bool, holding: dict(list(dicts))
返回数据样例：如下

| created_at               | instrument_id  | last    | leverage | liquidation_price | long_avail_qty | long_avg_cost | long_margin | long_pnl   | long_pnl_ratio | long_qty | long_settled_pnl | long_settlement_price | long_unrealised_pnl | margin_mode | realised_pnl | short_avail_qty | short_avg_cost | short_margin | short_pnl | short_pnl_ratio | short_qty | short_settled_pnl | short_settlement_price | short_unrealised_pnl | updated_at               |
| ------------------------ | -------------- | ------- | -------- | ----------------- | -------------- | ------------- | ----------- | ---------- | -------------- | -------- | ---------------- | --------------------- | ------------------- | ----------- | ------------ | --------------- | -------------- | ------------ | --------- | --------------- | --------- | ----------------- | ---------------------- | -------------------- | ------------------------ |
| 2019-09-30T10:26:26.272Z | BTC-USD-191227 | 7331.91 | 100      | 0.00              | 0              | 8392          | 0.0         | 0.0        | -14.476222     | 0        | 0                | 7442.67               | 0.0                 | crossed     | 0            | 0               | 9625.57862816  | 0.0          | 0.0       | 31.303608       | 0         | 0                 | 9683.27                | 0.0                  | 2019-12-05T08:00:42.886Z |
| 2019-10-12T03:54:38.933Z | ETH-USD-191227 | 146.0   | 50       | 0.000             | 0              | 171.95009322  | 0.0         | 0.0        | -8.887018      | 0        | 0                | 161.659               | 0.0                 | crossed     | 0            | 0               | 188.439        | 0.0          | 0.0       | 14.533904       | 0         | 0                 | 188.819                | 0.0                  | 2019-12-05T08:00:53.814Z |
| 2019-09-16T04:51:41.568Z | BSV-USD-191227 | 96.86   | 20       | 80.35             | 0              | 112.19541605  | 25.03611226 | -68.173379 | -3.15217       | 4853     | -76.63170252     | 95.31                 | 8.45832352          | crossed     | 0            | 0               | 137.99         | 0.0          | 0.0       | 8.475031        | 0         | 0                 | 98.68                  | 0.0                  | 2019-12-05T08:35:59.859Z |

###  Exchange.get_accounts(Type: str)

功能：加载市场中的交易对信息，并将其写入self.instruments中，self.instruments为DataFrame格式。
参数：Type(), 可选(spot','lever','futures','swap')
返回类型：dict('info'), info: list(dicts)
返回数据样例：如下

```
[{'equity': '10000.00',
 'fixed_balance': '0.00',
 'instrument_id': 'EOS-USDT-SWAP',
 'maint_margin_ratio': '',
 'margin': '0.00',
 'margin_frozen': '0.00',
 'margin_mode': '',
 'margin_ratio': '0.0000',
 'max_withdraw': '10000.00',
 'realized_pnl': '0.00',
 'timestamp': '2019-12-04T06:02:30.000Z',
 'total_avail_balance': '10000.00',
 'unrealized_pnl': '0.00'}]
```



###  Exchange.get_order_info(Type, instrument_id, order_id='',client_oid = '')

功能：加载private订单信息，参照order_id和client_oid进行查询，client_oid为用户自设定的oid, order_id在create_order返回数据中。
参数：

1. Type: str, 可选(spot','lever','futures','swap')
2. instrument_id: str， 略。
3. order_id: int, 为订单id，系统自动生成，在create_order返回数据中查询。
4. client_oid: int，为用户自设定oid，在create_order中获取。

返回类型：dict()
返回数据样例：如下

```
{'instrument_id': 'BSV-USD-SWAP',
 'size': '1',
 'timestamp': '2019-12-05T08:58:22.428Z',
 'filled_qty': '0',
 'fee': '0.000000',
 'order_id': '3823390156174970882', # has been changed
 'price': '88.00',
 'price_avg': '0.00',
 'trigger_price': None,
 'status': '0',
 'state': '0',
 'type': '1',
 'contract_val': '10',
 'client_oid': '',
 'order_type': '0'}
```



###  Exchange.cancel_order(Type, instruments, order_id='',client_oid='')

功能：撤销private order。
参数：

1. Type: str, 可选(spot','lever','futures','swap')
2. instrument_id: str， 略。
3. order_id: int, 为订单id，系统自动生成，在create_order返回数据中查询。
4. client_oid: int，为用户自设定oid，在create_order中获取。

返回类型：dict()
返回数据样例：如下

```
{'result': 'true', 

'order_id': '382339015617497088'}
```

###  Exchange.get_fills(Type, instruments_id ,order_id='', client_oid='', froms='', to='', limit='')

功能：获取最近的成交明细列表，本接口能查询最近7天的数据。
参数：

1. Type: str, 可选(spot','lever','futures','swap')
2. instrument_id: str， 略。
3. order_id: int, 为订单id，系统自动生成，在create_order返回数据中查询。
4. client_oid: int，为用户自设定oid，在create_order中获取。
5. from: string, 请求此id之前（更旧的数据）的分页内容，传的值为对应接口的trade_id
6. to: string, 请求此id之后（更新的数据）的分页内容，传的值为对应接口的trade_id
7. limit: int,  分页返回的结果集数量，最大为100，不填默认返回100条

返回类型：list(dicts)
返回数据样例：如下

```
{'created_at': '2019-09-25T02:06:37.000Z',
  'exec_type': 'T',
  'fee': '0',
  'instrument_id': 'BSV-USDT',
  'ledger_id': '7252732078',
  'liquidity': 'T',
  'order_id': '3580965487790080',
  'price': '88.75',
  'product_id': 'BSV-USDT',
  'side': 'sell',
  'size': '7.5111',
  'timestamp': '2019-09-25T02:06:37.000Z'}
```

###  Exchange.get_coin_account(symbol: str)

功能：查询某一个账户的币余额信息，spot、futures、swap都适用，我觉得离谱，都这么设计不好吗？

参数：symbol: str，例如BTC-USDT，BTC-USD，BTC-USD-191227，BTC-USD-SWAP，都tm avaiable

返回类型：dict()

返回数据样例：如下

```
{'equity': '117.83970777',
 'margin': '24.93120827',
 'realized_pnl': '0',
 'unrealized_pnl': '10.67003965',
 'margin_ratio': '0.23632972',
 'margin_mode': 'crossed',
 'total_avail_balance': '107.16966812',
 'margin_frozen': '24.92552645',
 'margin_for_unfilled': '0.00568182',
 'liqui_mode': 'tier',
 'maint_margin_ratio': '0.02',
 'liqui_fee_rate': '0.0005',
 'can_withdraw': '92.9084995',
 'underlying': 'BSV-USD',
 'currency': 'BSV'}
```



###  Exchange.get_usdt_rate()

功能：查询usdt/cny官方汇率。

参数：None

返回类型：dict()

返回数据样例：如下

```
{'instrument_id': 'USD_CNY',
 'rate': '7.029',
 'timestamp': '2019-12-05T09:29:59.267Z'}
```



###  Exchange.get_historical_funding_rate(instrument_id, limit='')

功能：加载SWAP的历史交割费率，
    参数：

1. instrument_id: str，为交易标的名称（如BTC-USD-SWAP）
2. limit: str，返回数据的长度，默认100。

​    返回类型：list(dict)
​    返回数据样例：

```
[{'instrument_id': 'BTC-USD-SWAP',
  'funding_rate': '-0.00014574',
  'realized_rate': '-0.00014574',
  'interest_rate': '0.00000000',
  'funding_time': '2019-12-05T08:00:00.000Z'},
 {'instrument_id': 'BTC-USD-SWAP',
  'funding_rate': '-0.00014378',
  'realized_rate': '-0.00014378',
  'interest_rate': '0.00000000',
  'funding_time': '2019-12-05T00:00:00.000Z'}]
```

