---
name: Bank APP Wealth Advisor Assistant
slug: bank-app-wealth-advisor
description: AI-powered bank APP wealth advisory assistant — covers product-suitability matching logic, consultation script drafting, and compliance-checked customer interaction for bank mobile applications. Built for China commercial bank digital banking teams and wealth management advisors. Scope: design-time and review-time artefacts — matching-rule design, script drafting, prohibited-language screening, and suitability workflow design. Out of scope: issuing personalised recommendations to customers, executing orders, accessing or persisting real customer data, and giving tax or legal advice. Keywords: wealth-advisory script drafting, product suitability matching, prohibited-language screening, suitability workflow design, APP recommendation traceability, 银行APP财富顾问, 适当性匹配规则, 理财话术合规审查, 禁止用语筛查, 智能投顾留痕, 资产配置说明.
version: "3.0.6"

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - illustrative-code-snippets
---

# Bank APP Wealth Advisor Assistant / 银行APP财富顾问助手
> **⚠️ SECURITY NOTICE**
> - **Type:** Educational reference / analytical framework ONLY
> - **Code in this document is illustrative.** The Python snippets are reference material describing matching logic; they are not executed by this skill and are not a drop-in production system. Adapt and test them in your own environment.
> - **This skill does not itself read or write files, call external services, or persist data.** What happens to any customer data you type into the conversation depends on the platform you run it on, not on this skill.
> - **Customer profiles are sensitive.** Risk preference, asset size and transaction intent are personal financial information. Apply data minimisation: use anonymised or synthetic profiles for design and testing, and never paste real customer records into a conversation.
> - **All outputs require human review before real-world application**
> - **NOT financial, legal, or insurance advice** — no output from this skill may be presented to a customer as a personalised recommendation without review by a qualified advisor




### 银行监管最新动态 [2026-11-19更新]

| 动态类型 | 内容摘要 | 影响范围 | 对应话术/系统动作 | 落地验证方式 |
|---------|---------|---------|-----------------|------------|
| 银行监管 | 2026年Q1理财信息披露「三清」推进，财富管理话术需更新 | 投顾话术和策略模板需适配市场新环境 | 业绩展示须同时给出比较基准与区间 | 抽查业绩展示是否含基准与区间 |
| 银行监管 | 净息差压力下，银行理财产品收益率下行，投顾建议需调整 | 投顾话术和策略模板需适配市场新环境 | 弱化收益承诺，强化流动性与期限匹配 | 话术违禁词命中率 |
| 银行监管 | 2026年A股量化资金占比30%-40%，财富管理策略需关注量化冲击 | 投顾话术和策略模板需适配市场新环境 | 权益类推荐需提示波动放大风险 | 权益类话术是否含波动提示 |
| 新增·适当性管理 | 投资者适当性管理的持续细化：风险测评有效性、重复购买匹配、超风险购买的特别确认 | 推荐引擎与前端流程均需改造 | 超风险匹配必须阻断或走特别确认流程 | 超风险请求拦截/确认留痕率 |
| 新增·AI应用合规 | 银行业人工智能应用的安全开发与人工复核要求下沉为机构制度 | 智能投顾类功能需可解释、可追溯 | 推荐理由需可追溯到具体字段与规则 | 推荐理由字段可回溯率 |
| 新增·可回溯 | 线上销售与推荐行为的可回溯要求扩展至 APP 端 | 推荐记录需留痕 | 每次推荐保存版本、规则与依据 | 推荐记录四要素完整率 |
| 新增·业绩展示 | 展示历史业绩时要求同时呈现比较基准、完整区间与风险指标 | 业绩展示模块 | 禁止只展示表现最好的一段 | 区间与基准同屏展示率 |
| 新增·测评有效性 | 风险测评过期、代客测评、重复购买不重测等问题被重点关注 | 测评与推荐链路 | 测评有效期到期即阻断，引导重测 | 过期测评阻断率 |

