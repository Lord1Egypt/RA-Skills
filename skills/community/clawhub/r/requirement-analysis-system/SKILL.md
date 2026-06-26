# 需求分析技能系统 (Requirement Analysis Skills)

> 版本：v0.1.0  
> 创建：2026-03-09  
> 适用：产品经理、售前工程师、需求分析师

---

## 📦 技能包概览

本技能系统包含 **12 个核心技能**，覆盖需求分析全流程：

```
┌─────────────────────────────────────────────────────────┐
│  需求分析技能系统 (Requirement Analysis Skills)          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  需求发现 (Discovery)                                    │
│  ├── problem-statement (问题定义)                        │
│  ├── proto-persona (用户画像)                            │
│  ├── customer-journey-map (旅程地图)                     │
│  └── jobs-to-be-done (JTBD 分析)                          │
│                                                          │
│  需求分析 (Analysis)                                     │
│  ├── problem-framing-canvas (问题框架)                   │
│  ├── opportunity-solution-tree (机会方案树)              │
│  └── company-research (客户调研)                         │
│                                                          │
│  优先级判断 (Prioritization)                             │
│  ├── prioritization-advisor (优先级框架选择)             │
│  ├── feature-investment-advisor (功能投资决策)           │
│  └── finance-based-pricing-advisor (定价分析)            │
│                                                          │
│  需求输出 (Output)                                       │
│  ├── user-story (用户故事)                               │
│  ├── epic-hypothesis (史诗假设)                          │
│  └── prd-development (PRD 开发)                           │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 技能详情

### 一、需求发现 (Discovery)

#### 1. problem-statement（问题定义）
**类型**: Component  
**用途**: 从用户视角清晰定义问题  
**核心框架**: 同理心驱动的问题陈述

**触发场景**:
- 新项目启动，需要明确问题
- 需求模糊，需要澄清
- 团队对问题理解不一致

**输出**:
```markdown
# 问题陈述

## 用户是谁
[角色描述]

## 用户想做什么
[任务/目标]

## 什么在阻碍他们
[痛点/障碍]

## 为什么这是问题
[影响/后果]

## 用户感受如何
[情绪状态]
```

**OpenClaw 适配**:
```markdown
---
name: problem-statement
description: 从用户视角定义问题，使用同理心驱动的问题陈述框架
tags: [requirement, problem-framing, user-centric]
license: MIT
---
```

---

#### 2. proto-persona（用户画像）
**类型**: Component  
**用途**: 快速创建假设性用户画像  
**核心框架**: 假设驱动的 Persona

**触发场景**:
- 缺乏用户研究数据
- 需要快速对齐目标用户
- 项目早期阶段

**输出**:
```markdown
# Proto-Persona

## 基本信息
- 姓名：[虚构但典型]
- 角色：[职位/身份]
- 背景：[相关经历]

## 目标与动机
- 主要目标：[1-3 个]
- 动机：[为什么重要]

## 痛点与挑战
- 当前痛点：[1-3 个]
- 阻碍因素：[什么在阻止他们]

## 行为特征
- 使用场景：[何时/何地]
- 技能水平：[新手/专家]
```

---

#### 3. customer-journey-map（客户旅程地图）
**类型**: Component  
**用途**: 可视化用户与品牌的完整互动过程  
**核心框架**: NNGroup 旅程地图

**触发场景**:
- 优化用户体验
- 识别体验断点
- 跨渠道体验设计

**输出**:
```markdown
# Customer Journey Map

## 旅程阶段
| 阶段 | 行为 | 触点 | 情绪 | 机会点 |
|------|------|------|------|--------|
| 认知 | ...  | ...  | ...  | ...    |
| 考虑 | ...  | ...  | ...  | ...    |
| 购买 | ...  | ...  | ...  | ...    |
| 使用 | ...  | ...  | ...  | ...    |
| 忠诚 | ...  | ...  | ...  | ...    |

## 关键洞察
- 峰值体验：[最高情绪点]
- 低谷体验：[最低情绪点]
- 关键触点：[影响力最大的触点]
```

---

#### 4. jobs-to-be-done（JTBD 分析）
**类型**: Component  
**用途**: 深度挖掘用户真实需求  
**核心框架**: JTBD 理论

**触发场景**:
- 需求表面化，需要深挖
- 创新机会探索
- 产品定位调整

**输出**:
```markdown
# Jobs To Be Done

## 功能性工作
- 用户想完成什么任务：[具体、可操作]

## 社会性工作
- 用户想在他人眼中如何：[身份/地位]

