---
name: BitSoul-Stock-Skill
description: 计算股票或组合的年化收益率，支持按股票代码+日期范围自动拉取K线计算，也支持直接输入初始/最终资金计算，输出年化收益率、总收益率、最大回撤、夏普比率等完整绩效报告
metadata:
  openclaw:
    emoji: "📊"
    homepage: https://www.aicodingyard.com
    requires:
      env:
        - BITSOUL_TOKEN
      bins:
        - python3
    optional:
      env:
        - BITSOUL_TOKEN_ENV_FILE
        - BITSOUL_CACHE_DIR
      pythonPackages:
        - pandas
        - numpy
        - requests
        - sqlalchemy
      network:
        - info.aicodingyard.com
    primaryEnv: BITSOUL_TOKEN
---

# 年化收益率计算 Skill

帮助用户计算股票或投资组合的年化收益率，支持两种模式：
1. **股票模式**：输入股票代码 + 日期区间，自动拉取K线数据并计算
2. **资金模式**：直接输入初始资金、最终资金、持有天数，快速计算

## Token 配置

本 skill 需要有效的 `BITSOUL_TOKEN` 才能访问股票数据。
token 可前往 <https://www.aicodingyard.com> 免费注册申请。

## 触发场景

当用户说以下内容时，触发本 skill：
- "帮我算一下XX股票的年化"
- "计算年化收益率"
- "我持有XXX，买入价YYY，现在ZZZ，年化多少"
- "从X日到Y日的年化"
- "年化收益是多少"
- "算算这个策略年化怎么样"

## 运行逻辑

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scripts'))
from stock_api import StockApi

api = StockApi()
```

### 模式一：按股票代码 + 日期区间计算

适用场景：用户给出了股票代码、买入日期、卖出（或当前）日期。

```python
# 获取区间内收盘价序列，构建权益曲线
klines = api.get_daily_kline([code], start_date, end_date)

# 以第一日收盘价为基准，构建等比权益曲线
initial_price = klines[0].close
equity_curve = [k.close / initial_price * initial_cash for k in klines]

# 计算总收益率
total_return = api.get_total_return(equity_curve[0], equity_curve[-1])

# 计算交易天数
trading_days = len(equity_curve) - 1

# 计算年化收益率（核心接口）
annualized_return = api.get_annualized_return(total_return, trading_days)

# 计算最大回撤
max_drawdown_pct = api.get_max_drawdown_pct(equity_curve)

# 计算夏普比率
sharpe = api.get_sharpe_ratio(equity_curve)
```

### 模式二：直接输入资金数据计算

适用场景：用户直接提供了初始资金/价格、最终资金/价格、持有天数。

```python
# 用户提供 initial_value, final_value, days
total_return = api.get_total_return(initial_value, final_value)
annualized_return = api.get_annualized_return(total_return, days)
```

### 模式三：完整回测结果计算（最全面）

适用场景：用户要求完整的绩效报告，或提供了多笔交易记录。

```python
# 如果有完整权益曲线和交易记录
report = api.calculate_metrics(equity_curve, trades, initial_cash, trading_days)
# report 包含: annualized_return_pct, total_return_pct, max_drawdown_pct, sharpe_ratio, calmar_ratio 等
```

## 输出格式（强制执行）

计算完成后，必须按以下格式输出报告，禁止简化：

```
📊 年化收益率分析报告
════════════════════════════════
股票/策略：{名称或描述}
分析区间：{start_date} ~ {end_date}（{trading_days} 个交易日）

┌─────────────────────┬──────────────┐
│ 指标                │ 数值         │
├─────────────────────┼──────────────┤
│ 年化收益率          │ XX.XX%       │
│ 总收益率            │ XX.XX%       │
│ 最大回撤            │ -XX.XX%      │
│ 夏普比率            │ X.XX         │
└─────────────────────┴──────────────┘

结论：{根据年化收益率给出简短评价，如：年化收益率 XX%，{高于/低于} 市场平均水平（约8-12%），{表现优秀/表现一般/表现较差}。}

⚠️ 免责声明：本结果仅供参考，不构成投资建议。
```

## 注意事项

- **股票显示格式**：输出股票代码时，必须同时附上股票名称，使用 `api.get_symbol_basic_infomation(code).name` 获取，格式如 `600519.SH（贵州茅台）`
- **年化收益率公式**：`(1 + total_return) ^ (252 / trading_days) - 1`，其中 252 为年交易日数，直接调用 `api.get_annualized_return()` 即可，禁止自己实现公式
- **数据不足处理**：如果交易天数少于 5 个交易日，提示用户数据不足，无法计算有意义的年化收益率
- **收益率参照**：年化收益率超过 20% 为优秀，10-20% 为良好，0-10% 为一般，负值为亏损

## 示例请求

- `帮我算一下贵州茅台从2025年1月到2025年12月的年化收益率`
- `我在2025年3月1日以50元买入000001.SZ，现在涨到60元，持有了180天，年化多少？`
- `计算一下工业富联最近一年的年化收益率和最大回撤`
- `初始资金100万，现在变成了120万，持有了200个交易日，年化是多少`
