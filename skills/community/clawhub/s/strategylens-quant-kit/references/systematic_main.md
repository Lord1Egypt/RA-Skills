# 文献深做：期货 / 系统化主线

> **本文件来源**：用户提供的 20 本英文原版文献中，选定的「期货 / 系统化主线」4 本。  
> **处理方法**：中文方法论解读 + 本 Skill **自写**的可运行模板（Python/pandas，用示例数据演示，不依赖网络）+ 参数说明 + 文献出处引用。  
> **版权红线**：所有内容均为本 Skill 用中文重写的方法论概括与自写代码，**不复制任何受版权保护的原文段落**。引用格式一律为 `作者(年份)《书名》`。



---

## 1. Carver《Systematic Trading》(2015) — 系统化期货的仓位与风控内核

### 1.1 核心思想（中文解读）

Carver 的核心是把"交易"拆成**信号（signal）→ 仓位（position）** 两段，并强调用**波动率目标化（volatility targeting）** 统一不同品种的风险尺度：

- **仓位不是按"手数"固定，而是按"想承担多少波动"反推**。目标账户年化波动 σ\*（常见 15%–25%），某品种年化波动为 σ_i，则对其仓位权重 ≈ σ\* / σ_i（再叠加上限与品种层风险预算）。
- **多策略 / 多品种需要风险预算**：账户层把总风险切分给不同策略或品种，避免单一品种主宰组合波动。
- **信号与仓位解耦**：趋势/动量等信号只决定"方向"，波动率目标化决定"大小"，二者正交，便于组合与再平衡。

### 1.2 波动率目标化仓位（自写模板）

逻辑见 `scripts/vol_target_position.py`：

```python
def vol_target_weight(returns, target_vol=0.20, period=252, max_leverage=3.0):
    vol = returns.std() * np.sqrt(period)          # 年化波动
    if vol <= 0:
        return 0.0
    w = target_vol / vol                            # 反推仓位
    return float(np.clip(w, 0, max_leverage))
```

输入某品种的日收益序列，输出应配置的仓位权重（受 `max_leverage` 上限约束）。示范输出：年化波动 0.32 的品种、目标 0.20 时，权重 ≈ 0.62。

### 1.3 关键参数

| 参数             | 含义                     | 常见区间           | 敏感度          |
| -------------- | ---------------------- | -------------- | ------------ |
| `target_vol`   | 账户目标年化波动               | 0.15–0.25      | 越高仓位越大、回撤也越大 |
| `period`       | 年化因子（日=252，小时≈252×6.5） | 252            | 仅影响量纲        |
| `max_leverage` | 单品种仓位上限                | 1.0–5.0（期货常 3+，股票/零售可设低） | 防单一品种爆仓      |
| 再平衡频率          | 多久重算一次权重               | 日/周/月          | 频率越高越贴合目标波动  |

### 1.4 文献引用

Carver, R. (2015). *Systematic Trading*. Harriman House. — 第 5–8 章关于 volatility targeting 与 risk budget 的论述（以本 Skill 概括为准，不摘录原文）。

---

## 2. Carver《Smart Portfolios》(2017) — 组合层资金分配

### 2.1 核心思想（中文解读）

上一本解决"单品种/单策略仓位"，这本解决"账户资金如何在多个策略、多个资产间分配"：

- **风险平价（risk parity）思路**：让每个资产/策略对组合总风险的贡献大致相等，而非等金额配置——波动低的资产自然配更多权重。
- **账户层风险预算**：先定账户总波动目标，再按策略重要性切分，逐层下钻到品种。
- **相关性处理**：高相关资产会放大组合波动，分配时需用协方差而非只看各自波动。

### 2.2 简化风险平价权重（自写模板）

逻辑见 `scripts/risk_parity.py`（**简化对角近似：按波动反比配权**）：

```python
def risk_parity_weights(returns):
    ann_vol = (returns.std() * np.sqrt(252)).replace(0, np.nan)
    inv_vol = 1.0 / ann_vol
    w = inv_vol / inv_vol.sum()
    return w.fillna(0.0)
```

> **说明**：精确等风险贡献(ERC)需迭代求解协方差非对角项、数值较敏感。此处采用文献中最常用的**简化（对角近似）**——按年化波动反比配权（w_i ∝ 1/σ_i）。当资产相关性较低时，该权重非常接近等风险贡献，且永远稳定、权重非负。若要精确 ERC，参考 Carver(2017) 或 Roncalli 的风险预算框架。
>
> 输入多资产日收益矩阵，输出波动越低权重越高的组合权重，可作为组合层资金分配的起点。

### 2.3 关键参数

| 参数     | 含义             | 说明                    |
| ------ | -------------- | --------------------- |
| 资产收益矩阵 | 各候选资产/策略的日收益   | 波动估计质量决定权重合理性         |
| 估计窗口   | 用多长历史估波动       | 过长→失真，过短→噪声大（常 1–2 年） |
| 约束     | 权重上下限、不允许做空    | 实务中常加 >=0 与单资产上限      |
| 相关性    | 资产间相关越高，简化近似越偏 | 高相关时建议改用精确 ERC        |

### 2.4 文献引用

Carver, R. (2017). *Smart Portfolios*. Harriman House. — 关于 account-level risk budget 与 risk parity 的章节（概括引用，不摘录原文）。

---

## 3. Clenow《Stocks on the Move》(2015) — 股票动量策略

### 3.1 核心思想（中文解读）

把"趋势跟踪"从期货搬到股票组合，形成一套可执行的股票动量框架：

