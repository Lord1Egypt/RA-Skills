# 文献深做：高频交易与市场微观结构

> **处理方法**：中文方法论解读 + 要点/可执行思路 + 文献出处引用。
> 本组偏**方法论与理论**，多数不对应单一"回测模板"（与前面可回测策略不同），故以概念框架 + 实务要点为主，少量给出可落地的计算思路。
> **版权红线**：只做中文重写的方法论概括与引用，引用格式 `作者(年份)《书名》`。

---

## 1. Aldridge《High-Frequency Trading: A Practical Guide》(2nd ed, 2013)

### 1.1 核心思想（中文解读）
把 HFT 当作**工程系统**而非单一策略：
- **策略分类**：做市(market making)、套利(arb)、方向性(directional)、统计套利等。
- **延迟是关键资源**：从行情到下单的全链路延迟决定策略可行性。
- **微观结构建模**：买卖价差、订单簿动态、短期均值回复是策略基础。
- **回测特殊性**：HFT 回测必须考虑排队位置、部分成交、滑点，普通日线回测完全无效。

### 1.2 实务要点
| 维度 | 说明 |
|---|---|
| 延迟 | 同轴/FPGA/就近托管(colocation)降低延迟 |
| 数据 | Level-2 / 逐笔(tick) 数据，非 OHLC |
| 成本 | 手续费、滑点、市场冲击需精确建模 |
| 风险 | 策略同质化导致的闪崩(flash crash)风险 |

### 1.3 文献引用
Aldridge, I. (2013). *High-Frequency Trading* (2nd ed.). Wiley. — 关于 HFT strategy taxonomy 与 microstructure 的章节（概括引用，不摘录原文）。

---

## 2. MacKenzie《Trading at the Speed of Light》(2021)

### 2.1 核心思想（中文解读）
从**社会技术系统**视角看 HFT：技术（算法、硬件、网络）与制度（交易所规则、监管）相互塑造。
- 不是教策略，而是理解 HFT 生态如何被基础设施与规则建构。
- 对从业者价值：理解"游戏规则"变迁（如交易所 rebate 结构、tick size）如何消灭或催生策略。

### 2.2 文献引用
MacKenzie, D. (2021). *Trading at the Speed of Light*. University of Chicago Press.（概括引用，不摘录原文）。

---

## 3. Lehalle & Laruelle《Market Microstructure in Practice》(2nd ed, 2018)

### 3.1 核心思想（中文解读）
把微观结构**建模**落到可优化：
- **订单簿动态**：限价单的排队、成交概率随队列位置变化。
- **最优执行(execution algo)**：把大单拆成小单，在冲击与时机风险间权衡（如 VWAP / TWAP / 更复杂的执行算法）。
- **微观结构因子**：从订单流中提炼可交易的短期信号。

### 3.2 可执行思路（自写起点）
- 用逐笔数据估计**成交概率模型**（队列位置 → 成交概率）。
- 用 `scripts/risk_forecast.py` 的思路扩展为**执行成本预测**。
- 大单拆单可用简单 VWAP 跟踪作为 baseline（自写即可）。

### 3.3 文献引用
Lehalle, C.-A. & Laruelle, S. (2018). *Market Microstructure in Practice* (2nd ed.). Cambridge University Press.（概括引用，不摘录原文）。

---

## 4. Dacorogna et al.《An Introduction to High-Frequency Finance》(2001)

### 4.1 核心思想（中文解读）
高频金融数据的**计量基础**（奠基之作）：
- **时间缩放(time scaling)**：不同频率下统计特征的缩放规律。
- **滤波与去噪**：从噪声中提取真实价格路径。
- **异方差与长记忆**：高频波动的聚类特征。

### 4.2 可执行思路
- 用 EWMA（`risk_forecast.py` 同思路）对 tick 数据做实时波动估计。
- 用滚动窗口估计高频收益的标度律。

### 4.3 文献引用
Dacorogna, M. et al. (2001). *An Introduction to High-Frequency Finance*. Academic Press.（概括引用，不摘录原文）。

---

## 配套脚本（自写，可本地直接运行）
| 脚本 | 演示内容 | 对应文献 |
|---|---|---|
| `scripts/hft_fill_probability.py` | 限价单排队成交概率（队列位置衰减） | Lehalle & Laruelle / 订单簿 |
| `scripts/hft_vwap_execution.py` | VWAP/TWAP 拆单执行与跟踪误差 | Lehalle & Laruelle |
| `scripts/hft_time_scaling.py` | 高频收益时间缩放/标度律、波动聚集 | Dacorogna et al. |

---

## 使用建议
- HFT/微观结构门槛高、受众窄但客单价极高，适合作为**进阶/机构向**付费模块，而非大众入口。
- 实务落地强烈依赖 tick/Level-2 数据与低延迟通道，**普通零售环境难以复现**，讲解时应明确边界。
- 回测务必包含排队、部分成交、冲击成本，否则结论失真（见 Tomasini 系统开发流程章节）。
