---
name: "tdx-stock-query"
description: "基于TDX API的股票数据查询技能，提供全面的A股市场数据查询功能，包括实时行情、K线数据、分时数据、分时成交、股票搜索、指数数据、ETF数据、市场统计、个股新闻、股票公告等31个API接口。当用户询问股票相关信息时调用。"
---

# TDX股票查询技能

## 功能描述

本技能基于TDX股票数据API，提供以下全面功能：

### 基础数据查询
- 股票实时五档行情查询
- K线数据查询（分钟/小时/日/周/月/季/年）
- 分时走势数据查询
- 分时成交明细查询
- 股票代码搜索
- 股票综合信息查询

### 扩展功能
- 股票代码列表获取
- 批量行情查询
- 历史K线范围查询
- 指数数据查询
- 市场统计数据
- 服务状态查询

### 数据入库任务
- 批量K线数据入库任务
- 分时成交数据入库任务
- 任务状态查询和控制

### 高级数据服务
- ETF基金列表查询
- 历史分时成交分页查询
- 全天分时成交汇总
- 交易日信息查询
- 市场证券数量统计
- 全部股票代码查询
- 全部ETF代码查询
- 股票历史K线全集
- 指数历史K线全集
- 上市以来分时成交
- 交易日范围列表
- 收益区间分析
- 个股新闻查询
- 股票公告查询

## API地址配置（必须）

**重要：使用本技能前，必须先配置API地址！**

### 1. TDX API配置

本技能需要用户自行提供TDX API的服务地址，通过环境变量 `TDX_API_URL` 进行配置。

**环境变量名称**: `TDX_API_URL`

**配置方法**:

1. **环境变量方式**:
   ```bash
   export TDX_API_URL=http://your-api-domain.com
   ```

2. **.env文件方式**:
   ```
   TDX_API_URL=http://your-api-domain.com
   ```

### 2. akshare API配置（可选）

如果需要使用个股新闻查询功能，还需要配置akshare API地址。

**环境变量名称**: `AKSHARE_API_URL`

**配置方法**:

1. **环境变量方式**:
   ```bash
   export AKSHARE_API_URL=http://your-akshare-api.com
   ```

2. **.env文件方式**:
   ```
   AKSHARE_API_URL=http://your-akshare-api.com
   ```

**注意**：`AKSHARE_API_URL` 是可选的，仅当需要使用个股新闻查询功能时才需要配置。

**使用方式**:
```python
from main import TDXStockQuery

# 初始化时会自动读取TDX_API_URL环境变量
stock_query = TDXStockQuery()

# 查询股票信息
result = stock_query.get_quote(['000001'])
```

**未配置环境变量的错误提示**:
如果未配置 `TDX_API_URL` 环境变量，初始化时会抛出错误：
```
ValueError: 环境变量 TDX_API_URL 未设置，请先配置API地址
```

## 接口说明

### 1. 获取五档行情

**接口**: `get_quote(codes)`

**参数**: `codes` - 股票代码列表，如 ['000001', '600519']

**示例**:
```python
result = stock_query.get_quote(['000001', '600519'])
```

**返回数据包含**:
- Exchange: 交易所代码
- Code: 股票代码
- K: 昨收、开盘、最高、最低、收盘价（厘）
- TotalHand: 总手数
- Amount: 成交额
- InsideDish: 内盘
- OuterDisc: 外盘
- BuyLevel: 买五档
- SellLevel: 卖五档

### 2. 获取K线数据

**接口**: `get_kline(code, ktype='day')`

**参数**:
- `code` - 股票代码，如 '000001'
- `ktype` - K线类型，默认day

**K线类型**: minute1, minute5, minute15, minute30, hour, day, week, month, quarter, year

**示例**:
```python
result = stock_query.get_kline('000001', 'day')
result = stock_query.get_kline('600519', 'minute30')
```

**返回数据包含**:
- Last, Open, High, Low, Close: 价格（厘）
- Volume: 成交量（手）
- Amount: 成交额（厘）
- Time: 时间
- UpCount, DownCount: 上涨下跌数（指数有效）

### 3. 获取分时数据

**接口**: `get_minute(code, date=None)`

**参数**:
- `code` - 股票代码，如 '000001'
- `date` - 日期（YYYYMMDD格式），默认当天

