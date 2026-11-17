# 文献深做：量化基础与工具

> **处理方法**：中文方法论解读 + 要点/可执行思路 + 文献出处引用。本组多为**数学基础、学习路径与工具书**，以"知识地图 + 自写可运行片段"为主，不强行套用回测模板。
> **版权红线**：只做中文重写的方法论概括与自写代码，引用格式 `作者(年份)《书名》`。

---

## 1. Stefanica《A Primer for the Mathematics of Financial Engineering》(2nd ed)

### 1.1 核心思想（中文解读）
金融工程所需的数学"自学圣经"（Baruch MFE 教材）：
- 微积分/线性代数/概率论在定价与对冲中的角色。
- 数值方法（有限差分、插值的直觉）。
### 1.2 对 Skill 的价值
作为**学习路径地图**：想深入定价/对冲的人，按此书补数学地基。本 Skill 的代码（如 `option_greeks.py`）所用到的 BS 公式正是其覆盖内容。
### 1.3 文献引用
Stefanica, D. (2011). *A Primer for the Mathematics of Financial Engineering* (2nd ed.). FE Press.

---

## 2. Regenstein《Reproducible Finance with R》(2018)

### 1.1 核心思想（中文解读）
强调**可重复研究（reproducible research）**：分析流程、数据、代码一体，别人能复现你的结果。
- R 中的组合优化与回测工作流。
### 1.2 对应本 Skill
本 Skill 用 Python 实现同等目标；理念一致——**回测必须可重复、可审计**（呼应 Tomasini 系统开发流程）。
### 1.3 文献引用
Regenstein, J. (2018). *Reproducible Finance with R*. CRC Press.

---

## 3. Chincarini & Kim《Quantitative Equity Portfolio Management》(2nd ed)

### 3.1 核心思想（中文解读）
系统化构建量化权益组合：
- **因子模型**：收益由若干因子（动量、价值、规模…）解释。
- **组合优化**：在因子暴露约束下最大化预期收益/风险比。
- **交易成本建模**：换手成本直接吃掉 alpha。
### 3.2 自写代码
见 `scripts/equity_portfolio.py`：动量因子得分 + 波动率目标化配权（简化 max-Sharpe），演示因子组合核心逻辑。
### 3.3 文献引用
Chincarini, L. & Kim, D. (2009). *Quantitative Equity Portfolio Management* (2nd ed.). McGraw-Hill.

---

## 4. Wilmott《Frequently Asked Questions in Quantitative Finance》(2nd ed)

### 4.1 核心思想（中文解读）
量化核心概念的 FAQ 合集：从 BS 公式到随机微积分的速查。
- 适合作为**概念速查表**与面试准备。
### 4.2 对应本 Skill
本 Skill 各章节的公式与概念（Greeks、VaR、Kelly…）可与本书交叉参考，互为索引。
### 4.3 文献引用
Wilmott, P. (2008). *Frequently Asked Questions in Quantitative Finance* (2nd ed.). Wiley.

---

## 5. MacLean et al.《The Kelly Capital Growth Investment Criterion》(2011)

### 5.1 核心思想（中文解读）
凯利公式 / 资本增长理论的权威论文集：
- **Kelly 比例** f* = p − (1−p)/b 决定最优下注比例，长期增长最快。
- **半 Kelly (f*/2)** 更稳健，显著降低回撤，实务常用。
### 5.2 自写代码
见 `scripts/kelly_position.py`：从收益序列估计胜率 p 与盈亏比 b，算 Kelly / 半 Kelly 下注比例。与 Carver 波动率目标化仓位（见 `systematic_main.md`）共同构成"仓位理论"双支柱。
### 5.3 文献引用
MacLean, L. et al. (2011). *The Kelly Capital Growth Investment Criterion*. World Scientific.

---

## 6. Kuznetsov《The Complete Guide to Capital Markets for Quantitative Professionals》(2006)

### 6.1 核心思想（中文解读）
量化从业者的**资本市场全图谱**：产品、参与者、市场机制。
- 作为"市场结构速查"，帮助理解策略落地的制度环境。
### 6.2 对应本 Skill
与 `hft_microstructure.md` 的微观结构、Teweles《The Futures Game》的期货机制互为补充，构成"市场认知层"。
### 6.3 文献引用
Kuznetsov, A. (2006). *The Complete Guide to Capital Markets for Quantitative Professionals*. Harper.

---

## 使用建议
- 本组是**地基与地图**：数学(Stefanica)、可重复研究(Regenstein)、因子组合(Chincarini)、速查(Wilmott)、仓位理论(MacLean)、市场图谱(Kuznetsov)。
- 想直接上手策略：优先看 `systematic_main.md` 与 `options_volatility.md`、`risk_management.md`；本组用于"补基础"与"交叉索引"。