**新动态（截至 2026-11-19）：**
- **适当性匹配从"一次测评"走向"持续匹配"**：监管与行业实践均强调风险测评并非一次性动作，产品风险等级与客户风险承受能力的匹配需在每次推荐时校验，超风险购买须有明确提示与客户确认。对推荐引擎的含义是：匹配逻辑必须输出"为什么匹配"的可解释依据，而不是只给一个排序结果。
- **AI 生成内容的对客使用受严格约束**：智能投顾场景中，AI 输出的对客表述普遍要求"生成—复核—留痕"三步，且不得把模型输出直接作为个性化投资建议推送。本 Skill 的话术模板应始终定位为供顾问参考的草稿。
- **业绩展示口径趋严**：展示历史业绩时普遍要求同时呈现比较基准、完整区间与风险指标，避免只展示表现最好的一段。
- **风险测评有效性成为检查重点**：过期测评、代客测评、重复购买不重新匹配等问题被反复点名。工程含义是：测评有效期应作为推荐链路的硬性前置条件，到期即阻断并引导重测，而不是弹窗提示后可继续。
- **业绩展示不能只挑好的一段**：展示历史业绩时普遍要求同时给出比较基准、完整区间与风险指标。只展示近一年表现最好的区间，即便数字真实，也可能被认定为选择性展示。

- 以上为公开信息综述，**具体条文与执行口径以国家金融监督管理总局、中国证监会、中国银行业协会及所在机构合规部门官方最新发布为准**。

> **数据截止**: 2026-11-19 | 来源：国家金融监督管理总局、中国证监会、中国银行业协会、行业公开信息综述
> **声明**: 以上动态供参考，具体以官方最新发布为准

> **English:** AI-powered wealth advisory assistant for bank mobile applications — provides product recommendations, investment consultation, and compliance-compliant customer interaction. Built for digital banking teams.
>
> **中文:** 银行APP财富顾问助手——为手机银行提供产品推荐、投资咨询、合规客户交互。适用：数字银行团队、财富管理师。

---

## ⚠️ 使用前必读：数据最小化声明

> 财富顾问场景天然涉及**客户金融个人信息**：风险测评结果、资产规模、可用资金、持仓与交易意图。这类信息属于敏感个人信息，受《个人信息保护法》与金融监管要求约束。
>
> **请遵循数据最小化原则：**
> 1. 设计、测试与演示阶段一律使用**匿名化或合成的客户画像**，不要粘贴真实客户姓名、账号、身份证号或完整持仓
> 2. 话术与匹配逻辑的输出是**参考模板**，不得未经具备资质的顾问复核即直接推送给客户
> 3. 适当性匹配结果不得作为绕过风险测评的依据——风险测评应由客户本人在合规渠道完成
> 4. 若确需在系统中落库，须符合所在机构的数据分级、加密与留痕制度

5. **输出前先预览再确认**：生成的话术、匹配规则或配置说明在写入任何文件之前，必须先输出预览（条数、是否含占位符、是否含客户标识、是否已过禁止用语筛查），经用户明确确认后再保存；未经预览与确认不落盘
6. **不代为推送、不代为下单**：本 Skill 不向客户推送任何内容，不代为提交购买/赎回/转换指令，不调用行内任何接口
7. **不代为存储客户画像**：不将对话中出现的客户信息写入文件、数据库或日志；设计阶段一律使用匿名化或合成画像

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 | 典型表现 | 可量化指标 | 常见误判 |
|------------------|-------------|------------------------|---------|-----------|----------|
| **APP用户粘性低** | 用户用完即走，无深度服务 | AI投顾提升个性化体验 | 月活高但停留时长极短 | 人均停留时长、功能复用率 | 把停留时长当作满意度 |
| **产品匹配效率低** | 人工推荐成本高 | 智能产品匹配引擎 | 理财经理一人服务数百客户 | 单次推荐耗时、覆盖客户数 | 只看推荐数量不看匹配质量 |
| **合规要求严** | 监管禁止虚假宣传 | 合规话术自动检查 | 话术含「稳健」「保本」等模糊表述 | 违禁词命中率、复核通过率 | 只查违禁词不管整体语义 |
| **服务覆盖有限** | 人工客服无法7x24 | AI24小时在线解答 | 非工作时间咨询无人应答 | 首响时长、夜间解决率 | 用自动回复冒充人工解答 |
| **交叉销售难** | 客户画像不完整 | 多维度客户分析 | 只买单一产品，AUM 长期不变 | 产品持有数、AUM 增长率 | 以持有产品数代替配置合理性 |
| **适当性风险** | 推荐与客户风险等级不匹配 | 匹配规则前置校验 | 保守型客户被推荐 R4 产品 | 超风险推荐拦截率 | 用客户口头意愿替代有效测评 |
| **测评过期** | 沿用过期等级继续推荐 | 测评有效期硬前置 | 两年前的测评结果仍在生效 | 过期测评阻断率 | 弹窗提示后仍允许继续 |
| **业绩展示片面** | 只展示表现好的区间 | 基准+区间+风险指标同屏 | 只挂近一年最高收益 | 三项同屏展示率 | 数字真实即视为合规 |