**示例**:
```python
result = stock_query.get_minute('000001')
result = stock_query.get_minute('000001', '20241103')
```

**返回数据包含**:
- date: 实际数据日期
- Count: 数据点数量
- List: 分时数据列表（Time, Price, Number）

### 4. 获取分时成交

**接口**: `get_trade(code, date=None)`

**参数**:
- `code` - 股票代码，如 '000001'
- `date` - 日期（YYYYMMDD格式），默认当天

**示例**:
```python
result = stock_query.get_trade('000001')
result = stock_query.get_trade('000001', '20241103')
```

**返回数据包含**:
- Time: 成交时间
- Price: 成交价（厘）
- Volume: 成交量（手）
- Status: 0=买入, 1=卖出, 2=中性
- Number: 成交单数

### 5. 搜索股票代码

**接口**: `search_stock(keyword)`

**参数**: `keyword` - 搜索关键词（代码或名称）

**示例**:
```python
result = stock_query.search_stock('平安')
result = stock_query.search_stock('000001')
```

**返回数据包含**:
- code: 股票代码
- name: 股票名称

### 6. 获取股票综合信息

**接口**: `get_stock_info(code)`

**参数**: `code` - 股票代码，如 '000001'

**示例**:
```python
result = stock_query.get_stock_info('000001')
```

**返回数据包含**:
- quote: 五档行情
- kline_day: 最近30天日K线
- minute: 今日分时数据

### 7. 获取股票详细信息列表

**接口**: `get_codes(exchange='all')`

**参数**: `exchange` - 交易所代码，默认all

**交易所代码**: sh, sz, bj, all

**示例**:
```python
result = stock_query.get_codes()
result = stock_query.get_codes('sh')
```

**返回数据包含**:
- total: 总数量
- exchanges: 各交易所数量
- codes: 股票详细信息列表（包含代码、名称、交易所）

### 8. 批量获取行情

**接口**: `batch_quote(codes)`

**参数**: `codes` - 股票代码列表，最多50只

**示例**:
```python
result = stock_query.batch_quote(['000001', '600519', '601318'])
```

### 9. 获取历史K线

**接口**: `get_kline_history(code, ktype='day', start_date=None, end_date=None, limit=100)`

**参数**:
- `code` - 股票代码
- `ktype` - K线类型
- `start_date` - 开始日期（YYYYMMDD）
- `end_date` - 结束日期（YYYYMMDD）
- `limit` - 返回条数，默认100，最大800

**示例**:
```python
result = stock_query.get_kline_history('000001', 'day', limit=30)
result = stock_query.get_kline_history('000001', 'day', start_date='20241001', end_date='20241101')
```

### 10. 获取指数数据

**接口**: `get_index(code, ktype='day')`

**参数**:
- `code` - 指数代码，如 'sh000001'
- `ktype` - K线类型，默认day

**常用指数代码**:
- sh000001 - 上证指数
- sz399001 - 深证成指
- sz399006 - 创业板指
- sh000300 - 沪深300

**示例**:
```python
result = stock_query.get_index('sh000001', 'day')
```

### 11. 获取服务状态

**接口**: `get_server_status()`

**示例**:
```python
result = stock_query.get_server_status()
```

**返回数据包含**:
- status: 服务状态
- connected: 连接状态
- version: 版本号
- uptime: 运行时间

### 12. 健康检查

**接口**: `health_check()`

**示例**:
```python
result = stock_query.health_check()
```

### 13. 创建批量K线入库任务

**接口**: `create_pull_kline_task(codes=None, tables=None, dir=None, limit=1, start_date=None)`

**参数**:
- `codes` - 股票代码数组，默认全部A股
- `tables` - K线类型列表，默认['day']
- `dir` - 存储目录，默认'data/database/kline'
- `limit` - 并发协程数量，默认1
- `start_date` - 起始日期阈值

**K线类型**: minute, 5minute, 15minute, 30minute, hour, day, week, month, quarter, year

**示例**:
```python
result = stock_query.create_pull_kline_task(
    codes=['000001', '600519'],
    tables=['day', 'week', 'month'],
    limit=4,
    start_date='2020-01-01'
)
```

**返回数据包含**:
- task_id: 任务ID

### 14. 创建分时成交入库任务