## 情感性工作
- 用户想感受什么：[情绪状态]

## 痛点
- 当前方案的不足：[1-5 个]

## 期望收益
- 理想方案的特点：[1-5 个]
```

---

### 二、需求分析 (Analysis)

#### 5. problem-framing-canvas（问题框架画布）
**类型**: Interactive  
**用途**: 结构化问题探索  
**核心框架**: MITRE Problem Framing Canvas

**触发场景**:
- 复杂问题需要系统分析
- 多方利益相关者
- 需要避免认知偏见

**引导问题**:
```
1. Look Inward（向内看）
   - 你的假设是什么？
   - 你的偏见可能是什么？
   - 你希望结果是什么？

2. Look Outward（向外看）
   - 谁会受影响？
   - 现有数据告诉我们什么？
   - 类似问题的解决方式？

3. Reframe（重新定义）
   - 问题可以如何重新表述？
   - 是否有更根本的问题？
   - 如果不解决会怎样？
```

**输出**:
```markdown
# Problem Framing Canvas

## 问题陈述
[清晰、无偏见的问题描述]

## 利益相关者
[受影响的人群/组织]

## 现有证据
[数据/研究/观察]

## 假设
[需要验证的假设]

## 成功标准
[如何判断问题已解决]
```

---

#### 6. opportunity-solution-tree（机会方案树）
**类型**: Interactive  
**用途**: 从目标到方案的系统拆解  
**核心框架**: Teresa Torres OST

**触发场景**:
- 多个需求需要优先级排序
- 需要探索多种解决方案
- 目标 - 方案链路不清晰

**引导流程**:
```
1. 定义目标成果
   - 业务目标是什么？
   - 如何衡量成功？

2. 识别机会（问题）
   - 什么在阻碍目标达成？
   - 用户有哪些未满足需求？

3. 生成方案
   - 可能的解决方案有哪些？
   - 每个方案如何解决对应机会？

4. 设计实验
   - 如何验证方案有效性？
   - 最小验证成本是多少？
```

**输出**:
```markdown
# Opportunity Solution Tree

## 目标成果
[明确的、可衡量的目标]

## 机会层
- 机会 1: [问题/需求]
  - 方案 1.1: [解决方案]
  - 方案 1.2: [解决方案]
  
- 机会 2: [问题/需求]
  - 方案 2.1: [解决方案]
  - 方案 2.2: [解决方案]

## 优先级实验
- 实验 1: [验证方案 1.1]
- 实验 2: [验证方案 2.1]
```

---

#### 7. company-research（客户调研）
**类型**: Component  
**用途**: 深度分析目标客户公司  
**核心框架**: 企业画像 + 决策链分析

**触发场景**:
- B2B 售前支持
- 大客户开发
- 定制化解决方案

**输出**:
```markdown
# Company Research Report

## 公司基本信息
- 行业：[细分行业]
- 规模：[人数/营收]
- 发展阶段：[初创/成长/成熟]

## 业务模式
- 核心产品：[是什么]
- 目标客户：[服务谁]
- 收入来源：[如何赚钱]

## 数字化现状
- 现有技术栈：[主要系统]
- 数字化水平：[评估]
- 近期项目：[相关 initiative]

## 决策链
- 决策者：[姓名/职位/关注点]
- 影响者：[姓名/职位/关注点]
- 使用者：[姓名/职位/关注点]

## 痛点与机会
- 核心痛点：[1-3 个]
- 潜在机会：[1-3 个]
```

---

### 三、优先级判断 (Prioritization)

#### 8. prioritization-advisor（优先级框架选择）
**类型**: Interactive  
**用途**: 选择最适合的优先级框架  
**核心框架**: 多框架自适应推荐

**触发场景**:
- 需求过多需要优先级排序
- 不确定用哪个框架
- 团队对优先级有争议

**引导问题**:
```
1. 产品阶段
   - 0-1 探索期
   - 1-10 成长期
   - 10-100 成熟期

2. 团队规模
   - 小团队 (<10 人)
   - 中团队 (10-50 人)
   - 大团队 (>50 人)

3. 数据可用性
   - 无数据（靠假设）
   - 部分数据（定性为主）
   - 充足数据（定量支持）

4. 决策压力
   - 低（可以慢慢讨论）
   - 中（需要在周内决定）
   - 高（今天必须决定）