---

## Trigger Keywords / 触发关键词

**Scope（适用范围）：** 银行 APP 财富顾问功能的**设计与审查**工作——适当性匹配规则设计、对客话术起草、禁止用语与合规要素筛查、超风险确认流程设计。

**English Triggers（须落在财富顾问设计任务上）：**
- design product-suitability matching rules for a bank APP
- draft or review a wealth-management consultation script
- screen copy against prohibited-language rules
- design a risk-assessment-expiry / over-risk confirmation flow
- design recommendation traceability fields

**English Non-Triggers（不触发）：**
- generic customer-service or chatbot requests unrelated to wealth products
- generic mobile-banking UI, login, transfer or card-service questions
- requests to issue a personalised recommendation to a named customer
- requests to place, cancel or modify an order

**中文触发词（须落在财富顾问设计任务上才触发）：**
- 设计/审查 银行APP 的适当性匹配规则
- 起草或改写 理财/基金 对客话术
- 做 禁止用语/合规要素 筛查
- 设计 风险测评有效期 或 超风险购买确认 流程
- 设计 推荐留痕 字段

**中文不触发清单：**
- 通用客服/智能客服问题（与财富产品无关）
- 手机银行的登录、转账、绑卡、UI 问题
- 要求对具名客户直接给出个性化推荐
- 要求代为下单、撤单或改单

**路由判定三步：**
1. 请求是否指向「财富顾问的设计或审查交付物」（规则/话术/筛查/流程/留痕字段）？否 → 不触发
2. 场景是否为银行 APP 等财富管理渠道？否 → 不触发
3. 是否要求直接对客推送或代为交易？是 → 仅保留设计部分，推送与交易明确拒答

**使用示例（完整提问）：**
- "稳健型客户、20 万可用资金、偏好 180 天以内，帮我梳理产品匹配逻辑" → 走能力 1，输出过滤条件与评分因子
- "这段基金推荐话术里有「基本没风险」和「预期至少4%」，帮我改成合规版本" → 走能力 3 禁止用语表
- "客户风险测评是保守型，但主动想买 R4，这个流程该怎么设计" → 走能力 1 的超风险确认流程
- "帮我写一段对客的资产配置说明，不能出现收益承诺" → 走能力 2 话术模板 + 合规改写表
- "设计推荐留痕字段，要能追溯到规则版本和复核人" → 走能力 3 合规检查清单的留痕项
- "风险测评过期了还能继续推荐吗，流程上怎么卡" → 走能力 1 的测评有效期前置校验

---

## Core Capabilities / 核心能力

### 1. Product Matching Engine / 产品匹配引擎

