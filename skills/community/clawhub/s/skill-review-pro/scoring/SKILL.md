# scoring — 评分模型 / Scoring Model

skill-review-pro 的评分体系。总分 100 分，单阶段（静态审查）。

> **设计说明**：基于 37 个真实 Skill 评审数据分析，Phase 1 静态审查覆盖 94% 的真实问题。原 Phase 2 测试的精华（对抗检查）已并入 Reliability 维度。总分 100 分直接从静态审查得出。

## 评分维度 / Dimensions

### 一级维度 / Primary Dimensions

| 维度 / Dimension | 分值 / Points | 核心问题 / Core Question |
|---|---|---|
| Reliability / 可靠性 | 40 | Skill 能不能稳定、正确地完成任务？ |
| Engineering / 工程化 | 30 | 写得像工程规范还是 AI 套话？ |
| UX / 用户体验 | 24 | 使用者（人和 AI）用起来顺畅吗？ |
| Maintainability / 可维护性 | 6 | 后续迭代和扩展容易吗？ |

### 二级观察项 / Secondary Observation Signals

二级观察项**不直接参与打分**，作为证据归入对应一级维度：

| 二级观察项 / Signal | 归属维度 / Primary Dimension | 说明 / Description |
|---|---|---|
| Positioning Clarity / 定位清晰度 | Reliability | 能否快速理解 Skill 干什么、不做什么 |
| Instruction Clarity / 指令明确性 | Reliability | 指令有无歧义、矛盾、缺失 |
| Boundary Rationality / 边界合理性 | Reliability | 职责是否聚焦，有无膨胀 |
| Actionability / 可执行性 | Reliability | AI 能否据此行动（区分 Skill 和知识文章） |
| Adversarial Robustness / 对抗鲁棒性 | Reliability | 模糊输入/越界请求/矛盾请求时是否优雅处理 |
| Degradation Strategy / 降级策略 | Reliability | 依赖不可用或异常时有无 fallback |
| Engineering Quality / 工程质量 | Engineering | 结构组织、命名规范、格式一致性 |
| Practicability / 实用性 | Engineering | 真实场景下 AI 能否稳定执行 |
| Information Density / 信息密度 | UX | 信息量是否合理，不轰炸也不贫乏 |
| Interaction Pacing / 交互节奏 | UX | 暂停点是否合理，用户是否疲劳 |
| Modularity / 模块化程度 | Maintainability | 是否便于拆分、扩展、复用 |
| Structure Completeness / 结构完整性 | Maintainability | 核心模块是否齐全 |

### 维度去重 / Deduplication

**同一问题只在一个一级维度扣分。** 归属规则：

- "不知道它干啥" → Reliability
- "写得像 AI 套话" → Engineering
- "用起来太累" → UX
- "改起来很麻烦" → Maintainability

如果一个证据信号同时影响多个维度，在主维度扣分，其他维度用备注标注但不额外扣分。

---

## 动态权重 / Dynamic Weights

根据 Skill 类型（由主控路由模块识别），对应域的一级维度权重 ×1.5，其余 ×0.8。**不要自行推导归一化**，直接查下表。

### 预计算权重表 / Pre-calculated Weights

原始分值：Reliability=40, Engineering=30, UX=24, Maintainability=6（总分100）

| Skill 类型 | +权重维度 | 加权后 R, E, UX, M | 归一化后（总分100） |
|---|---|---|---|
| **engineering/coding** | Reliability, Engineering | 60, 45, 19.2, 4.8 | R=46, E=35, UX=15, M=4 |
| **cognition/teaching** | UX, Reliability | 60, 24, 36.0, 4.8 | R=48, E=19, UX=29, M=4 |
| **cognition/analysis** | Reliability, Engineering | 60, 45, 19.2, 4.8 | R=46, E=35, UX=15, M=4 |
| **workflow/planner** | Maintainability, Reliability | 60, 24, 19.2, 9.0 | R=54, E=21, UX=17, M=8 |
| **workflow/reviewer** | Reliability, UX | 60, 24, 36.0, 4.8 | R=48, E=19, UX=29, M=4 |
| **仅 base（未识别类型）** | 无 | 40, 30, 24.0, 6.0 | R=40, E=30, UX=24, M=6 |

