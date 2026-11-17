# 量化 / 期货 英文文献索引（知识地图）

> **用途**：本文件是 `quant-trading-kit` 策略解读 Skill 的**文献索引与知识地图**，把用户提供的 20 本英文原版书/论文集，按「可封装程度」映射到具体策略模块。
>
> **版权红线（必须遵守）**：本索引及后续所有策略章节，**只做中文解读、方法论概括与出处引用，绝不复制任何受版权保护的原文段落**。引用一律采用「作者（年份）《英文原名》」格式，便于读者查证原书。所有可运行代码均为本 Skill 自行编写或改写，不搬运原书源码。
>
> **标注说明**：
> - 🟢 **强可封装**：直接相关于可回测策略，优先深做
> - 🟡 **方法论/工具**：提供框架、统计或数学基础，适合做"方法索引 + 引用"
> - 🔴 **背景/理论**：偏学术或系统性认知，适合做概念说明而非回测

---

## 一、系统化交易与组合管理

### 《Systematic Trading》(2015) — Robert Carver  🟢
- **领域**：系统化期货交易、策略设计、仓位与风控框架（含 Python）
- **可提取核心**：① 波动率目标化仓位（volatility targeting）；② 多策略/多品种风险预算；③ 信号→仓位的标准化流水线；④ 用"固定分数/风险"而非固定手数的仓位逻辑。
- **对应 Skill 模块**：`仓位管理`、`风险预算`、`趋势/动量类策略框架`
- **变现角度**：期货系统化交易中文圈稀缺、付费意愿强，是本项目主线之一
- **引用**：Carver, R. (2015). *Systematic Trading*. Harriman House.

### 《Smart Portfolios》(2017) — Robert Carver  🟡
- **领域**：系统化交易者的组合构建与资金分配
- **可提取核心**：① 账户层资金在策略/资产间的分配；② 风险平价（risk parity）思路；③ 组合层相关性处理与再平衡。
- **对应 Skill 模块**：`组合构建`、`资金分配`、`风险平价`
- **变现角度**：与上一本配套，构成"单策略→组合"完整链路
- **引用**：Carver, R. (2017). *Smart Portfolios*. Harriman House.

### 《Stocks on the Move》(2015) — Andreas Clenow  🟢
- **领域**：动量股票策略的完整回测与实施（含完整源码）
- **可提取核心**：① 以 ATR/通道突破定义的股票动量筛选；② 波动率目标化股票组合；③ 趋势跟踪在权益市场的落地。
- **对应 Skill 模块**：`股票动量策略`（最易变现、代码可直接改写）
- **变现角度**：股票动量是最广受众方向之一，示例清晰，适合做"股票动量策略从0到1"
- **引用**：Clenow, A. (2015). *Stocks on the Move*. Wiley.

### 《Trading Systems: A New Approach to System Development》(2009) — Tomasini & Jaekle  🟢
- **领域**：从数据准备到实盘的交易系统开发全流程
- **可提取核心**：① 系统开发的阶段化流程（数据→信号→回测→评估→实盘）；② 参数稳健性/样本外检验；③ 交易系统评分框架。
- **对应 Skill 模块**：`系统开发流程`、`回测规范`
- **变现角度**：新手最缺"完整流程"，做成"交易系统搭建 SOP"价值高
- **引用**：Tomasini, E. & Jaekle, U. (2009). *Trading Systems*. Harriman House.

### 《Evidence-Based Technical Analysis》(2006) — David Aronson  🟢
- **领域**：用科学统计方法验证技术分析（AIMR 最佳研究奖，开山之作）
- **可提取核心**：① 数据窥探偏差（data snooping）与过拟合识别；② 统计显著性与 p 值/置信区间在策略检验中的应用；③ 样本内/样本外、WFE（白噪声检验）框架。
- **对应 Skill 模块**：`策略显著性检验`、`防过拟合`
- **变现角度**：所有策略的"可信度过滤器"，可独立成"策略回测防坑"模块
- **引用**：Aronson, D. (2006). *Evidence-Based Technical Analysis*. Wiley.

---

## 二、期货与衍生品