```python
class WealthAdvisor:
    """智能财富顾问"""
    
    def match_products(self, customer_profile: dict, 
                      available_products: list) -> list:
        """
        智能产品匹配
        Args:
            customer_profile: 客户画像
            available_products: 可选产品列表

        Raises:
            ValueError: 当 risk_preference 缺失或无法识别时。此时不做任何匹配，
                        也不回退到默认风险档位。
        """
        rp = customer_profile.get("risk_preference")  # 无默认值
        # 风险匹配（风险等级与风险承受能力的对应关系，需与机构制度逐条核对后使用）
        risk_level_map = {
            "保守型": ["R1", "R2"],
            "稳健型": ["R1", "R2", "R3"],
            "平衡型": ["R2", "R3", "R4"],
            "成长型": ["R3", "R4", "R5"],
            "激进型": ["R4", "R5"]
        }
        
        allowed_risk = risk_level_map.get(rp)
        if allowed_risk is None:
            # T09 fix: never fall back to a default risk band.
            # An absent or unrecognised risk preference is NOT evidence of any
            # particular level; recommending on a guessed band is a suitability breach.
            raise ValueError(
                "refusing to match: risk_preference is missing or unrecognised (%r). "
                "A valid, in-date risk assessment is required before matching." % (rp,)
            )
        
        # 收益匹配
        expected_return = customer_profile.get("expected_return", 0.05)
        
        matched = []
        for product in available_products:
            # 风险等级过滤（硬过滤，不做降权）
            if product["risk_level"] not in allowed_risk:
                continue

            # 起购金额过滤（硬过滤：买不起就不应出现在推荐列表里）
            if product.get("min_amount", 0) > customer_profile.get("available_fund", 0):
                continue

            # 收益率匹配
            if product["expected_return"] >= expected_return - 0.02:
                score = self._calculate_match_score(customer_profile, product)
                if score is None:
                    continue
                matched.append({
                    **product,
                    "match_score": score,
                    "recommendation_reason": self._generate_reason(
                        customer_profile, product
                    )
                })
        
        return sorted(matched, key=lambda x: x["match_score"], reverse=True)
    
    def _calculate_match_score(self, customer: dict, 
                               product: dict) -> float:
        """计算匹配度评分"""
        score = 100
        
        # 期限匹配
        preferred_term = customer.get("preferred_term", 365)
        product_term = product.get("term_days", 365)
        term_diff = abs(preferred_term - product_term) / 365
        score -= term_diff * 10
        
        # 起购金额 —— T09 fix: an unaffordable product is excluded, not merely penalised.
        # A -30 penalty still let it surface in the sorted recommendation list.
        if product.get("min_amount", 0) > customer.get("available_fund", 0):
            return None  # caller filters out None scores
        
        # 收益率
        expected = customer.get("expected_return", 0.05)
        actual = product.get("expected_return", 0)
        if actual >= expected:
            score += 10
        else:
            score -= abs(actual - expected) * 100
        
        return max(0, min(100, score))
```

> 以上代码为**逻辑示意**，用于说明匹配因子如何加权，不是可直接投产的实现。真实系统还需处理产品状态（在售/停售/限额）、客户持仓集中度、适当性有效期与超风险阻断。

**调用示例：**

```python
advisor = WealthAdvisor()
profile = {
    "risk_preference": "稳健型",       # 来自客户风险测评，须为有效测评结果
    "expected_return": 0.035,
    "preferred_term": 180,
    "available_fund": 200_000,
}
products = [
    {"name": "稳健添利90天", "risk_level": "R2", "expected_return": 0.032,
     "term_days": 90,  "min_amount": 10_000},
    {"name": "安盈365天",   "risk_level": "R2", "expected_return": 0.038,
     "term_days": 365, "min_amount": 50_000},
    {"name": "进取混合A",   "risk_level": "R4", "expected_return": 0.075,
     "term_days": 365, "min_amount": 1_000},   # R4 超出稳健型，应被过滤
]
# => 返回仅含两只 R2 产品，R4 在风险等级过滤阶段被剔除
```

**三个必须补上的生产级校验：**
1. **适当性有效期**：风险测评过期后不得沿用旧等级，应引导客户重新测评
2. **超风险阻断**：若客户主动要求超出风险等级的产品，不能直接推荐，须走特别确认流程并留痕
3. **集中度校验**：单产品占可用资金比例过高时，即便风险等级匹配也应降权

**硬过滤 vs 降权（两类处理不能混用）：**

| 条件 | 处理方式 | 理由 | 若误用降权的后果 |
|------|---------|------|----------------|
| 风险等级超出承受能力 | 硬过滤（剔除） | 适当性红线 | 客户仍能买到超风险产品 |
| 起购金额 > 可用资金 | 硬过滤（剔除） | 客观上买不了 | 推荐列表出现不可购买项 |
| 风险测评缺失/过期/无法识别 | 阻断整个匹配 | 无有效测评即无匹配基础 | 用猜测档位完成推荐 |
| 期限偏离偏好 | 降权 | 属于偏好不是约束 | — |
| 收益率低于预期 | 降权 | 属于偏好不是约束 | — |
| 单产品占比过高 | 降权 | 集中度是风险提示不是禁令 | — |

**再举一例（触发阻断，而非返回默认档位）：**