**接口**: `create_pull_trade_task(code, dir=None, start_year=2000, end_year=None)`

**参数**:
- `code` - 股票代码
- `dir` - 输出目录，默认'data/database/trade'
- `start_year` - 起始年份，默认2000
- `end_year` - 结束年份，默认当年

**示例**:
```python
result = stock_query.create_pull_trade_task(
    code='000001',
    start_year=2015,
    end_year=2023
)
```

### 15. 查询任务列表

**接口**: `get_tasks()`

**示例**:
```python
result = stock_query.get_tasks()
```

### 16. 查询任务详情

**接口**: `get_task_detail(task_id)`

**参数**: `task_id` - 任务ID

**示例**:
```python
result = stock_query.get_task_detail('9b0d1b1b-7c3d-4ce6-9a0e-bd9f5e0dcf3b')
```

### 17. 取消任务

**接口**: `cancel_task(task_id)`

**参数**: `task_id` - 任务ID

**示例**:
```python
result = stock_query.cancel_task('9b0d1b1b-7c3d-4ce6-9a0e-bd9f5e0dcf3b')
```

### 18. 获取ETF列表

**接口**: `get_etf(exchange='all', limit=None)`

**参数**:
- `exchange` - 交易所，默认all
- `limit` - 返回条数限制

**示例**:
```python
result = stock_query.get_etf()
result = stock_query.get_etf('sh', limit=10)
```

**返回数据包含**:
- code: ETF代码
- name: ETF名称
- exchange: 交易所
- last_price: 最新价格

### 19. 获取历史分时成交（分页）

**接口**: `get_trade_history(code, date, start=0, count=2000)`

**参数**:
- `code` - 股票代码
- `date` - 交易日期（YYYYMMDD）
- `start` - 起始游标，默认0
- `count` - 返回条数，默认2000，最大2000

**示例**:
```python
result = stock_query.get_trade_history('000001', '20241108')
result = stock_query.get_trade_history('000001', '20241108', start=0, count=1000)
```

### 20. 获取全天分时成交

**接口**: `get_minute_trade_all(code, date=None)`

**参数**:
- `code` - 股票代码
- `date` - 交易日期（YYYYMMDD），默认当天

**示例**:
```python
result = stock_query.get_minute_trade_all('000001')
result = stock_query.get_minute_trade_all('000001', '20241108')
```

### 21. 查询交易日信息

**接口**: `get_workday(date=None, count=1)`

**参数**:
- `date` - 查询日期（YYYYMMDD），默认当天
- `count` - 返回的前后交易日数量，范围1-30，默认1

**示例**:
```python
result = stock_query.get_workday()
result = stock_query.get_workday('20241108', count=3)
```

**返回数据包含**:
- date: 查询日期
- is_workday: 是否交易日
- next: 后续交易日
- previous: 前续交易日

### 22. 获取市场证券数量

**接口**: `get_market_count()`

**示例**:
```python
result = stock_query.get_market_count()
```

**返回数据包含**:
- total: 总数量
- exchanges: 各交易所数量

### 23. 获取全部股票代码

**接口**: `get_stock_codes(limit=None, prefix=True)`

**参数**:
- `limit` - 返回条数限制
- `prefix` - 是否包含交易所前缀，默认true

**示例**:
```python
result = stock_query.get_stock_codes()
result = stock_query.get_stock_codes(limit=100, prefix=False)
```

**返回数据包含**:
- count: 代码总数
- list: 股票代码列表

### 24. 获取全部ETF代码

**接口**: `get_etf_codes(limit=None, prefix=True)`

**参数**:
- `limit` - 返回条数限制
- `prefix` - 是否包含交易所前缀，默认true

**示例**:
```python
result = stock_query.get_etf_codes()
result = stock_query.get_etf_codes(limit=50, prefix=False)
```

**返回数据包含**:
- count: 代码总数
- list: ETF代码列表

### 25. 获取股票全部历史K线

**接口**: `get_kline_all(code, ktype='day', limit=None)`

**参数**:
- `code` - 股票代码
- `ktype` - K线类型，默认day
- `limit` - 返回条数限制

**示例**:
```python
result = stock_query.get_kline_all('000001')
result = stock_query.get_kline_all('000001', 'day', limit=100)
```

### 26. 获取指数全部历史K线

**接口**: `get_index_all(code, ktype='day', limit=None)`

