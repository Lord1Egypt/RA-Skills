# 股票数据 API 文档

## 新浪财经 API（免费、无需 Key）

### 实时行情接口

**URL:** `http://hq.sinajs.cn/s={symbol}`

**支持市场:**
- A 股：`sh600519`, `sz000001`, `sz300750`
- 港股：`hk00700`, `hk09988`
- 美股：`gb_aapl`, `gb_msft`, `gb_tsla`
- 基金：`sh510000`, `sz159915`
- 期货：`hf_CL` (原油), `hf_GC` (黄金)

### 返回数据格式

```
var hq_str_sh600519="贵州茅台，1500.00,1480.00,1490.00,1510.00,1495.00,1498.00,1499.00,100000,150000000,..."
```

**字段说明（逗号分隔）：**

| 索引 | 字段 | 说明 |
|------|------|------|
| 0 | name | 股票名称 |
| 1 | open | 今日开盘价 |
| 2 | prev_close | 昨日收盘价 |
| 3 | current | 当前价格 |
| 4 | high | 今日最高价 |
| 5 | low | 今日最低价 |
| 6 | bid | 买入价（委买） |
| 7 | ask | 卖出价（委卖） |
| 8 | volume | 成交量（股） |
| 9 | turnover | 成交额（元） |
| 10-19 | bid_data | 买一至买五（价格和数量） |
| 20-29 | ask_data | 卖一至卖五（价格和数量） |
| 30 | date | 日期 (YYYY-MM-DD) |
| 31 | time | 时间 (HH:MM:SS) |

### 买卖盘口数据

```
字段 10: 买一价格
字段 11: 买一数量
字段 12: 买二价格
字段 13: 买二数量
...
字段 18: 买五价格
字段 19: 买五数量
字段 20: 卖一价格
字段 21: 卖一数量
...
字段 28: 卖五价格
字段 29: 卖五数量
```

### 代码示例

**Python:**
```python
import urllib.request

symbol = "sh600519"
url = f"http://hq.sinajs.cn/s={symbol}"

with urllib.request.urlopen(url) as response:
    content = response.read().decode('gbk')
    
# 解析
import re
match = re.search(r'="([^"]+)"', content)
data = match.group(1).split(',')

name = data[0]
current = float(data[3])
change_pct = (float(data[3]) - float(data[2])) / float(data[2]) * 100
```

**cURL:**
```bash
curl "http://hq.sinajs.cn/s=sh600519"
```

### 交易时间

| 市场 | 交易时间 (北京时间) |
|------|-------------------|
| A 股 | 09:30-11:30, 13:00-15:00 |
| 港股 | 09:30-12:00, 13:00-16:00 |
| 美股 | 21:30-04:00 (冬令时 22:30-05:00) |

**非交易时间:** 返回最近收盘价

### 注意事项

1. **编码:** 返回数据为 GBK 编码，需要转换
2. **延迟:** A 股实时，港股/美股延迟 15 分钟
3. **限流:** 避免高频请求（建议间隔>1 秒）
4. **稳定性:** 免费 API，不保证 100% 可用

---

## 其他免费数据源

### 东方财富 API

**实时行情:**
```
http://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45...
```

**K 线数据:**
```
http://push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{code}&klt=101&fqt=1...
```

### 腾讯财经 API

**实时行情:**
```
http://qt.gtimg.cn/q={symbol}
```

### Yahoo Finance (美股)

**API:** `https://query1.finance.yahoo.com/v8/finance/chart/{symbol}`

需要处理 JSON 响应，数据较全但速度较慢。

---

## 推荐实践

1. **首选新浪 API** - 速度快、稳定、支持全市场
2. **添加重试机制** - 网络波动时重试 2-3 次
3. **本地缓存** - 相同股票 1 分钟内不重复请求
4. **错误处理** - 优雅降级，显示友好提示