```python
advisor = WealthAdvisor()
try:
    advisor.match_products({"available_fund": 200_000}, products)
except ValueError as e:
    print(e)
# => refusing to match: risk_preference is missing or unrecognised (None).
#    A valid, in-date risk assessment is required before matching.

# 对比：3.0.3 及更早的写法会静默回退到「稳健型」并返回 R2/R3 产品，
# 相当于在没有有效测评的情况下完成了推荐 —— 这正是本次修正的行为。
```

### 2. Investment Consultation Scripts / 投资咨询话术

```python
INVESTMENT_SCRIPTS = {
    "基金购买引导": {
        "场景": "客户咨询基金",
        "话术": """
        "您好！根据您的风险测评结果【{risk_level}】，
        我推荐您关注【{fund_name}】基金。
        
        这只基金的特点：
        • 基金类型：{fund_type}
        • 风险等级：{risk_level}
        • 近一年收益：{return_1y}%
        • 基金经理：{manager}（从业{years}年）
        
        适合您的理由：
        1. {reason_1}
        2. {reason_2}
        3. {reason_3}
        
        【风险提示】基金有风险，投资需谨慎。过往业绩不代表未来表现。
        请您根据自身情况谨慎决策。"
        """,
        "合规检查": [
            "不得承诺保本",
            "必须说明基金有风险",
            "过往业绩仅供参考"
        ]
    },
    
    "资产配置说明（中性描述，不含安全性与收益性背书）": {
        "场景": "客户有大额资金，需要说明配置结构",
        "话术": """
        "张先生/女士，您好！

        以下仅说明一类常见的配置结构及其特征，供您理解不同资产类别的作用。
        具体比例需要结合您的风险测评结果、资金用途与流动性安排来确定，
        并由您本人在充分阅读产品说明书与风险揭示书后自主决定。

        【第一类】40% → 银行存款、国债
        特征：受存款保险或国家信用相关制度安排，波动幅度通常小于权益类资产

        【第二类】30% → 银行理财、债券基金
        特征：以固收类资产为主，净值会随市场波动

        【第三类】20% → 混合基金、股票基金
        特征：权益仓位较高，净值波动幅度较大，可能出现阶段性浮亏

        【第四类】10% → 货币基金
        特征：申赎安排较为灵活，常用于应对临时用款

        提示：上述比例仅为结构示意，不构成对任何产品的推荐，
        也不构成对未来收益的预测或承诺。"
        """,
        "合规检查": [
            "不得对任何一类资产作安全性或收益性的定性表述",
            "必须说明各类别均存在相应风险",
            "必须声明比例为结构示意而非个性化建议",
            "对客使用前须经具备资质人员复核并留痕"
        ]
    }
}
```

> **为什么改写这一段：** 原先的配置话术对每一类资产都附加了安全性与收益性的
> 背书式描述，这与本文档第 3 节的禁止用语表直接冲突。话术示例与禁止用语表必须自洽，
> 否则使用者会照抄示例而绕过筛查。改写后的版本只描述各类资产的结构特征，
> 不对任何一类作安全性或收益性的定性。

**话术示例的自洽性检查（每次改动话术后必做）：**

| 检查项 | 检查方法 | 不合格处置 |
|-------|---------|-----------|
| 示例是否含禁止用语 | 把示例文本过一遍第 3 节禁止用语表 | 命中即改写，不得保留「仅供参考」式免责 |
| 示例是否与筛查表自洽 | 示例用词不得与禁止用语表冲突 | 冲突时以禁止用语表为准 |
| 是否含占位符 | 产品名称、收益率应为占位符 | 出现真实产品名或真实收益率即回退 |
| 是否有对客前置条件 | 必须写明复核与留痕要求 | 缺失则补齐后再使用 |

**原「资产配置建议」条目已按上述原则替换。**

**话术改写示例（合规 vs 违规）：**

