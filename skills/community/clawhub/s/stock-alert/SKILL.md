---
name: stock-alert
description: Real-time stock query, portfolio analysis, and conversational threshold alerts for A-shares/HK/US stocks. No API key needed.
version: 1.3.0
license: MIT-0
metadata:
  openclaw:
    emoji: 📈
    requires:
      bins: []
      env: []
---

# Stock Alert

查股价、分析持仓、设预警。A 股 / 港股 / 美股。

**核心差异**：每次聊股票时自动扫一遍监测列表，有触发直接提醒。不用专门开 app。

---

## Triggers

- "查 [股票名/代码]"
- "分析 / 看看我的 / 持仓"
- "盯着 / 监控 / 帮我看着 [股票名]"
- "检查预警"
- "行情 / 大盘 / 涨跌"
- 对话中出现股票代码或知名股票名

---

## Behavioral Rules

### 1. 查股价

用户说 "查茅台" "腾讯多少了" "AAPL":

```
python3 scripts/stock_query.py <code1> [code2] ...
```

返回后格式化成：

```
🍶 贵州茅台 (sh600519)
├─ 当前: ¥1850.00
├─ 开盘: ¥1820.00 / 昨收: ¥1845.00
├─ 最高: ¥1860.00 / 最低: ¥1815.00
├─ 涨跌: +5.00 (+0.27%)
```

→ **查完后自动做两件事**：
1. 顺带跑一次 `stock_analysis.py`，报一句 "茅台在日内区间 25% 位置（偏低）"
2. 读取 `~/.stock_alert_config.json`，拉行情比阈值，有触发就提醒

### 2. 设预警

用户说 "帮我盯着茅台" "茅台跌破1500提醒" "监控腾讯":

**不要直接跑命令。先确认条件：**

```
你：监控茅台设什么条件？
① 价格低于 ___ 时提醒
② 价格高于 ___ 时提醒
③ 涨跌幅超过 ___% 时提醒
④ 以上都要（可以都设）
```

用户给条件后，调：
```
scripts/stock_monitor.py add <code> <name> [price_high] [price_low] [change_pct]
```
空缺的参数传 `""`。

**设完后主动提议定时任务：**

```
已记下了。要不要我再设个定时任务，每半小时自动检查一次？
这样你不问股票的时候我也会在后台盯着。
```

用户答应 → 检查 `schedule_job` 工具是否可用：
- 有 → 设 `*/30 * * * *`，prompt 描述检查 + 写 `~/.stock_alerts_pending.json`
- 无 → "需要先装 opencode-scheduler 插件才支持后台定时检查"

### 3. 检查预警

用户说 "检查预警" "有触发吗":

```
python3 scripts/stock_monitor.py check
```

有预警 → 逐条报告触发条件
无预警 → "一切正常，当前 X 只监测股均未触发"

→ **每次回答完，再顺口问一句**：

```
要不要调整一下条件？或者加新的监测？
```

### 4. 分析持仓

用户说 "看看我的" "分析一下":

先看 `~/.stock_alert_config.json` 有没有监测股。没有 → "你还没设监测股，要我现在帮你盯哪些？"

有 → `scripts/stock_analysis.py <codes...>`，输出：

```
📊 你的持仓 (3只)
📈 涨跌: 2涨 1跌
🥇 腾讯 +2.3%
🥉 茅台 -0.8%

⚠️ 接近极值：茅台在日内低位 12% 位置
```

→ **末尾同样自动比一次预警** + 建议下一步

### 5. 定时任务的回执

如果 `~/.stock_alerts_pending.json` 存在，**每次回任何股票问题前先读它**：

```
# 读取 pending 预警
cat ~/.stock_alerts_pending.json | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f\"⚠️ {a['name']}({a['current']}) — {'; '.join(a['triggers'])}\") for a in d.get('pending',[])]"
```

有内容 → 回答开头先提醒：
```
📢 定时检查发现预警！
· 茅台 ¥1480 — 低于你设的 ¥1500 阈值
· 腾讯 -5.3% — 超过你设的 5% 阈值
```

然后删掉文件（`rm ~/.stock_alerts_pending.json`），再继续回答用户问题。

---

## Commands Reference

### Query
```
python3 scripts/stock_query.py sh600519 hk00700 usAAPL
```

### Analysis
```
python3 scripts/stock_analysis.py sh600519 hk00700 sz000001
```

### Monitor CRUD
```
# 添加 (code name price_high price_low change_pct, 跳过的不传)
python3 scripts/stock_monitor.py add 600519 茅台 2000 1500 5

# 列表
python3 scripts/stock_monitor.py list

# 删除
python3 scripts/stock_monitor.py remove 600519

# 手动检查 (调试用)
python3 scripts/stock_monitor.py check
```

### Code format

| Market | 格式 |
|--------|------|
| 沪市 | `600XXX` 或 `sh600XXX` |
| 深市 | `000XXX` / `300XXX` 或 `sz0XXX` |
| 港股 | `00XXX` 或 `hk00XXX` |
| 美股 | `SYMBOL` 或 `usSYMBOL` |

---

## 对话示例

```
你：帮我盯着腾讯
AI：设什么条件？
    ① 价格低于 ___ 时提醒
    ② 价格高于 ___ 时提醒
    ③ 涨跌幅超过 ___% 时提醒
你：低于300，高于500
AI：已记录：腾讯 (hk00700) — 低于300 / 高于500 时提醒。
    要不要设个定时任务每半小时自动检查？
你：好
AI：已设定时任务，每30分钟检查一次。下次聊股票时我会告诉你是否有预警。
```

```
你：查茅台
AI：🍶 贵州茅台 ¥1490 (-0.5%)

    ⚠️ 预警：茅台 ¥1490，低于你设的 ¥1500 阈值
    
    要不要调整条件或加新的监测？
```

---

## Config

`~/.stock_alert_config.json`:
```json
[
  {"code": "sh600519", "name": "贵州茅台", "price_low": 1500, "price_high": 2000}
]
```
