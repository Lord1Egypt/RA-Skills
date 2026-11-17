# 策略历史回撤分析方法论

> 当用户问"某策略在某段时间为什么跌得这么惨"时使用此工作流。
> 典型触发：用户给出策略ID/URL + 时间段，要求分析下跌原因和持仓变化。

## 1. 获取策略基本信息

```sql
SELECT * FROM strategy_information WHERE strategy_id = ?
```

关键字段：
- `strategy_table` — 持仓数据表名（格式：`strategy_{name}_{id}`）
- `benchmark` — 对标指数
- `how_to_trade` — 调仓规则（日频/周频/月频）
- `start_date` — 回测起始时间

## 2. 查询时间段内全部调仓记录

```sql
SELECT DISTINCT trade_date FROM {strategy_table}
WHERE trade_date >= ? AND trade_date <= ?
ORDER BY trade_date ASC
```

统计总交易日数，确认调仓频率是否符合 `how_to_trade` 描述。

## 3. 月度持仓快照（核心）

取每月最后一个交易日的持仓作为月度快照：

```javascript
// 对于每个月，查询 <= 月末日期 的最新一条记录
SELECT trade_date, trading_info FROM {table}
WHERE trade_date <= ?
ORDER BY trade_date DESC LIMIT 1
```

⚠️ `trading_info` 在 mysql2 中返回为 Object 而非 String，需判断类型：
```javascript
let holdings = row.trading_info;
if (typeof holdings === 'string') {
    holdings = JSON.parse(holdings);
}
// 直接使用 Object.keys(holdings) 获取持仓代码列表
```

## 4. 换手率分析

对相邻两个月度快照计算换手率：
- 新进 = 月末持仓 - 月初持仓
- 清仓 = 月初持仓 - 月末持仓
- 保留 = 交集
- 换手率 = (新进数 + 清仓数) / max(月初持仓数, 月末持仓数)

**高换手率 + 下跌 = 交易成本侵蚀 + 频繁止损割肉**

## 5. 持仓数量趋势

逐日统计持仓ETF/股票数量，计算：
- 每月平均持仓数
- 最少/最多持仓日
- 持仓数变化趋势（是否在下跌期间集中度上升）

**持仓数下降 + 净值下跌 = 策略在用减仓应对亏损，而非分散风险**

## 6. ETF/个股被持有天数统计

遍历时间段内每一期持仓，统计每个标的被持有的天数：
- 持有时间最长的标的是否也是跌幅最大的？
- 是否存在"长期持有亏损标的"的模式？

## 7. 标的价格走势关联

用东方财富 API 获取每个标的在分析时段的涨跌幅和最大回撤：

```
# ETF/股票名称
https://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f57,f58

# 历史K线（日频前复权）
https://push2his.eastmoney.com/api/qt/stock/kline/get?secid={market}.{code}
  &fields1=f1,f2,f3&fields2=f51,f52,f53,f54,f55,f56
  &klt=101&fqt=1&beg={YYYYMMDD}&end={YYYYMMDD}
```

secid 前缀：沪市 `1.`，深市 `0.`

K线格式：`date,open,close,high,low,volume`

⚠️ 部分请求会失败（`Remote end closed connection`），需 `time.sleep(0.5-1)` + 重试

## 8. 回撤原因归因框架

常见回撤原因（按优先级排查）：

| 原因 | 诊断指标 |
|------|---------|
| **重仓标的暴跌** | 持有时间最长的标的跌幅最大？最大回撤多少？ |
| **调仓频率过高** | 日频/周频策略？月度换手率 > 50%？交易成本年化 > 10%？ |
| **持仓集中度上升** | 持仓数在下跌期间是否显著减少？单只权重是否 > 30%？ |
| **信号失效环境** | 策略类型（动量/趋势/均值回归）与市场环境（震荡/单边）是否错配？ |
| **时点不匹配** | 策略起始日期是否恰好在市场顶部？ |

## 9. 报告输出格式

```
## 策略回撤分析报告

### 基本信息（策略名/ID/调仓频率/对标/分析时段）
### 持仓数量变化趋势（月度表 + 持仓数变化图）
### 月度持仓快照（每月末持仓ETF/股票列表）
### 月度换手率分析（新进/清仓/保留 + 换手率%）
### 被持有天数排名（标的代码 + 天数 + 期间涨跌幅 + 最大回撤）
### 回撤原因归因（按框架逐项分析）
### 关键结论与改进建议
### 免责声明
```

## 实战案例

2026-07-01 分析 stgetf0001（华夏基金ETF-信号匹配轮动策略）2023.06-2024.02 回撤：
- 策略为日频ETF轮动，6月27日启动恰好踩在A股顶部
- 持仓数从9.5只月均→1.5只月均，极端集中
- 月度换手率67%-150%，交易成本侵蚀严重
- 被持有最久的游戏ETF(90天,-31.8%)和云计算ETF(76天,-21.5%)恰为最大跌幅标的
- 结论：日频调仓在震荡下跌市中被反复打脸，持仓集中度与下跌形成正反馈螺旋