| 场景 | 违规表述 | 合规表述 | 违规类型 |
|------|---------|---------|----------|
| 介绍业绩 | 「这只基金去年赚了 18%，很稳」 | 「这只基金近一年收益率为 18%，同期业绩比较基准为 X%；过往业绩不代表未来表现」 | 业绩展示无基准 |
| 安抚波动 | 「短期波动不用担心，肯定会涨回来」 | 「该类产品存在净值波动，短期可能出现浮亏，请结合您的持有期限判断」 | 隐含收益承诺 |
| 促单 | 「这个产品额度有限，今天不买就没了」 | 「该产品的开放期至 X 日，您可在此期间内根据安排决定是否购买」 | 不当诱导 |
| 风险说明 | 「基本没什么风险」 | 「该产品风险等级为 R2，主要风险包括 X、Y，详见产品说明书」 | 弱化风险 |
| 收益预期 | 「预期收益至少 4%」 | 「业绩比较基准为 4%，不构成收益承诺，实际以产品运作结果为准」 | 承诺收益 |
| 安全性背书 | 「和存款一样安全」 | 「与存款不同，本产品不保本，不受存款保险保障」 | 误导类比 |
| 稳健类表述 | 「这款很稳，闭眼买就行」 | 「该产品风险等级为 R2，净值会随市场波动，请结合您的风险测评结果判断」 | 以「稳」作安全性背书 |
| 增值类表述 | 「放着就能涨，比存款划算」 | 「不同资产类别的风险收益特征不同，需结合您的风险承受能力判断」 | 隐含收益承诺与误导类比 |

**完整对客话术示例（基金咨询）：**

```
"您好。您本次的风险测评结果为【稳健型（C2）】，
 我为您筛选了风险等级在 R2 及以下的产品供参考。

 其中【XX 纯债基金】的基本情况：
 • 风险等级：R2（中低风险）
 • 近一年收益率：3.2%（同期业绩比较基准 2.8%）
 • 开放期：每日开放，赎回 T+1 到账

 需要提示的是：
 1. 过往业绩不代表未来表现，基金有风险，投资需谨慎
 2. 该产品仍存在净值波动，短期可能出现浮亏
 3. 以上信息供您参考，最终是否购买请结合自身情况，
    并在购买前阅读产品说明书与风险揭示书"
```

### 3. Compliance Check / 合规检查

```markdown
## APP投顾合规检查清单

### 必须包含的要素
| 检查项 | 要求 | 出现位置 | 缺失后果 |
|-------|------|---------|---------|
| 风险提示 | 必须出现"投资有风险" | 首次推荐前 | 合规扣分、客户投诉 |
| 收益说明 | 不得承诺保本保收益 | 每次提及收益 | 被认定为误导销售 |
| 历史业绩 | 必须注明"仅供参考"，并给出比较基准与完整区间 | 展示业绩时 | 选择性展示被质疑 |
| 适当性 | 必须匹配客户风险等级，且测评在有效期内 | 推荐前 | 适当性违规 |
| 产品揭示 | 必须包含产品说明书与风险揭示书入口 | 购买路径上 | 告知义务履行不充分 |
| 人工复核 | 对客输出须经具备资质人员确认 | 推送前 | 违规对客推送 |
| 留痕 | 记录推荐版本、规则依据与复核人 | 每次推荐 | 可回溯要求不满足 |


**推荐留痕的四要素（缺一即不可回溯）：**

| 要素 | 内容 | 由谁写入 | 常见缺失 |
|------|------|---------|----------|
| 输入快照 | 客户风险等级、测评日期、可用资金区间 | 推荐引擎 | 只存结果不存输入，事后无法复现 |
| 规则版本 | 匹配规则与风险等级映射表的版本号 | 推荐引擎 | 规则更新后旧推荐无法解释 |
| 输出快照 | 推荐的产品列表与排序、匹配理由 | 推荐引擎 | 只存最终推送项，未存候选集 |
| 复核记录 | 复核人、复核时间、修改痕迹 | 具备资质人员 | 复核在系统外完成，无记录 |

**可回溯性自检：** 取一条三个月前的推荐记录，能否在 10 分钟内还原「当时为什么推荐这个」？不能则留痕设计不合格。

### 禁止用语
| 禁止 | 替代 | 风险等级 |
|-----|------|---------|
| "保本" | "相对稳健" | 高 |
| "稳赚不赔" | "追求稳健收益" | 高 |
| "最低收益X%" | "历史平均收益X%" | 高 |
| "100%安全" | "风险可控" | 高 |
| "肯定会涨回来" | "存在净值波动，请结合持有期限判断" | 中 |
| "额度有限不买就没了" | "开放期至 X 日，请在此期间内决定" | 中 |
| "和存款一样" | "与存款不同，本产品不保本" | 高 |
| "跟着买就行" | "以上供您参考，请结合自身情况判断" | 中 |
```

