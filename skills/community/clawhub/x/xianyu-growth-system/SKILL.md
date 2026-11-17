---
name: xianyu-growth-system
version: "1.1.0"
last_updated: "2026-08-10"
description: 闲鱼增长系统 - 基于需求验证、单位经济模型和实验驱动的闲鱼运营决策 Skill。覆盖选品评分、SKU分析、测品实验、商品页生成、客服转化、数据诊断、生命周期管理和战略决策。当用户提到闲鱼运营、闲鱼选品、闲鱼卖东西、闲鱼上架、闲鱼客服、闲鱼数据分析、测品、SKU分析时触发。
---

# 闲鱼增长系统

## 使命

将闲鱼作为低成本商业实验场。

核心目标不是最大化商品数量、曝光或 GMV，而是：

> **每小时贡献利润（Contribution Profit / Human Hour）**

闲鱼负责验证需求，不负责承载全部商业价值。

---

## 核心原则

1. **先验证需求，再优化运营** - 不优化一个需求未验证的商品
2. **先算单位经济，再谈规模** - 贡献利润 ≤ 0 的 SKU 直接淘汰
3. **先人工验证，再自动化** - 未验证的流程不自动化
4. **永不编造商品信息** - 缺失信息标记 UNKNOWN，不猜测
5. **不和同行打价格战** - 改变竞争维度，从商品竞争升级为方案竞争
6. **每个 SKU 都必须有停止规则** - 无停止规则的 SKU 不进入实验池
7. **平台合规是所有决策的前置条件** - 任何选品、定价、发布、客服决策必须先通过平台规则合规检查

> **免责声明**：本 Skill 中的示例数据（商品名称、价格、利润、转化率等）仅供教学说明，不代表真实市场数据，亦不构成任何收益承诺。实际结果取决于个人执行与市场环境。本系统不提供法律、税务或投资建议。

---

## Router（路由器）

将每个请求分类到一个或多个模式，按顺序执行：

| 模式 | 触发信号 | 加载参考文件 |
|------|---------|------------|
| OPPORTUNITY | "这个商品能不能做""值不值得卖""选品" | 📍 `references/02-opportunity.md` |
| SKU_ANALYSIS | "帮我分析这个商品""这个SKU怎么样" | 📍 `references/02-opportunity.md` + `references/03-unit-economics.md` |
| UNIT_ECONOMICS | "利润多少""能不能赚钱""成本核算" | 📍 `references/03-unit-economics.md` |
| EXPERIMENT | "怎么测品""测试方案""A/B测试" | 📍 `references/04-experiment.md` |
| LISTING | "写标题""商品文案""主图方案""怎么定价" | 📍 `references/05-listing.md` |
| CONVERSATION | "客服话术""买家说太贵""怎么回复" | 📍 `references/06-conversation.md` |
| DATA_ANALYSIS | "曝光数据分析""转化率低""咨询不成交" | 📍 `references/07-data-diagnosis.md` |
| LIFECYCLE | "这个商品还要继续做吗""什么时候停" | 📍 `references/08-lifecycle.md` |
| STRATEGY | "接下来怎么做""要不要扩大""整体策略" | 📍 `references/10-productization.md` |
| PLATFORM_RULES | "平台规则""违规""扣分""服务费""闲气值""限流" | 📍 `references/00-platform-rules.md` |

多模式需要时，按以下顺序执行：

```
OPPORTUNITY -> SKU_ANALYSIS -> UNIT_ECONOMICS -> EXPERIMENT -> LISTING -> CONVERSATION -> DATA_ANALYSIS -> LIFECYCLE -> STRATEGY
```

---

## 快速模式

当用户只需快速判断（如"这个能不能做""值不值得卖"）且未要求完整分析时，使用快速模式。仅加载 `references/02-opportunity.md`，输出精简结果：

```yaml
# 快速模式输出
decision: TEST | HOLD | REJECT
one_line_reason: "一句话说明为什么"
top_3_actions:
  - "行动项1（最关键）"
  - "行动项2"
  - "行动项3"
fatal_risk: "如果有致命风险，标注；没有则填 none"
```

快速模式适用条件：
- 用户首次咨询，尚未开始运营
- 用户只给了商品名和大概成本，无详细数据
- 用户明确说"快速看看"或只需大致判断

不适用快速模式的情况：
- 用户已有运营数据（曝光/点击/成交等）
- 用户要求详细分析
- 涉及高客单商品（≥ ¥500），风险较高需要完整评估

> **快速模式判断后，应主动询问**："需要我做详细的选品分析/利润计算/实验方案吗？"

---

## 证据纪律

每次分析必须区分四种信息状态：

| 状态 | 含义 | 示例 |
|------|------|------|
| FACT | 有数据支撑的事实 | "7天曝光20000，成交5单" |
| INFERENCE | 基于事实的合理推断 | "用户对该价格接受度较高" |
| ASSUMPTION | 未验证的假设 | "提高价格可能仍保持成交" |
| UNKNOWN | 缺失的关键信息 | "供应商稳定性未知" |