```

**推荐框架**:
| 场景 | 推荐框架 | 理由 |
|------|---------|------|
| 0-1+ 无数据 | ICE/RICE | 快速试错，量化假设 |
| 成长期 + 部分数据 | Kano/价值复杂度 | 平衡用户满意度与投入 |
| 成熟期 + 充足数据 | WSJF/机会成本 | 经济模型驱动 |
| 高压力决策 | MoSCoW/强制排序 | 快速达成共识 |

---

#### 9. feature-investment-advisor（功能投资决策）
**类型**: Interactive  
**用途**: 评估功能投资的 ROI  
**核心框架**: 收益 - 成本 - 风险三维分析

**触发场景**:
- 大功能需要立项审批
- 资源有限需要取舍
- 需要向管理层证明价值

**引导问题**:
```
1. 收益评估
   - 收入影响：[直接/间接/无]
   - 用户影响：[多少用户受益]
   - 战略价值：[是否符合方向]

2. 成本评估
   - 开发成本：[人天估算]
   - 运维成本：[持续投入]
   - 机会成本：[放弃什么]

3. 风险评估
   - 技术风险：[实现难度]
   - 市场风险：[用户接受度]
   - 执行风险：[团队能力]
```

**输出**:
```markdown
# Feature Investment Analysis

## 收益评分 (1-10)
- 收入影响：[分数] + [依据]
- 用户影响：[分数] + [依据]
- 战略价值：[分数] + [依据]
- **收益总分**: [平均分]

## 成本评分 (1-10, 越低越好)
- 开发成本：[分数] + [依据]
- 运维成本：[分数] + [依据]
- 机会成本：[分数] + [依据]
- **成本总分**: [平均分]

## 风险评分 (1-10, 越低越好)
- 技术风险：[分数] + [依据]
- 市场风险：[分数] + [依据]
- 执行风险：[分数] + [依据]
- **风险总分**: [平均分]

