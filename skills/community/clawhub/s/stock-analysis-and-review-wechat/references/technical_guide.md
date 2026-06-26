# 股市复盘技术参考

## 数据源详解

### 1. 腾讯财经 API (推荐)

**接口地址**: `https://qt.gtimg.cn/q={codes}`

**优点**:
- 无需认证，直接访问
- 实时更新
- 稳定可靠
- 支持A股、港股、美股

**编码**: GBK (注意解码)

**返回字段说明**:

```
v_sh600919="1~江苏银行~600919~10.78~10.70~10.72~1234567~...";

字段索引对应表:
0: 未知
1: 股票名称
2: 股票代码
3: 当前价格
4: 昨日收盘价
5: 今日开盘价
6: 成交量(手)
7: 外盘
8: 内盘
9-28: 买卖盘五档价格和数量
29: 最近逐笔成交
30: 时间
31: 涨跌
32: 涨跌率
33: 最高价
34: 最低价
35: 价格/成交量(手)/成交额
36: 成交量(手)
37: 成交额(万)
38: 换手率
39: 市盈率
40: 未知
41: 最高价
42: 最低价
43: 振幅
44: 流通市值
45: 总市值
46: 市净率
47: 涨停价
48: 跌停价
```

**代码前缀规则**:

| 市场 | 前缀 | 示例 |
|------|------|------|
| 上海A股 | sh | sh600919 |
| 深圳A股 | sz | sz000001 |
| 上海ETF | sh | sh510310 |
| 深圳ETF | sz | sz159819 |
| 港股 | hk | hk00700 |
| 美股 | 无 | AAPL |

### 2. 新浪财经 API (备选)

**接口地址**: `https://hq.sinajs.cn/list={codes}`

**优点**:
- 历史悠久，广泛使用
- 数据全面

**缺点**:
- 偶尔不稳定
- 需要Referer头

**返回格式**:
```javascript
var hq_str_sh600919="江苏银行,10.78,10.70,10.72...";
```

## 持仓管理最佳实践

### 1. 数据结构设计

```json
{
  "portfolio": [
    {
      "code": "sh600919",
      "name": "江苏银行",
      "qty": 700,
      "cost": 8.99,
      "target_sell": 11.50,
      "target_buy": 8.00,
      "category": "银行股"
    }
  ],
  "strategy": {
    "stop_loss_pct": -10,
    "take_profit_pct": 20,
    "add_position_pct": -3
  }
}
```

### 2. 建仓策略模板

**分步建仓法**:
```
首次建仓: 计划仓位的 30%
跌3%加仓: 计划仓位的 30%
跌8%加仓: 计划仓位的 40% (完成建仓)
```

**金字塔加仓法**:
```
首次建仓: 500元
加仓1: 500元 (跌3%)
加仓2: 1000元 (跌8%)
```

### 3. 止盈止损策略

**移动止盈法**:
```
盈利20%时，设置回撤10%止盈
盈利30%时，设置回撤15%止盈
```

**固定比例法**:
```
止损线: -10%
止盈线: +20%
```

## 常见错误处理

### 1. 数据解析错误

```python
# 错误示例
price = float(fields[3])  # 如果fields[3]为空会报错

# 正确做法
price = float(fields[3]) if fields[3] else 0.0
try:
    price = float(fields[3])
except ValueError:
    price = 0.0
```

### 2. 网络请求错误

```python
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
session.mount('http://', HTTPAdapter(max_retries=retry))
session.mount('https://', HTTPAdapter(max_retries=retry))

try:
    resp = session.get(url, timeout=10)
except requests.RequestException as e:
    print(f"请求失败: {e}")
```

### 3. 时区处理

```python
from datetime import datetime
import pytz

# 设置中国时区
china_tz = pytz.timezone('Asia/Shanghai')
now = datetime.now(china_tz)

# 判断是否在交易时间
def is_trading_hours():
    now = datetime.now(china_tz)
    if now.weekday() >= 5:  # 周末
        return False
    time_str = now.strftime('%H:%M')
    return ('09:30' <= time_str <= '11:30') or ('13:00' <= time_str <= '15:00')
```

## 定时任务配置

### OpenClaw Cron 配置

```bash
# 早盘监控 (9:30, 10:30, 11:30)
openclaw cron add \
  --name stock-monitor-am \
  --cron "30 9,10,11 * * 1-5" \
  --agent main \
  --message "执行早盘监控任务" \
  --description "工作日早盘监控"

# 午盘监控 (13:00, 14:00, 14:30)
openclaw cron add \
  --name stock-monitor-pm \
  --cron "0 13,14 * * 1-5" \
  --cron "30 14 * * 1-5" \
  --agent main \
  --message "执行午盘监控任务" \
  --description "工作日午盘监控"

# 收盘复盘 (15:05)
openclaw cron add \
  --name stock-daily-review \
  --cron "5 15 * * 1-5" \
  --agent main \
  --message "执行收盘复盘任务" \
  --description "工作日收盘复盘"
```

### Cron 表达式说明

```
* * * * *
| | | | |
| | | | +----- 星期 (0-7, 0和7都是周日)
| | | +------- 月份 (1-12)
| | +--------- 日期 (1-31)
| +----------- 小时 (0-23)
+------------- 分钟 (0-59)

特殊字符:
* : 任意值
, : 列表 (1,2,3)
- : 范围 (1-5)
/ : 步长 */10
```

## Markdown 报告模板

### 标准复盘报告结构

```markdown
# YYYY-MM-DD 股票复盘报告

## 📊 大盘概览
- 上证指数
- 深证成指
- 创业板指
- 成交额

## 💼 持仓盘点
| 标的 | 数量 | 成本 | 现价 | 盈亏 | 收益率 | 状态 |

## 🚨 预警分析
- 触及止盈线的标的
- 触及加仓线的标的
- 亏损超10%的标的

## 📰 消息面
### 国际消息
### 国内政策
### 行业动态

## 💡 策略建议
### 明日计划
### 风险提示

---
*报告时间: YYYY-MM-DD HH:MM*
```

## 数据存储建议

### 1. 持仓数据存储

推荐使用JSON格式存储持仓信息：

```json
{
  "last_updated": "2026-04-11",
  "positions": [
    {
      "code": "sh600919",
      "name": "江苏银行",
      "qty": 700,
      "cost": 8.99,
      "category": "银行股",
      "strategy": {
        "target_sell": 11.50,
        "target_buy": 8.00,
        "stop_loss": 8.10
      }
    }
  ],
  "cash": 10000,
  "total_value": 50000
}
```

### 2. 交易记录存储

```json
{
  "transactions": [
    {
      "date": "2026-04-10",
      "code": "sh600919",
      "type": "buy",
      "qty": 100,
      "price": 10.50,
      "amount": 1050
    }
  ]
}
```

### 3. MEMORY.md 更新格式

```markdown
## 💹 持仓状态（YYYY-MM-DD 更新）
| 标的 | 持仓 | 成本 | 现价 | 盈亏 | 收益率 |

### 关键监控点位
- 标的A: 止盈线¥X.XX / 加仓线¥X.XX
- 标的B: 止盈线¥X.XX / 加仓线¥X.XX

### 近期交易
| 日期 | 标的 | 操作 | 数量 | 价格 | 备注 |
```
