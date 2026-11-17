# 量化 / 期货经典策略库（中文解读 + 回测模板 + 参数说明）

> 说明：以下策略原理均为**公开方法论**，本文用中文重写解读并附文献出处，**不摘录任何受版权保护的原文**。回测模板基于 `pandas`，数据可由配套 MCP `get_price_history` 取数后传入 `df[['date','open','high','low','close','volume']]`。

---

## 1. 双均线交叉（Moving Average Crossover）

**原理（中文）**：用两条不同周期的移动平均线捕捉趋势。短周期均线上穿长周期均线（金叉）→ 做多；下穿（死叉）→ 做空/平仓。本质是最基础的趋势跟踪。

**适用市场**：股票、期货、加密货币；在**单边趋势市**有效，在震荡市会反复止损。

**回测模板**
```python
def ma_crossover(df, short=5, long=20):
    df = df.copy()
    df['ma_s'] = df['close'].rolling(short).mean()
    df['ma_l'] = df['close'].rolling(long).mean()
    df['signal'] = 0
    df.loc[df['ma_s'] > df['ma_l'], 'signal'] = 1     # 金叉做多
    df.loc[df['ma_s'] < df['ma_l'], 'signal'] = -1    # 死叉做空
    df['position'] = df['signal'].shift(1).fillna(0)
    df['ret'] = df['close'].pct_change()
    df['strat'] = df['position'] * df['ret']
    return df[['close', 'ma_s', 'ma_l', 'signal', 'strat']]
```

**参数说明**
- `short`（短周期）：5–20 日，越小越灵敏、交易越频繁、滑点成本越高。
- `long`（长周期）：20–200 日，决定趋势长度；常见短长比 1:4 ~ 1:10。
- 调参建议：先用 (5,20) 或 (10,50) 基准，再用品种波动率缩放；**严防参数过拟合**（做样本外检验）。

**文献出处**：Murphy, J. (1999) *Technical Analysis of the Financial Markets* — 移动平均章；Kaufman, P. (2013) *Trading Systems and Methods* — 均线系统评估。

---

## 2. 海龟交易法则（Turtle Trading）

**原理（中文）**：Richard Dennis 公开的趋势突破系统。价格突破**N 日最高价**入场做多、跌破 **N 日最低价**出场；用 **ATR（真实波幅）** 计算头寸规模与止损距离，让每笔交易风险恒定（约 1% 账户）。

**适用市场**：期货、外汇、指数；强趋势品种收益高，震荡市回撤大。

**回测模板（简化版）**
```python
def turtle(df, entry=20, exit_n=10, atr_n=20):
    df = df.copy()
    df['hh'] = df['high'].rolling(entry).max().shift(1)   # 入场通道
    df['ll'] = df['low'].rolling(exit_n).min().shift(1)    # 出场通道
    df['tr'] = (df['high'] - df['low']).rolling(atr_n).mean()  # 简化 ATR
    df['signal'] = 0
    df.loc[df['close'] > df['hh'], 'signal'] = 1
    df.loc[df['close'] < df['ll'], 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    return df
```

**参数说明**
- `entry`：入场通道 20（系统1）或 55（系统2）；越长信号越少越稳健。
- `exit_n`：出场通道 10（比入场短，利于锁定利润）。
- `atr_n`：20；头寸单位 = 1% 账户资金 / (N × 每点价值)，N 即 ATR。
- 调参建议：海龟原版参数已较鲁棒，修改需严格样本外验证；可加"加仓（ pyramiding ）"逻辑。

**文献出处**：Faith, C. (2007) *Way of the Turtle* — Dennis 实验与完整规则；原始《Turtle Trading Rules》为公开文献。

---

## 3. 布林带均值回归（Bollinger Band Mean Reversion）

**原理（中文）**：价格在布林带上/下轨之间波动，触及下轨视为超卖→做多，触及上轨视为超买→做空，回归中轨平仓。适合**均值回复（震荡）**环境。

**适用市场**：低趋势、均值回复品种（部分商品期货、ETF、利差）。

