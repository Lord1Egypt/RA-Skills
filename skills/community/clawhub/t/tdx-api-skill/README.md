# TDX股票查询技能

基于TDX API的股票数据查询技能，提供全面的A股市场数据查询功能。

## 功能特性

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

## 安装配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API地址

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的TDX API地址：

```
TDX_API_URL=http://your-api-domain.com
```

### 3. 验证配置

运行测试脚本验证配置是否正确：

```bash
python main.py
```

## 快速开始

### 基础使用

```python
from main import TDXStockQuery

# 初始化查询对象
stock_query = TDXStockQuery()

# 获取股票实时行情
result = stock_query.get_quote(['000001', '600519'])
print(result)

# 获取K线数据
result = stock_query.get_kline('000001', 'day')
print(result)

# 搜索股票
result = stock_query.search_stock('平安')
print(result)
```

### 高级使用

```python
# 批量获取行情
result = stock_query.batch_quote(['000001', '600519', '601318'])

# 获取历史K线
result = stock_query.get_kline_history('000001', 'day', limit=30)

# 创建数据入库任务
result = stock_query.create_pull_kline_task(
    codes=['000001', '600519'],
    tables=['day', 'week'],
    limit=2
)

# 查询任务状态
task_id = result['data']['task_id']
task_detail = stock_query.get_task_detail(task_id)
```

## API接口列表

### 基础接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| get_quote | GET | 五档行情 |
| get_kline | GET | K线数据 |
| get_minute | GET | 分时数据 |
| get_trade | GET | 分时成交 |
| search_stock | GET | 搜索股票 |
| get_stock_info | GET | 综合信息 |

### 扩展接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| get_codes | GET | 股票代码列表 |
| batch_quote | POST | 批量行情 |
| get_kline_history | GET | 历史K线 |
| get_index | GET | 指数数据 |
| get_server_status | GET | 服务状态 |
| health_check | GET | 健康检查 |

### 任务管理接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| create_pull_kline_task | POST | 创建K线入库任务 |
| create_pull_trade_task | POST | 创建分时成交入库任务 |
| get_tasks | GET | 查询任务列表 |
| get_task_detail | GET | 查询任务详情 |
| cancel_task | POST | 取消任务 |

### 高级数据接口

| 接口 | 方法 | 说明 |
|-----|------|------|
| get_etf | GET | ETF列表 |
| get_trade_history | GET | 历史分时成交分页 |
| get_minute_trade_all | GET | 全天分时成交 |
| get_workday | GET | 交易日信息 |
| get_market_count | GET | 市场证券数量 |
| get_stock_codes | GET | 全部股票代码 |
| get_etf_codes | GET | 全部ETF代码 |
| get_kline_all | GET | 股票历史K线全集 |
| get_index_all | GET | 指数历史K线全集 |
| get_trade_history_full | GET | 上市以来分时成交 |
| get_workday_range | GET | 交易日范围 |
| get_income | GET | 收益区间分析 |

## 数据说明

### 价格单位
- 所有价格单位为"厘"（1元 = 1000厘）
- 转换函数：`format_price(price_in_li)`

### 成交量单位
- 成交量单位为"手"（1手 = 100股）
- 转换函数：`format_volume(volume_in_hands)`

### 响应格式
所有接口统一返回格式：
```json
{
  "code": 0,           // 0=成功, -1=失败
  "message": "success", // 提示信息
  "data": {}           // 数据内容
}
```

## 使用示例

### 查询股票实时行情

```python
result = stock_query.get_quote(['000001', '600519'])
if result['code'] == 0:
    for quote in result['data']:
        code = quote['Code']
        price = quote['K']['Close'] / 1000  # 转换为元
        print(f"{code}: {price}元")
```

### 查询K线数据

```python
result = stock_query.get_kline('000001', 'day')
if result['code'] == 0:
    klines = result['data']['List']
    for kline in klines[:5]:  # 最近5天
        date = kline['Time']
        close = kline['Close'] / 1000
        print(f"{date}: {close}元")
```

### 批量获取行情

```python
watchlist = ['000001', '600519', '601318', '000858', '600036']
result = stock_query.batch_quote(watchlist)
if result['code'] == 0:
    for quote in result['data']:
        print(f"{quote['Code']}: {quote['K']['Close']/1000}元")
```

### 创建数据入库任务

```python
# 创建K线入库任务
result = stock_query.create_pull_kline_task(
    codes=['000001', '600519'],
    tables=['day', 'week', 'month'],
    limit=4,
    start_date='2020-01-01'
)

if result['code'] == 0:
    task_id = result['data']['task_id']
    print(f"任务创建成功，任务ID: {task_id}")
    
    # 查询任务状态
    task_detail = stock_query.get_task_detail(task_id)
    print(f"任务状态: {task_detail['data']['status']}")
```

### 查询交易日信息

```python
result = stock_query.get_workday('20241108', count=3)
if result['code'] == 0:
    data = result['data']
    print(f"查询日期: {data['date']['iso']}")
    print(f"是否交易日: {data['is_workday']}")
    print(f"前一个交易日: {data['previous'][0]['iso']}")
    print(f"后一个交易日: {data['next'][0]['iso']}")
```

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

## 注意事项

1. **必须配置环境变量**：使用前必须配置 `TDX_API_URL` 环境变量
2. **股票代码格式**：股票代码必须为6位数字
3. **批量查询限制**：批量获取行情一次最多查询50只股票
4. **数据回退机制**：分时数据查询时，如果指定日期无数据，会自动回退至最近交易日
5. **K线复权说明**：日/周/月K线默认返回同花顺前复权数据
6. **非交易时段**：非交易时段查询可能返回最新的收盘数据
7. **任务管理**：数据入库任务在后台异步执行，需要通过任务管理接口查询状态
8. **数据量控制**：全量数据较大，建议配合limit参数控制响应大小

## 技术支持

如有问题，请参考技术文档或联系技术支持。

## 许可证

MIT License