### 使用方法 / How to Use

1. 识别 Skill 类型 → 从上表找到对应行
2. 按"归一化后"列的分数上限评分（如 engineering/coding 的 Reliability 满分 46）
3. 四个维度分数相加，总分 = 100
4. **严禁自行推导**：如果表中没有对应类型，使用"仅 base"行

### 计算方法（仅参考，不用于实际评分）

公式：`归一化分 = 加权分 × (100 / 加权总分)`
示例 engineering/coding：加权总分 = 60+45+14.4+9.6 = 129，R归一化 = 60 × (100/129) ≈ 46

---

## 评分锚点 / Scoring Anchors

**Reliability（40分 / 权重后 46-54）**
- 满分 = 定位清晰、指令无歧义、边界明确、可执行、有降级策略、对抗场景优雅处理
- 70% = 能理解且有边界，大部分场景可执行，但有 1-2 处指令不完整
- 40% = 经常跑偏或边界模糊，缺降级策略
- 15% = 不是真正的 Skill（知识文章伪装），无可执行指令

**Engineering（30分 / 权重后 34）**
- 满分 = 读起来像团队内部工程规范，结构清晰无 AI 套话，有具体可执行步骤
- 65% = 有结构但夹杂套话或格式不统一
- 30% = 大量空泛描述和口号，缺少具体指导
- 10% = 纯描述性内容，无可执行指令层

**UX（24分 / 权重后 15-29）**
- 满分 = 信息密度合理，暂停点恰当，重点突出，交互流畅
- 70% = 信息略多但可接受，交互基本顺畅
- 40% = 信息过密或节奏不当，用户容易疲劳
- 15% = 信息轰炸或过度简略，无交互设计

**Maintainability（6分 / 权重后 4-8）**
- 满分 = 模块化清晰，核心模块齐全，无硬编码，便于扩展
- 60% = 有基本结构但扩展需重写
- 25% = 巨石结构，改一处影响全局
- 5% = 硬编码/魔法值导致环境迁移崩溃

---

## 评分等级 / Grade Scale

| 分数 / Score | 图标 / Icon | 中文等级 | English Grade | 结论 / Conclusion |
|---|---|---|---|---|
| 90-100 | ⭐ | 优秀 | Excellent | 可直接发布 / Ready to publish |
| 75-89 | ✅ | 良好 | Good | 小幅改进后可发布 / Minor improvements needed |
| 60-74 | ⚠️ | 合格 | Adequate | 需要较多修改 / Significant improvements needed |
| <60 | ❌ | 不及格 | Fail | 建议重新设计 / Recommend redesign |

---

## Failure Taxonomy（高频问题类型）

> 基于 37 个真实 Skill 评审数据归纳。评审时如果发现这些问题，标注问题类型，帮助用户定位系统性弱点。

| 问题类型 / Type | 描述 / Description |
|---|---|
| **instruction-incomplete** | 指令有步骤但缺关键细节（fallback、边界、错误处理） |
| **knowledge-not-skill** | 知识文章伪装成 Skill，无可执行指令 |
| **boundary-missing** | 缺少"不做什么"的边界定义 |
| **no-degradation** | 依赖不可用或异常时无 fallback |
| **format-inconsistency** | 多文件间 schema/命名/格式冲突 |
| **hardcoded-config** | 路径/ID/版本写死，环境迁移后崩溃 |
| **instruction-redundant** | 指令存在功能性重复（同一要求出现多次且无新增信息）。**判定规则**：先判断两段文字的**目标受众**和**功能目的**是否相同——如果受众不同（如一段给人看、一段给 agent 执行）或功能不同（如一段定义规则、一段展示示例），则**不是重复**；只有当两段文字对同一受众传达相同要求、AI 读后会产生混淆或矛盾时，才标记为 `instruction-redundant` |
