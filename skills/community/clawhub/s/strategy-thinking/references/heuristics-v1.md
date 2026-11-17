# C 层启发式 V1.0 — 进入工作流的 9 条 + 暂不进入的 8 条

> **证据状态**：所有 C 层条目均为 AI 抽象的假设，未经用户明确确认。
> **执行强度**：[默认启发式，AI 抽象，可 override]
> **隔离规则**：C 层假设不得出现在硬约束位置、必经路径、必须通过验收项中。
> **Provenance 体系**：四轴标注（ORIGIN × ENDORSEMENT × EVIDENCE-BASIS × VALIDATION-MATURITY）

---

## 进入 V1.0 工作流的 9 条

### C1：七维思考维度划分

| 字段 | 内容 |
|------|------|
| 假设 | 七维思考（结果/条件/问题/资源/路径/策略/执行）的维度划分是否完整 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | USER-ACKNOWLEDGED |
| EVIDENCE-BASIS | USER-STATEMENT + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 部分验证） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | 内部默认导航框架 |
| 触发参考 | 默认作为内部导航参考；根据项目实际情况增减或跳过，不要求每次显式调用 |
| 什么情况下不应强行调用 | 当用户已有完整方案时——不需要逐维检查，直接进入 DECIDE 检查模式 |

> **C1 来源说明**：用户提供七个维度的原始表述（EVIDENCE-BASIS 含 USER-STATEMENT），AI 将其结构化为 C1 框架/完整性假设（ORIGIN=AI-AUTHORED）。用户对维度内容有贡献，但对框架结构和完整性假设未给出强确认信号（ENDORSEMENT=USER-ACKNOWLEDGED）。

> **C1 与四项闭环的关系**：四项闭环（当前结果/真正问题/路径+理由/下一步行动）是 D5/Runtime Rule 的要求，不是 C1 的硬约束权力。即使不调用 C1，也必须产生四项闭环。C1 本身可被 override。
>
> 完整定义见 `method-core-v1.md` §3。

---

### C3：多场景探索触发条件

| 字段 | 内容 |
|------|------|
| 假设 | 多场景探索的触发条件是什么 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | USER-ACKNOWLEDGED |
| EVIDENCE-BASIS | AI-INFERENCE + CASE |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（Case 01 SUPPORT，Case 02 NOT-TRIGGERED，证据增强但未识别唯一触发变量） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | EXPLORE 状态的柔性判断 |
| 触发参考 | 路径清晰、不确定性低 → 直接选一条。存在多个可行方向、不确定性高 → 建立可比较场景。用户已在自己探索 → 帮他系统化比较 |
| 可能触发信号 | 定价/商业模式选择、技术路线选择、目标用户群体选择、渠道/平台选择（柔性参考，非硬规则） |
| 不触发信号 | 只有一条技术可行路径、时间紧迫不允许比较、用户已有明确选择 |
| 什么情况下不应强行调用 | 只有一条路径时——不创建人为的多方案比较。用户已有明确选择时——不推翻用户思路 |

---

### C4：多维决策维度构成与通用性

| 字段 | 内容 |
|------|------|
| 假设 | 多维决策的维度构成与通用性（主观判断/同类对比/市场反馈是否完整，是否跨场景适用） |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | DOC + AI-INFERENCE |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（3 案例SUPPORT框架层面，Case 02 出现新维度） |
| 证据状态 | [默认启发式，维度可增减] |
| 产品角色 | DECIDE 状态的多维比较参考 |
| 触发参考 | 存在多个方案需要比较时。提供多维比较框架，但维度因项目而异 |
| 什么情况下不应强行调用 | 只有一个方案时——不需要多维比较。用户已有明确倾向时——只验证合理性，不强推自己的比较框架 |

---

### C7：目标优先级重排 / 项目价值重估

| 字段 | 内容 |
|------|------|
| 假设 | 目标优先级重排 / 项目价值重估 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | CASE + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 SUPPORT） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | S3 入口（遇到问题重新策划）的判断参考 |
| 触发参考 | 用户遇到重大挫折或方向变化时。评估当前目标是否需要重排优先级，而非放弃 |
| 什么情况下不应强行调用 | 用户只是遇到小障碍时——不需要重排目标优先级。用户目标清晰且进展正常时——不引入"价值重估" |

