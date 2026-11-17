# 纵向 / 面板 / 生存分析卡（longitudinal & survival）

> 招式定位：描述 / 比较 / 预测 / 解释机制。学科轴：医学/临床 · 社科/教育 · 心理 · 生态。
> 与 `cards/data-analysis.md`（截面统计）、`cards/experiment-design.md`（干预）互补：本卡专治"随时间变化"的数据。

## 适用场景
- 同一批人/对象**反复测**（panel / 纵向）：成长、衰退、变化轨迹。
- **到事件时间**数据：复发、死亡、离职、失败——大量删失（censoring）。
- 想看"随时间的变化"或"谁先发生事件"，而非只比组间均值。

## 核心方法
1. **纵向建模**：
   - 多层/混合效应模型（HLM）：个体为随机截距/斜率，建模轨迹（线性/曲线增长）。
   - 广义估计方程（GEE）：看总体平均趋势，对缺失更稳。
   - 交叉滞后模型（CLPM / 随机截距 CLPM）：分"稳定特质"与"随时间因果"。
2. **生存分析（时间到事件）**：
   - Kaplan–Meier 估生存曲线；log-rank 比组间。
   - Cox 比例风险模型：估风险比 HR（控制协变量），不强假设基线风险形状。
   - 竞争风险（Fine–Gray）：有互斥事件时别用普通删失。
3. **样本量**：纵向需算"有效样本"（相关性强→需更多时间点/人）；生存需算**事件数**而非人数。

## 前提
- 时间点设计合理（等距/覆盖变化期）；缺失机制最好 MAR，用 FIML/多重插补。
- 删失机制非信息性（删失与事件风险无关）——否则 HR 偏。

## 常见坑
- **混淆年龄效应与队列效应**（横断+纵向西门庆陷阱）：用出生队列设计或增长模型分离。
- **相关聚类当独立**：同一人多次测量不独立，普通回归 SE 偏小→假显著；用稳健 SE / 混合模型。
- **Cox 比例风险假设破**：HR 随时间变（如治疗后期失效）——画 log-log 图或用时变协变量检验。
- **滥用删失**：把失访当"没事件"直接删，低估风险。

## 何时换招
- 只需单次截面比较 → `cards/data-analysis.md`。
- 想做干预看效果 → `cards/experiment-design.md`（可结合纵向随访）。
- 要"复现/公开数据" → `cards/replication-preregistration.md`。

## 经典出处
- Singer & Willett 2003. *Applied Longitudinal Data Analysis*. Oxford. ISBN 9780195152968
- Therneau & Grambsch 2000. *Modeling Survival Data*（Springer）
- Cox 1972. Regression models and life-tables. JRSS B 34:187–220