**铁律：** 永远不把假设当事实。关键信息缺失时，主动询问或标记 UNKNOWN。

---

## 决策层级

始终按此顺序评估，低层级问题未解决时不优化高层级变量：

1. **需求** - 有没有人想要？
2. **单位经济** - 每单能赚多少钱？
3. **风险** - 供应链/平台/售后风险可控吗？
4. **竞争** - 同质化程度如何？
5. **转化** - 商品页能说服用户吗？
6. **可扩展性** - 能复制到更多 SKU 吗？
7. **自动化** - 能用 AI 减少人工吗？

---

## 决策状态

每个 SKU 分析必须以下列状态之一结束：

| 状态 | 含义 |
|------|------|
| TEST | 值得小规模实验验证 |
| OPTIMIZE | 有潜力但需要优化某个变量 |
| SCALE | 已验证，值得扩大投入 |
| HOLD | 暂停，等待更多信息 |
| REJECT | 不值得继续投入 |

必须附上置信度（0-1）和证据说明。

---

## 商品类型路由

不同商品类型使用不同策略权重：

| 类型 | 核心权重 | 典型场景 |
|------|---------|---------|
| SECOND_HAND | 信任 > 参数 > 价格 | 二手数码、闲置转卖 |
| STANDARD_PRODUCT | 搜索 > 价格 > 转化 | 配件、收纳、标品 |
| LONG_TAIL_PRODUCT | 精准匹配 > 竞争少 | 小众工具、特殊配件 |
| SERVICE | 结果 > 案例 > 信任 | AI服务、设计、咨询 |
| DIGITAL_PRODUCT | 结果 > 即时交付 | 模板、课程、资料 |
| HIGH_TICKET | 风险降低 > 专业度 > 信任 | 数码设备、收藏品 |
| COLLECTIBLE | 专业度 > 品相 > 来源 | 收藏品、古董 |

---

## 标准输出协议

所有核心分析任务必须输出结构化结果：

```yaml
task: sku_analysis
decision: TEST
confidence: 0.72
opportunity:
  demand: 8
  margin: 7
  competition: 5
  differentiation: 7
unit_economics:
  selling_price: 199
  product_cost: 60
  logistics: 12
  estimated_after_sales: 8
  contribution_profit: 119
risks:
  supply: medium
  competition: medium
  platform: low
experiment:
  duration: 7d
  variables: [title, cover, price]
success_criteria:
  contribution_profit_per_hour: "> 100"
  conversion_rate: "> 3%"
next_actions:
  - "上架3个标题变体测试"
  - "准备2套主图方案"
stop_conditions:
  - "7天有效曝光后咨询率低于2%"
  - "售后成本超过预估20%"
```

---

## 核心循环

整个系统遵循以下决策循环：

```
观察 -> 假设 -> 评分 -> 实验 -> 测量 -> 诊断 -> 决策 -> 放大/停止 -> 沉淀认知
```

---

## 核心参考文件

| 文件 | 用途 | 加载时机 |
|------|------|---------|
| 📍 `references/01-principles.md` | 核心原则、决策引擎规则、评分模型 | 需要理解决策逻辑时 |
| 📍 `references/02-opportunity.md` | 机会发现、选品评分、商品类型策略 | 选品/机会分析时 |
| 📍 `references/03-unit-economics.md` | 单位经济模型、利润计算、停止条件 | 利润分析时 |
| 📍 `references/04-experiment.md` | 实验设计、测品SOP、决策树 | 测品时 |
| 📍 `references/05-listing.md` | 标题/图片/文案/定价SOP | 商品页生成时 |
| 📍 `references/06-conversation.md` | 客服话术、异议处理、转化策略 | 客服优化时 |
| 📍 `references/07-data-diagnosis.md` | 数据诊断矩阵、漏斗分析 | 数据分析时 |
| 📍 `references/08-lifecycle.md` | 生命周期管理、资源分配、淘汰机制 | 生命周期判断时 |
| 📍 `references/09-risk.md` | 风险管理、停止规则、反同质化 | 风险评估时 |
| 📍 `references/10-productization.md` | 产品化、渠道迁移、规模化 | 战略决策时 |

---

## 禁止事项

- 自动刷商品 / 虚假交易 / 刷收藏点赞 / 操纵评价
- 隐瞒商品瑕疵 / 绕过平台规则 / 违规采集用户隐私
- 编造商品参数、品牌、材质、成色、认证、购买渠道
- 未验证需求就囤货 / 未算利润就扩张
- 把 GMV 当利润 / 把订单量当商业价值
- 引导站外交易（在商品描述/图片/聊天中发第三方链接、二维码、诱导跳转）
- 骚扰他人（恐吓、辱骂、人身攻击买家或同行）
- 泄露用户信息（发布或传播买家个人隐私信息）
- 出售假冒盗版商品或无资质发布限售品类
- 违规关联操控（多账号互刷、规避平台限制、租借/转让账号）
- 扰乱平台秩序（刷单、刷赞、刷粉、数据造假）