## 投资建议
[Build / Don't Build / Need More Data]

## 关键假设
[需要验证的假设列表]
```

---

#### 10. finance-based-pricing-advisor（定价分析）
**类型**: Interactive  
**用途**: 基于财务影响的定价决策  
**核心框架**: 定价 - 财务模型联动

**触发场景**:
- 新功能定价
- 价格调整评估
- 套餐设计优化

**输出**:
```markdown
# Pricing Decision Analysis

## 当前状态
- ARPU/ARPA: [当前值]
- 转化率：[当前值]
- 流失率：[当前值]
- NRR: [当前值]

## 定价变更影响
| 指标 | 当前 | 乐观 | 保守 | 悲观 |
|------|------|------|------|------|
| ARPU | $X  | $X+20% | $X+10% | $X-5% |
| 转化率 | Y% | Y-10% | Y-20% | Y-30% |
| 流失率 | Z% | Z+5% | Z+10% | Z+20% |
| NRR  | W% | W+3% | W+1% | W-2% |

## 财务影响
- 月度收入影响：[+$X / -$X]
- 年度收入影响：[+$X / -$X]
- 回本周期：[X 个月]

## 建议
[Go / No-Go / Need Test]
```

---

### 四、需求输出 (Output)

#### 11. user-story（用户故事）
**类型**: Component  
**用途**: 将需求转化为可执行的开发任务  
**核心框架**: Mike Cohn 用户故事 + Gherkin 验收标准

**触发场景**:
- 需求准备进入开发
- 需要与研发团队对齐
- 敏捷迭代规划

**输出**:
```markdown
# User Story: [简短标题]

## 故事描述
作为 [角色]
我想要 [完成什么任务]
以便于 [获得什么价值]

## 验收标准 (Gherkin 格式)
### 场景 1: [正常流程]
Given [前提条件]
When [执行动作]
Then [预期结果]

### 场景 2: [异常流程]
Given [前提条件]
When [执行动作]
Then [预期结果]

### 场景 3: [边界情况]
Given [前提条件]
When [执行动作]
Then [预期结果]

## 技术备注
- [技术考虑点]
- [依赖关系]
- [性能要求]

## 设计资源
- [设计稿链接]
- [原型链接]
```

---

#### 12. epic-hypothesis（史诗假设）
**类型**: Component  
**用途**: 将大型需求转化为可验证假设  
**核心框架**: If/Then 假设结构

**触发场景**:
- 大型功能/项目立项
- 需要验证价值假设
- 敏捷史诗定义

**输出**:
```markdown
# Epic Hypothesis: [史诗名称]

## 假设陈述
**如果** 我们 [做什么/提供什么功能]  
**为了** [目标用户/客户群体]  
**那么** 他们会 [产生什么行为/结果]  
**我们将通过** [指标/信号] **来验证成功**  
**成功标准是** [具体数值/阈值]

## 背景与依据
- 市场洞察：[为什么认为这是机会]
- 用户研究：[用户反馈/数据支持]
- 竞争分析：[竞品情况]

## 关键指标
| 指标类型 | 指标名称 | 基线 | 目标 | 当前 |
|----------|----------|------|------|------|
| 结果指标 | [如留存率] | X% | Y% | - |
| 过程指标 | [如使用率] | A% | B% | - |

## 验证实验
- 实验 1: [最小验证方式]
- 实验 2: [进一步验证]

## 风险与假设
- 关键假设：[需要验证的假设]
- 主要风险：[可能的失败原因]
```

---

#### 13. prd-development（PRD 开发）
**类型**: Workflow  
**用途**: 端到端的 PRD 创建流程  
**核心框架**: 结构化 PRD + 多技能编排

**触发场景**:
- 正式产品/功能立项
- 需要跨团队对齐
- 需要评审和归档

**工作流**:
```
1. 问题定义 (problem-statement)
   ↓
2. 用户研究 (proto-persona + customer-journey)
   ↓
3. 需求分析 (problem-framing + OST)
   ↓
4. 优先级排序 (prioritization-advisor)
   ↓
5. 方案定义 (user-story + epic-hypothesis)
   ↓
6. 成功标准 (metrics definition)
   ↓
7. PRD 整合 (final document)
```

**输出**:
```markdown
# Product Requirements Document (PRD)

## 1. 文档信息
| 项目 | 内容 |
|------|------|
| 产品名称 | [名称] |
| 版本 | v1.0 |
| 创建日期 | YYYY-MM-DD |
| 最后更新 | YYYY-MM-DD |
| 负责人 | [姓名] |
| 状态 | [草稿/评审中/已批准] |

## 2. 背景与目标
### 2.1 问题陈述
[从用户视角描述问题]

### 2.2 业务目标
- 目标 1: [可衡量的业务目标]
- 目标 2: [可衡量的业务目标]

### 2.3 用户目标
- 用户是谁：[目标用户]
- 用户需求：[核心需求]

## 3. 需求范围
### 3.1 In Scope
- 功能 1: [描述]
- 功能 2: [描述]

### 3.2 Out of Scope
- 不包含 1: [描述]
- 不包含 2: [描述]

## 4. 用户故事
### 4.1 用户故事地图
[用户故事地图或链接]

### 4.2 优先级排序
| 优先级 | 用户故事 | 验收标准 |
|--------|----------|----------|
| P0     | [故事 1] | [标准 1] |
| P0     | [故事 2] | [标准 2] |
| P1     | [故事 3] | [标准 3] |

## 5. 功能规格
### 5.1 功能 1 详情
- 描述：[详细说明]
- 交互流程：[流程图/原型链接]
- 技术考虑：[技术要点]

### 5.2 功能 2 详情
[同上]

## 6. 成功标准
### 6.1 产品指标
| 指标 | 基线 | 目标 | 测量方式 |
|------|------|------|----------|
| [指标 1] | X | Y | [方式] |
| [指标 2] | A | B | [方式] |

### 6.2 业务指标
| 指标 | 基线 | 目标 | 测量方式 |
|------|------|------|----------|
| [指标 1] | X | Y | [方式] |

## 7. 发布计划
### 7.1 里程碑
| 阶段 | 日期 | 交付物 |
|------|------|--------|
| 需求评审 | YYYY-MM-DD | PRD 定稿 |
| 开发完成 | YYYY-MM-DD | 功能完成 |
| 测试完成 | YYYY-MM-DD | 测试报告 |
| 正式发布 | YYYY-MM-DD | 上线 |

### 7.2 发布策略
- 发布范围：[全量/灰度/内测]
- 灰度比例：[10% → 50% → 100%]
- 回滚计划：[如果失败如何回滚]

## 8. 风险与依赖
### 8.1 技术风险
- 风险 1: [描述] + [缓解措施]
- 风险 2: [描述] + [缓解措施]

### 8.2 依赖关系
- 依赖 1: [团队/系统] + [期望日期]
- 依赖 2: [团队/系统] + [期望日期]

## 9. 附录
- 用户研究报告：[链接]
- 竞品分析报告：[链接]
- 设计稿：[链接]
- 技术架构图：[链接]
```

---

## 🔧 OpenClaw 集成方案

### 方案 A: 单技能多模式（推荐）

创建一个 `requirement-analysis` 技能，通过模式切换：

```markdown
---
name: requirement-analysis
description: 需求分析全流程技能系统，覆盖需求发现/分析/优先级/输出
tags: [product-management, requirement-analysis, prd]
license: MIT
---

# 需求分析技能系统

## 可用模式

### discovery（需求发现）
- problem-statement
- proto-persona
- customer-journey-map
- jobs-to-be-done

### analysis（需求分析）
- problem-framing-canvas
- opportunity-solution-tree
- company-research

### prioritization（优先级判断）
- prioritization-advisor
- feature-investment-advisor
- finance-based-pricing-advisor

### output（需求输出）
- user-story
- epic-hypothesis
- prd-development

## 使用方式

```
/requirement-analysis discovery problem-statement "用户反馈注册流程复杂"
/requirement-analysis analysis ost "提升新用户激活率"
/requirement-analysis prioritization "12 个需求如何排序"
/requirement-analysis output prd "移动审批功能"
```
```

---

### 方案 B: 独立技能包

创建 13 个独立技能，按目录组织：

```
skills/
└── requirement-analysis/
    ├── 01-discovery/
    │   ├── problem-statement/
    │   ├── proto-persona/
    │   ├── customer-journey-map/
    │   └── jobs-to-be-done/
    ├── 02-analysis/
    │   ├── problem-framing-canvas/
    │   ├── opportunity-solution-tree/
    │   └── company-research/
    ├── 03-prioritization/
    │   ├── prioritization-advisor/
    │   ├── feature-investment-advisor/
    │   └── finance-based-pricing-advisor/
    └── 04-output/
        ├── user-story/
        ├── epic-hypothesis/
        └── prd-development/
```

---

### 方案 C: 工作流编排

创建一个 Workflow Skill，自动编排多个技能：

```markdown
---
name: requirement-workflow
description: 端到端需求分析工作流，从问题定义到 PRD 输出
type: workflow
---

# 需求分析工作流

## 阶段 1: 问题定义 (10-15 分钟)
1. 运行 problem-statement
2. 运行 proto-persona
3. 输出：问题定义文档

## 阶段 2: 需求探索 (30-60 分钟)
1. 运行 customer-journey-map 或 jobs-to-be-done
2. 运行 problem-framing-canvas
3. 输出：需求分析报告

## 阶段 3: 方案设计 (30-60 分钟)
1. 运行 opportunity-solution-tree
2. 运行 prioritization-advisor
3. 输出：方案选项 + 优先级

## 阶段 4: 需求输出 (60-90 分钟)
1. 运行 user-story（针对 P0 需求）
2. 运行 epic-hypothesis（针对大型功能）
3. 输出：用户故事 + 史诗假设

## 阶段 5: PRD 整合 (30-60 分钟)
1. 整合所有输出
2. 运行 prd-development
3. 输出：完整 PRD
```

---

## 📊 与 PreSales AI 集成

### 集成点 1: 需求分析 Agent

在 PreSales AI 工作台中：

```
客户需求 → 需求分析 Agent → 结构化需求清单
                              ↓
                    调用 requirement-analysis 技能
                              ↓
                    - problem-statement
                    - customer-journey-map
                    - opportunity-solution-tree
```

### 集成点 2: 方案生成 Agent

```
结构化需求 → 方案生成 Agent → 完整解决方案
                              ↓
                    调用 prioritization-advisor
                    调用 feature-investment-advisor
                              ↓
                    - 优先级排序
                    - ROI 分析
```

### 集成点 3: 原型设计 Agent

```
方案 → 原型设计 Agent → 可交互原型
                        ↓
              调用 user-story
              调用 epic-hypothesis
                        ↓
              - 用户故事地图
              - 功能假设定义
```

---

## 🎯 实施路线图

### Phase 1: 核心技能 (Week 1-2)
- [ ] problem-statement
- [ ] user-story
- [ ] prioritization-advisor
- [ ] prd-development

### Phase 2: 分析技能 (Week 3-4)
- [ ] problem-framing-canvas
- [ ] opportunity-solution-tree
- [ ] customer-journey-map
- [ ] epic-hypothesis

### Phase 3: 决策技能 (Week 5-6)
- [ ] feature-investment-advisor
- [ ] finance-based-pricing-advisor
- [ ] company-research

### Phase 4: 工作流编排 (Week 7-8)
- [ ] requirement-workflow（端到端编排）
- [ ] 与 PreSales AI 集成
- [ ] 文档和示例

---

## ✅ 质量标准

每个技能必须包含：
- [ ] 清晰的触发场景
- [ ] 结构化的输出模板
- [ ] 引导式问题（Interactive 类型）
- [ ] 使用示例
- [ ] 与其他技能的关联

---

*适配 OpenClaw 标准：2026-03-09*