**回测模板**
```python
def bollinger_reversion(df, period=20, k=2):
    df = df.copy()
    mid = df['close'].rolling(period).mean()
    std = df['close'].rolling(period).std()
    df['upper'] = mid + k * std
    df['lower'] = mid - k * std
    df['signal'] = 0
    df.loc[df['close'] < df['lower'], 'signal'] = 1   # 触下轨做多
    df.loc[df['close'] > df['upper'], 'signal'] = -1  # 触上轨做空
    df['position'] = df['signal'].shift(1).fillna(0)
    return df
```

**参数说明**
- `period`：20（默认）；越短越敏感、交易越频繁。
- `k`（标准差倍数）：1.5–2.5，常用 2；k 越大信号越少。
- 调参建议：配合"带宽（bandwidth）收窄"过滤横盘；趋势市禁用此策略。

**文献出处**：Bollinger, J. (2002) *Bollinger on Bollinger Bands* — 带宽与回归逻辑。

---

## 4. 动量突破（Momentum / Time-Series Momentum）

**原理（中文）**：过去一段时间收益为正的资产未来短期往往延续（动量效应）。用过去 N 日收益率符号决定多空，或价格创 N 日新高入场。

**适用市场**：股票、期货、加密货币；**中期动量（3–12 个月）** 学术证据最强。

**回测模板**
```python
def momentum(df, window=90):
    df = df.copy()
    df['mom'] = df['close'].pct_change(window)
    df['signal'] = 0
    df.loc[df['mom'] > 0, 'signal'] = 1
    df.loc[df['mom'] < 0, 'signal'] = -1
    df['position'] = df['signal'].shift(1).fillna(0)
    return df
```

**参数说明**
- `window`：学术常用 6–12 个月（约 126–252 交易日）；短期（数日）常出现反转而非动量，需区分。
- 调参建议：可改为"横截面动量"（买最强卖最弱一组），降低系统性风险。

**文献出处**：Jegadeesh & Titman (1993) *Returns to Buying Winners and Selling Losers* — 动量效应经典；Moskowitz, Ooi & Pedersen (2012) *Time Series Momentum*。

---

## 5. 跨期套利（Calendar Spread，期货特有）

**原理（中文）**：同一品种不同到期月份的合约，其价差（近月 − 远月）围绕均值波动。价差 z-score 极端时反向建仓（价差过高→空近月多远月，反之反之），回归平仓。属**统计套利**。

**适用市场**：流动性好的商品期货近远月（如沪铜、原油、豆粕）。

**回测模板**
```python
def calendar_spread(near, far, window=20, z=2):
    spread = near['close'] - far['close']
    zscore = (spread - spread.rolling(window).mean()) / spread.rolling(window).std()
    # 价差极度偏高→空近月多远月(-1)；极低→反(1)
    signal = -((zscore > z).astype(int) - (zscore < -z).astype(int))
    return zscore, signal
```

**参数说明**
- `window`：20–60 日；决定均值与波动基准。
- `z`：1.5–2.5；越大信号越少。
- 关键风险：**展期（rollover）** 与基差结构（contango 正套 / backwardation 反套）；须处理合约换月。

**文献出处**：Hull, J. (2017) *Options, Futures and Other Derivatives* — 价差与套利章。

---

## 6. 配对交易（Pair Trading / Statistical Arbitrage）

**原理（中文）**：选取两高度相关（协整）品种，其价格比/价差平稳。z-score 极端时做空"贵方"、做多"便宜方"，回归平仓。与跨期套利类似但跨品种。

**适用市场**：同行业股票对、相关期货、ETF 与其成分股。

**回测模板**
```python
def pair_trade(a, b, window=30, z=2):
    ratio = a['close'] / b['close']
    zscore = (ratio - ratio.rolling(window).mean()) / ratio.rolling(window).std()
    signal_a = -(zscore > z).astype(int) + (zscore < -z).astype(int)
    return zscore, signal_a
```

**参数说明**
- `window`：20–60；决定均值基准。
- `z`：2（常用）；结合"半衰期"确定持仓周期。
- 前置条件：必须做**协整检验（CADF / Johansen）** 确认价差平稳，否则伪套利。

**文献出处**：Gatev, Goetzmann & Rouwenhorst (2006) *Pairs Trading: Performance of a Relative-Value Arbitrage Rule*；Chan, E. (2008) *Quantitative Trading* — 配对交易章。