---

### C9：一石多鸟行动选择

| 字段 | 内容 |
|------|------|
| 假设 | 一石多鸟行动选择 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | CASE + AI-INFERENCE |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（Case 02 + Case 03 SUPPORT） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | EXPLORE 状态的辅助判断 |
| 触发参考 | 探索路径时留意是否有能同时满足多个需求的高杠杆动作 |
| 什么情况下不应强行调用 | 当项目目标单一明确时——不需要寻找"一石多鸟"。当寻找杠杆动作会显著增加复杂度时——不强行引入 |

---

### C11：当前层多次尝试无效 → 提升问题层级

| 字段 | 内容 |
|------|------|
| 假设 | 当前层多次尝试无效 → 提升问题层级重新判断 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | CASE + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 SUPPORT） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | S3 入口（遇到问题重新策划）的判断参考 |
| 触发参考 | 用户在当前层面反复尝试仍无法突破时。评估是否需要提升到更高层级重新定义问题 |
| 什么情况下不应强行调用 | 用户只是首次遇到障碍时——不急于提升层级。当前层尝试尚未充分时——不跳过当前层 |

---

### C13：先小规模验证再放大

| 字段 | 内容 |
|------|------|
| 假设 | 先以小规模行动验证，再决定是否放大投入 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | CASE + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 SUPPORT） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | DECIDE 状态的风险降低建议 |
| 触发参考 | 目标过于乐观、资源紧绷、路径未经验证时。建议先小规模测试 |
| 什么情况下不应强行调用 | 当用户已经做过验证时——不重复建议。当项目本身就是小规模行动时——不需要再"先小规模" |

---

### C16：执行中发现新"结果"触发新周期

| 字段 | 内容 |
|------|------|
| 假设 | 执行中可能发现新的"结果"，触发新一轮逆向推导 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | CASE + AI-INFERENCE |
| VALIDATION-MATURITY | SINGLE-CASE（Case 02 SUPPORT：陈桃花角色涌现） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | S6 入口（执行中调整路线）的判断参考 |
| 触发参考 | 用户在执行中发现新的可能性或价值时。识别这是否触发新的策划周期 |
| 什么情况下不应强行调用 | 执行中的调整只是细节微调时——不触发新周期。用户明确表示不需要重新规划时——尊重用户判断 |

---

### C17：现实锚定

| 字段 | 内容 |
|------|------|
| 假设 | 现实锚定是否为独立策划原则 |
| ORIGIN | AI-AUTHORED |
| ENDORSEMENT | NONE |
| EVIDENCE-BASIS | DOC + AI-INFERENCE |
| VALIDATION-MATURITY | CROSS-CASE-PRELIMINARY（3 案例弱 SUPPORT） |
| 证据状态 | [默认启发式，可 override] |
| 产品角色 | JUDGE 状态的检查项 |
| 触发参考 | 检查结果是否锚定在现实中（预算/时间/能力/市场是否支撑） |
| 什么情况下不应强行调用 | 当用户已经提供了充分的现实约束信息时——不需要额外锚定检查。当项目处于纯创意探索阶段时——不过早引入现实约束 |

---

## 暂不进入 V1.0 的 8 条

> 以下条目在模型中存在，但未进入 V1.0 工作流。仅在 references 中保留记录，不得偷偷进入主流程。

| 编号 | 假设 | 不进入理由 |
|------|------|-----------|
| C2 | 资源链适用性 | 1 SUPPORT + 1 COUNTEREXAMPLE。已在 A7"允许跳级"设计中体现，不需要单独判断 |
| C8 | 按价值密度配置 | 过于具体（质量分配策略），通用性不足 |
| C10 | 涌现资产识别 | 与 C16 重叠 |
| C12 | 能力缺口作为战略输入 | 过于具体，产品价值不明显 |
| C15 | 不可牺牲的硬目标 | 单案例SUPPORT，触发条件不明确，Case 03 NOT-OBSERVED |
| C19 | 第一步行动锁定跨场景适用 | 第一步行动已作为硬约束（策划闭环必选项），不需要 C19 作为独立假设 |
| C20 | 长短期分层 | 单案例SUPPORT，过于具体，不是所有项目都有长期愿景 |
| C21 | 资源链非线性 | 已在 A7"允许跳级"设计中体现 |
