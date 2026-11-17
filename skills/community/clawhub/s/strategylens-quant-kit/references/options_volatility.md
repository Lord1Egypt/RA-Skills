# 文献深做：期权与衍生品

> **处理方法**：中文方法论解读 + 本 Skill **自写**的可运行模板（仅用标准库，不依赖任何期权库，不复制原书代码）+ 参数说明 + 文献出处引用。
> **版权红线**：只做中文重写的方法论概括与自写代码，引用格式 `作者(年份)《书名》`。

---

## 1. Sinclair《Positional Option Trading》(2020) — 期权头寸策略与风控

### 1.1 核心思想（中文解读）
把期权视为"头寸（position）"而非单纯的方向赌注：
- **Greeks 管理是核心**：用 Delta/Gamma/Vega/Theta 刻画头寸对价格、波动、时间的暴露，并设定各 Greek 的预算上限。
- **波动率视角**：隐含波动率(IV)与已实现波动(realized vol)的关系是利润来源；IV 偏高/偏低决定卖方/买方倾向。
- **波动率曲面**：skew（偏度）与期限结构(term structure)决定具体合约选择，而非只看方向。
- **尾部与 Gamma 风险**：临近到期 Gamma 放大，价格跳空时对冲成本骤升，需要情景压力测试。

### 1.2 关键要点
| 要素 | 实务含义 |
|---|---|
| Delta 中性 / 定向暴露 | 是否保留方向性，决定策略β |
| Vega | 对波动率变化的暴露（波动率交易的核心 Greek） |
| Gamma | 临近到期放大，决定对冲频率 |
| Theta | 时间衰减，卖方的主要收益来源 |
| IV rank / percentile | 判断当前 IV 处于历史高位还是低位 |

### 1.3 自写代码（Greeks 计算）
见 `scripts/option_greeks.py`：用最基础的 Black-Scholes 公式自写看涨/看跌定价与主要 Greeks，仅依赖 `math`/`numpy`，可立即运行、便于二次开发。

### 1.4 文献引用
Sinclair, E. (2020). *Positional Option Trading*. Wiley. — 关于 option position Greeks 与 volatility surface 的章节（概括引用，不摘录原文）。

---

## 2. Hilpisch《Derivatives Analytics with Python》(2015) — 衍生品定价与 Greeks

### 2.1 核心思想（中文解读）
用 Python 把衍生品分析工程化：
- **定价**：解析法（Black-Scholes 类）与数值法（蒙特卡洛、有限差分、树）。
- **Greeks**：对定价公式求灵敏度的解析或数值实现。
- **市场模拟**：用随机过程（几何布朗运动、跳跃扩散）模拟标的路径，做风险与对冲演练。

### 2.2 自写代码（定价与 Greeks）
见 `scripts/option_greeks.py`：自写 Black-Scholes 看涨/看跌价格与 delta/gamma/vega/theta/rho。原书用 `NumPy`/`SciPy` 做更完整的分析，本 Skill 用最小依赖实现核心公式，便于理解后即可扩展到蒙特卡洛等。

### 2.3 文献引用
Hilpisch, Y. (2015). *Derivatives Analytics with Python*. Wiley. — 关于 pricing / Greeks / simulation 的章节（概括引用，不摘录原文）。

---

## 使用建议
- 想算**单期权定价与 Greeks**：直接跑 `option_greeks.py`，按需替换 S/K/T/r/σ。
- 想做**波动率交易/头寸管理**：结合第 1 章的 Greeks 预算框架，把 `option_greeks.py` 的输出纳入头寸层面汇总。
- 所有计算为研究用途，实盘需接入实时 IV 与对冲成本。