### 《The Futures Game》(3rd ed) — Teweles & Jones  🟢
- **领域**：期货市场百科全书级经典，"期货圣经"
- **可提取核心**：① 期货/远期/期权合约机制；② 保证金、盯市、交割；③ 套期保值与投机基础；④ 主要品种与市场结构。
- **对应 Skill 模块**：`期货基础`、`市场机制`、`套保逻辑`
- **变现角度**：新手入门刚需，适合做"期货入门知识库"章节
- **引用**：Teweles, R. & Jones, F. (2008). *The Futures Game* (3rd ed.). McGraw-Hill.

### 《Positional Option Trading》(2020) — Euan Sinclair  🟢
- **领域**：高级期权头寸策略，结合波动率曲面与风控
- **可提取核心**：① 期权头寸的 Greeks 管理；② 波动率曲面视角下的头寸构建；③ 波动率预测与风控。
- **对应 Skill 模块**：`期权策略`、`波动率交易`
- **变现角度**：期权是期货之后最垂直的付费方向
- **引用**：Sinclair, E. (2020). *Positional Option Trading*. Wiley.

### 《Derivatives Analytics with Python》(2015) — Yves Hilpisch  🟡
- **领域**：用 Python 做衍生品定价、市场模拟与 Greeks 分析
- **可提取核心**：① 蒙特卡洛/数值方法定价；② Greeks 计算；③ 市场模拟。
- **对应 Skill 模块**：`期权定价（数学工具）`
- **变现角度**：偏工具/代码库，适合做"定价计算"辅助模块
- **引用**：Hilpisch, Y. (2015). *Derivatives Analytics with Python*. Wiley.

---

## 三、高频交易与市场微观结构

### 《High-Frequency Trading: A Practical Guide》(2nd ed, 2013) — Irene Aldridge  🟡
- **领域**：高频策略开发、回测及市场微观结构模型
- **可提取核心**：① 高频策略分类；② 微观结构相关的执行成本建模；③ 高频回测注意事项。
- **对应 Skill 模块**：`高频策略（高门槛）`、`执行成本`
- **变现角度**：门槛高、受众窄但客单价极高，可作为进阶付费项
- **引用**：Aldridge, I. (2013). *High-Frequency Trading* (2nd ed.). Wiley.

### 《Trading at the Speed of Light》(2021) — Donald MacKenzie  🔴
- **领域**：高频交易的社会技术系统全景分析（偏学术/历史）
- **可提取核心**：① 高频生态与基础设施认知；② 技术—制度互动。
- **对应 Skill 模块**：`背景认知`
- **变现角度**：不构成策略，适合做"行业认知"说明
- **引用**：MacKenzie, D. (2021). *Trading at the Speed of Light*. University of Chicago Press.

### 《Market Microstructure in Practice》(2nd ed, 2018) — Lehalle & Laruelle  🟡
- **领域**：市场微观结构建模与交易策略优化
- **可提取核心**：① 订单簿动态；② 最优执行（执行算法）思路；③ 微观结构因子。
- **对应 Skill 模块**：`微观结构`、`执行优化`
- **变现角度**：进阶，适合机构/专业用户
- **引用**：Lehalle, C.-A. & Laruelle, S. (2018). *Market Microstructure in Practice* (2nd ed.). Cambridge University Press.

### 《An Introduction to High-Frequency Finance》(2001) — Dacorogna et al.  🟡
- **领域**：高频金融数据的滤波、缩放与计量方法（奠基之作）
- **可提取核心**：① 高频数据的统计特征；② 时间缩放（time scaling）；③ 滤波与去噪。
- **对应 Skill 模块**：`高频数据处理`
- **变现角度**：方法论文献，适合做"数据处理方法索引"
- **引用**：Dacorogna, M. et al. (2001). *An Introduction to High-Frequency Finance*. Academic Press.

---

## 四、量化金融数学与编程

### 《A Primer for the Mathematics of Financial Engineering》(2nd ed) — Dan Stefanica  🟡
- **领域**：金融工程数学自学圣经（Baruch MFE 教材）
- **可提取核心**：① 微积分/线性代数/概率在量化中的角色；② 数值方法基础。
- **对应 Skill 模块**：`数学基础（工具书）`
- **变现角度**：学习路径指引，适合做"量化数学学习地图"
- **引用**：Stefanica, D. (2011). *A Primer for the Mathematics of Financial Engineering* (2nd ed.). FE Press.