- **动量筛选**：用"价格是否接近 N 日新高"（如 100/200 日最高价的一定比例）作为动量信号，而非传统截面排序。
- **波动率目标化组合**：对入选股票按各自波动反比配权（与 Carver 第 1 章同源），把组合年化波动压到目标（如 20%–25%），避免单票主导。
- **趋势止损与再平衡**：定期（月/季）重新筛选与配权，跌破趋势则退出。

### 3.2 完整回测模板（自写）

逻辑见 `scripts/momentum_equity.py`：

```python
def momentum_signal(price, lookback=200, pct=0.95):
    return price >= price.rolling(lookback).max() * pct   # 接近 N 日新高

def vol_target_weights(returns, target_vol=0.20):
    inv_vol = 1.0 / (returns.std() * np.sqrt(252)).replace(0, np.nan)
    w = inv_vol / inv_vol.sum()
    return w.fillna(0)
```

示范：对 4 只模拟股票，输出"是否接近 200 日新高"信号与波动率目标化权重。可替换为真实行情（经 MCP 拉取）后直接回测。

### 3.3 关键参数

| 参数           | 含义          | 常见区间      | 影响          |
| ------------ | ----------- | --------- | ----------- |
| `lookback`   | 动量回看窗口      | 100–250 日 | 越长越偏长线、信号越少 |
| `pct`        | 触发阈值（占新高比例） | 0.90–1.00 | 越接近 1 越严格   |
| `target_vol` | 组合目标波动      | 0.18–0.30 | 决定整体杠杆      |
| 再平衡周期        | 重新筛选频率      | 月/季       | 影响换手与税费     |

### 3.4 文献引用

Clenow, A. (2015). *Stocks on the Move*. Wiley. — 关于 momentum filter 与 volatility target 的章节（概括引用，不摘录原文）。

---

## 4. Tomasini & Jaekle《Trading Systems》(2009) — 系统开发流程与防过拟合

### 4.1 核心思想（中文解读）

把"做一个能上实盘的交易系统"变成可复现的工程流程：

1. **数据准备**：清洗、对齐、处理除权除息与停牌。
2. **信号/规则定义**：明确进场、出场、止损、仓位。
3. **回测**：在历史数据上跑，记录收益、回撤、换手。
4. **评估与稳健性**：参数敏感性、样本内 vs 样本外、不同市场/时段是否稳定。
5. **实盘过渡**：纸上交易→小资金→放量，监控偏离。

### 4.2 防过拟合 / 样本外检验（自写演示）

结合 Aronson《Evidence-Based Technical Analysis》(2006) 的统计视角，逻辑见 `scripts/backtest_guardrails.py`：

- **参数稳定性扫描**：在训练集上扫描参数，看最优值是否"尖峰孤立"（孤立尖峰 = 过拟合信号）。
- **样本外衰减**：把数据分成训练/测试，训练集选最优参数后，在测试集检验绩效是否显著下降。

```python
# 示意：训练集选最优均线周期，测试集验证
best_p = select_best_param(train_ret, grid=range(5, 61))
train_sharpe = sharpe(train_ret, best_p)
test_sharpe  = sharpe(test_ret, best_p)
print(f"训练 Sharpe={train_sharpe:.2f} 样本外 Sharpe={test_sharpe:.2f} "
      f"衰减={train_sharpe-test_sharpe:.2f}")
```

若样本外衰减过大，说明参数依赖历史噪声，应 widen 参数或简化模型。

### 4.3 关键清单

| 检查项        | 目的       |
| ---------- | -------- |
| 参数是否孤立尖峰   | 识别过拟合    |
| 样本外是否明显衰减  | 验证泛化     |
| 多市场/多时段一致性 | 排除偶然     |
| 成本/滑点是否计入  | 防止"纸面盈利" |
| 未来函数检查     | 杜绝偷看未来   |

### 4.4 文献引用

Tomasini, E. & Jaekle, U. (2009). *Trading Systems: A New Approach to System Development*. Harriman House.  
Aronson, D. (2006). *Evidence-Based Technical Analysis*. Wiley. — 关于 data snooping 与样本外检验的章节（概括引用，不摘录原文）。

---

## 5. Teweles & Jones《The Futures Game》(3rd ed) — 期货市场机制与套保基础

### 5.1 核心思想（中文解读）

期货"圣经"，偏市场机制与基础认知，是前面策略的**土壤**：

- **合约机制**：标准化合约（标的、月份、乘数）、做多/做空对称、杠杆本质。
- **保证金与逐日盯市（mark-to-market）**：每日结算盈亏，保证金不足即追保（margin call），这是期货高杠杆风险的根源。
- **交割与展期**：近月合约到期前需平仓或移仓（roll），展期成本影响长期持有收益。
- **套期保值**：现货持有者用期货反向对冲价格风险，核心是**套保比率（hedge ratio）**——期货头寸规模与现货暴露的比例。

### 5.2 套保比率（最低方差）说明

经典最小方差套保比率：`h* = Cov(ΔS, ΔF) / Var(ΔF)`，其中 S 为现货、F 为期货。可用 `scripts/backtest_guardrails.py` 之外的简单回归估计（或后续补脚本）。本 Skill 的通用回测模板 `scripts/backtest_template.py` 亦可用于对比"套保前/后"组合波动。

### 5.3 文献引用

Teweles, R. & Jones, F. (2008). *The Futures Game* (3rd ed.). McGraw-Hill. — 关于合约机制、保证金、套期保值的章节（概括引用，不摘录原文）。

---

## 使用建议

- 想跑**单品种仓位**：用 `vol_target_position.py`。
- 想做**股票动量组合**：用 `momentum_equity.py`（可接 MCP 真实行情）。
- 想做**多资产组合分配**：用 `risk_parity.py`。
- 想**检验策略是否过拟合**：用 `backtest_guardrails.py`。
- 所有模板均为研究用途，实盘前务必计入成本、滑点与样本外验证。