**参数**:
- `code` - 指数代码
- `ktype` - K线类型，默认day
- `limit` - 返回条数限制

**示例**:
```python
result = stock_query.get_index_all('sh000001')
result = stock_query.get_index_all('sh000001', 'day', limit=200)
```

### 27. 获取上市以来分时成交

**接口**: `get_trade_history_full(code, before=None, limit=None)`

**参数**:
- `code` - 股票代码
- `before` - 截止日期（YYYYMMDD），默认今天
- `limit` - 返回条数限制

**示例**:
```python
result = stock_query.get_trade_history_full('000001')
result = stock_query.get_trade_history_full('000001', before='20241108', limit=5000)
```

### 28. 获取交易日范围

**接口**: `get_workday_range(start, end)`

**参数**:
- `start` - 起始日期（YYYYMMDD）
- `end` - 结束日期（YYYYMMDD）

**示例**:
```python
result = stock_query.get_workday_range('20241101', '20241130')
```

### 29. 计算收益区间指标

**接口**: `get_income(code, start_date)`

**参数**:
- `code` - 股票代码
- `start_date` - 基准日期（YYYYMMDD）

**示例**:
```python
result = stock_query.get_income('000001', '20241101')
```

### 30. 个股新闻查询

**接口**: `get_stock_news(symbol)`

**参数**:
- `symbol` - 股票代码或关键词，如 '603777' 或 '宁德时代'

**示例**:
```python
# 查询股票代码相关新闻
result = stock_query.get_stock_news('603777')

# 查询关键词相关新闻
result = stock_query.get_stock_news('宁德时代')
```

**返回数据包含**:
- 关键词: 搜索关键词
- 新闻标题: 新闻标题
- 新闻内容: 新闻内容摘要
- 发布时间: 新闻发布时间
- 文章来源: 新闻来源
- 新闻链接: 新闻详情链接

**注意**:
- 需要配置环境变量 `AKSHARE_API_URL` 才能使用此功能
- 当查询关键词包含中文时，API会自动进行URL编码
- 新闻数据来自东方财富网

### 31. 股票公告查询

**接口**: `get_stock_disclosure(symbol, start_date, end_date, market='沪深京', category=None, keyword=None)`

**参数**:
- `symbol` - 股票代码，如 '300058'
- `start_date` - 起始日期，格式YYYYMMDD，如 '20260101'
- `end_date` - 结束日期，格式YYYYMMDD，如 '20260314'
- `market` - 市场，默认'沪深京'
- `category` - 公告分类，如 '年报'、'董事会'、'权益分派' 等（可选）
- `keyword` - 关键词搜索，在公告标题中进行搜索（可选）

**公告分类选项**:
- 定期报告: '年报'、'半年报'、'一季报'、'三季报'
- 业绩相关: '业绩预告'
- 公司治理: '董事会'、'监事会'、'股东大会'、'公司治理'
- 股本权益: '权益分派'、'股权变动'、'股权激励'、'解禁'
- 融资相关: '增发'、'配股'、'公司债'、'可转债'
- 重大事项: '资产重组'、'日常经营'、'风险提示'
- 其他: '中介报告'、'首发'、'补充更正'、'澄清致歉'等

**示例**:
```python
# 查询股票300058在2026年第一季度发布的所有类型公告
result = stock_query.get_stock_disclosure('300058', '20260101', '20260331')

# 查询股票300058在2026年发布的"董事会"相关公告
result = stock_query.get_stock_disclosure('300058', '20260101', '20261231', category='董事会')

# 查询股票300058近期关于"权益分派"的公告
result = stock_query.get_stock_disclosure('300058', '20250101', '20260314', category='权益分派')

# 查询股票300058在2025年全年标题中包含"担保"关键词的公告
result = stock_query.get_stock_disclosure('300058', '20250101', '20251231', keyword='担保')
```

**返回数据包含**:
- 代码: 股票代码
- 简称: 股票简称
- 公告标题: 公告的完整标题
- 公告时间: 公告的发布日期
- 公告链接: 指向巨潮资讯网公告原文PDF/HTML的直达链接