### 《Reproducible Finance with R》(2018) — Jonathan Regenstein  🟡
- **领域**：用 R 做可重复的金融分析、组合优化与回测
- **可提取核心**：① 可重复研究工作流；② R 中的组合优化与回测。
- **对应 Skill 模块**：`回测框架（R）`、`可重复研究`
- **变现角度**：方法论参考，可对照给出 Python 版实现
- **引用**：Regenstein, J. (2018). *Reproducible Finance with R*. CRC Press.

### 《Quantitative Equity Portfolio Management》(2nd ed) — Chincarini & Kim  🟡
- **领域**：量化权益组合的因子模型、优化算法与交易成本建模
- **可提取核心**：① 因子模型构建；② 组合优化；③ 交易成本建模。
- **对应 Skill 模块**：`权益组合管理`、`因子模型`
- **变现角度**：权益量化系统级参考
- **引用**：Chincarini, L. & Kim, D. (2009). *Quantitative Equity Portfolio Management* (2nd ed.). McGraw-Hill.

### 《Frequently Asked Questions in Quantitative Finance》(2nd ed) — Paul Wilmott  🔴
- **领域**：量化面试必读 FAQ 合集
- **可提取核心**：① 量化核心概念速查；② 面试/自测参考。
- **对应 Skill 模块**：`综合参考（工具书）`
- **变现角度**：参考索引，适合做"量化概念速查表"
- **引用**：Wilmott, P. (2008). *Frequently Asked Questions in Quantitative Finance* (2nd ed.). Wiley.

---

## 五、风险管理

### 《Trading Risk》(2004) — Kenneth Grant  🟢
- **领域**：对冲基金交易风险管理的实战框架
- **可提取核心**：① 交易风险的组织与流程；② 限额体系；③ 风险事件处理。
- **对应 Skill 模块**：`交易风险管理`
- **变现角度**：风控是付费决策者的刚需
- **引用**：Grant, K. (2004). *Trading Risk*. Wiley.

### 《Financial Risk Forecasting》(2011) — Jon Danielsson  🟡
- **领域**：金融风险预测（GARCH 到极值理论，含 R 代码）
- **可提取核心**：① 波动率预测（GARCH 族）；② 风险价值 VaR / 期望短缺 ES；③ 极值理论 EVT。
- **对应 Skill 模块**：`风险预测`、`波动率建模`
- **变现角度**：可独立成"风险预测模块"，代码可改 Python
- **引用**：Danielsson, J. (2011). *Financial Risk Forecasting*. Wiley.

---

## 六、其他重要著作

### 《The Kelly Capital Growth Investment Criterion》(2011) — MacLean et al.  🟡
- **领域**：凯利公式 / 资本增长理论的权威学术论文集
- **可提取核心**：① 凯利仓位公式及其变体；② 资本增长与回撤权衡；③ 分数凯利（half-Kelly）实践。
- **对应 Skill 模块**：`仓位/资金增长理论`
- **变现角度**：与 Carver 仓位管理呼应，构成"仓位理论"双支柱
- **引用**：MacLean, L. et al. (2011). *The Kelly Capital Growth Investment Criterion*. World Scientific.

### 《The Complete Guide to Capital Markets for Quantitative Professionals》(2006) — Alex Kuznetsov  🔴
- **领域**：量化从业者的资本市场全图谱
- **可提取核心**：① 资本市场结构全景；② 各类产品与参与者。
- **对应 Skill 模块**：`市场知识（工具书）`
- **变现角度**：认知地图，适合做"市场结构速查"
- **引用**：Kuznetsov, A. (2006). *The Complete Guide to Capital Markets for Quantitative Professionals*. Harper.

---

## 建议的深做路线（待用户确认）

- **主线（最贴"期货+量化"定位，变现主力）**：Carver《Systematic Trading》+ Clenow《Stocks on the Move》+ Tomasini《Trading Systems》+ Teweles《The Futures Game》
- **质量标杆（先做 3 本示范）**：Carver 系统化交易 + Clenow 动量股票 + Aronson 证据检验
- **风控补强**：Grant《Trading Risk》+ Danielsson《Financial Risk Forecasting》+ MacLean《Kelly》
- **进阶/机构向**：Sinclair 期权 + Aldridge/Lehalle 微观结构 + Chincarini 权益组合

> 深做每本书时，在 `strategies.md` 或独立章节中给出：① 中文方法论解读 ② 可运行回测/计算模板（本 Skill 自写代码）③ 参数说明 ④ 文献引用（作者/年/书名）。