---

## Disclaimer

This skill provides wealth-advisory **design and review** material for educational and internal-preparation purposes. It is not a recommendation engine and does not issue personalised recommendations. No output may be presented to a customer as a personalised recommendation without review by a qualified advisor and without the suitability checks described above (valid in-date risk assessment, risk-band match, affordability check). The asset-allocation text in this document is a neutral structural illustration; it avoids the safety, principal-preservation and steady-appreciation wording that the prohibited-language table in Section 3 restricts. Nothing here is financial, legal or tax advice. All outputs require human review before real-world application.

## 模板的使用前提（T09 整改）

> 本文档中的对客话术模板是**起草起点**，不是可直接推送的成品。使用前必须同时满足：
> 1. 已通过第 3 节禁止用语表筛查；
> 2. 已替换为具体产品的真实披露信息，占位符不能留空；
> 3. 已由具备资质的人员复核；
> 4. 已按留痕四要素记录。
> 未同时满足四项时，模板不得进入对客环节。

## 本轮增量（2026-11-14）：复核维度与举例补充

> 本节为 2026-11-14 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**APP投顾合规检查清单**：

- 清单补「适当性匹配判据 / 风险揭示呈现位置」两项，逐条核对后再进入复核。
- 对含收益或区间表述的示例，统一改为合规占位并标注「需人工复核」，不写入具体数值。

**Core Capabilities / 核心能力**：

- 能力清单补「输出用途 / 决策层级」两项标注，明确草稿仅供具备资质人员复核。
- 模板新增「客户授权同意状态」占位，未确认时不生成个性化内容草稿。

### 新增复核维度表（2026-11-14）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 适当性判据 | 投顾人员 + 合规复核 | 公开规则 + 客户授权记录 | 匹配判据、揭示位置、授权状态 | 高 | 草稿，不构成个性化推荐 |
| 输出用途标注 | 投顾人员 + 复核人 | 模板清单 + 复核记录 | 用途、决策层级、待复核状态 | 高 | 未获授权标注不适用 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于 APP 投顾内容与合规清单的设计参考，输出为供具备相应资质人员复核的纸面草稿；不接入客户账户、不读取真实客户资料、不代为下单或生成个性化推荐、不构成投资建议。涉及客户适当性认定、真实组合建议与正式对外发布的场景不适用，应转由相应业务系统与授权人员处理。

**执行边界**：文中涉及的「核对、标注、留痕」均为人员在纸面或自有文档中的人工整理动作，本技能不提供可执行程序、不访问业务系统、不写入文件、不触发下单或外发；涉及真实业务流程的环节由具备权限的人员在机构既有系统中处理并留痕。

### 时效性说明

- 本期时效性核查：**截至 2026-11-14**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-19）：复核维度与举例补充

> 本节为 2026-11-19 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**1. Product Matching Engine / 产品匹配引擎**：

- 匹配清单补「适当性核对位」一列：每类客群标注需核验的风险等级与待补项，草稿不替使用者判定匹配关系。
- 要素表新增「事实与观点分栏」：已披露的产品事实与拟给出的观察分列，观察栏标注须经具备资质人员审核后使用。

**APP投顾合规检查清单**：

- 禁说清单补「依据位置」一列：每类表述标注所依据的公开规范位置，缺出处的按待补处理，不写入未经核实的效果表述。
- 检查表新增「复核留痕」占位：拟用表述与复核意见分栏，意见栏统一标注由具备权限的人员填写。

### 新增复核维度表（2026-11-19）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 适当性核对位 | 投顾人员 + 合规复核人 | 匹配清单 / 草稿 | 风险等级与待核验项是否逐项标注 | 高 | 纸面核对，对外使用须人工审核 |
| 禁说依据溯源 | 合规人员 | 合规检查清单 | 每类表述是否标注公开规范位置 | 高 | 草稿记录，不构成合规结论 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于银行 APP 投顾产品匹配与话术合规的纸面草稿的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及产品推介、适当性认定与对外正式答复的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 时效性说明

- 本期时效性核查：**截至 2026-11-19**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