**注意**:
- 需要配置环境变量 `AKSHARE_API_URL` 才能使用此功能
- 必须指定日期范围，无法一次性获取"最新100条"
- 数据来源是巨潮资讯网，具有最高权威性
- 公告链接可直接访问PDF原文，用于存档或深度分析
- 建议设定足够长的近期范围（如过去一年），然后按公告时间倒序排列取前100条，即为最新的100条权威公告

## 使用示例

### 查询股票实时行情

**用户提问**: 查询平安银行和贵州茅台的实时行情

**调用代码**:
```python
result = stock_query.get_quote(['000001', '600519'])
```

### 查询股票K线数据

**用户提问**: 查询贵州茅台最近30天的日K线数据

**调用代码**:
```python
result = stock_query.get_kline_history('600519', 'day', limit=30)
```

### 查询股票分时数据

**用户提问**: 查询平安银行今天的分时走势

**调用代码**:
```python
result = stock_query.get_minute('000001')
```

### 查询股票分时成交

**用户提问**: 查询贵州茅台今天的分时成交明细

**调用代码**:
```python
result = stock_query.get_trade('600519')
```

### 搜索股票

**用户提问**: 搜索包含"平安"的股票

**调用代码**:
```python
result = stock_query.search_stock('平安')
```

### 查询指数数据

**用户提问**: 查询上证指数的日K线数据

**调用代码**:
```python
result = stock_query.get_index('sh000001', 'day')
```

### 批量获取行情

**用户提问**: 批量获取自选股的实时行情

**调用代码**:
```python
result = stock_query.batch_quote(['000001', '600519', '601318'])
```

### 查询ETF列表

**用户提问**: 查询所有ETF基金

**调用代码**:
```python
result = stock_query.get_etf()
```

### 查询交易日信息

**用户提问**: 查询2024年11月8日是否为交易日

**调用代码**:
```python
result = stock_query.get_workday('20241108')
```

### 创建数据入库任务

**用户提问**: 创建批量K线数据入库任务

**调用代码**:
```python
result = stock_query.create_pull_kline_task(
    codes=['000001', '600519'],
    tables=['day', 'week'],
    limit=2
)
```

## 数据说明

### 价格单位
- 所有价格单位为"厘"（1元 = 1000厘）
- 转换公式：价格（元）= 价格（厘） / 1000

### 成交量单位
- 成交量单位为"手"（1手 = 100股）
- 挂单量单位为"股"

### 时间格式
- 分时数据时间格式：HH:MM
- K线数据时间格式：ISO 8601格式
- 分时成交时间格式：ISO 8601格式

### 日期格式
- API请求日期格式：YYYYMMDD（如20241108）
- 也支持YYYY-MM-DD格式（如2024-11-08）

### 响应格式
所有接口统一返回格式：
```json
{
  "code": 0,           // 0=成功, -1=失败
  "message": "success", // 提示信息
  "data": {}           // 数据内容
}
```

## 注意事项

1. **必须配置环境变量**：在使用本技能前，必须先配置 `TDX_API_URL` 环境变量
2. **股票代码格式**：股票代码必须为6位数字，如000001（平安银行）、600519（贵州茅台）
3. **批量查询限制**：批量获取行情一次最多查询50只股票
4. **数据回退机制**：分时数据查询时，如果指定日期无数据，会自动回退至最近一个有交易数据的工作日
5. **K线复权说明**：日/周/月K线默认返回同花顺前复权数据
6. **非交易时段**：非交易时段查询可能返回最新的收盘数据
7. **任务管理**：数据入库任务在后台异步执行，需要通过任务管理接口查询状态
8. **数据量控制**：全量数据较大，建议配合limit参数控制响应大小
9. **交易日查询**：交易日查询会返回前后若干个最近的交易日信息
10. **错误处理**：所有接口都有完善的错误处理机制，返回详细的错误信息

## 常用股票代码

### 蓝筹股
- 000001 - 平安银行
- 600519 - 贵州茅台
- 601318 - 中国平安
- 000858 - 五粮液
- 600036 - 招商银行

### 科技股
- 000333 - 美的集团
- 002415 - 海康威视
- 300750 - 宁德时代
- 688981 - 中芯国际

### 指数代码
- sh000001 - 上证指数
- sz399001 - 深证成指
- sz399006 - 创业板指
- sh000300 - 沪深300
- sz399905 - 中证500

## 技术支持

如有问题，请参考技术文档或联系技术支持。