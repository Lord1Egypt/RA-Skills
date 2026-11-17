---
name: success-business-review
description: "Use when a customer is in the post-sales customer-success phase and the rep+CS need to run a recurring business review / value review meeting (QBR/EBR) with the customer's decision-makers — align goals & baseline pre-meeting, score progress evidence red/yellow/green in-meeting, set next-quarter joint plan, and plant renewal/expansion/referral triggers post-meeting. Triggers: '业务回顾', '复盘', 'QBR', 'EBR', '季度回顾', '价值回顾', '续约前复盘', '客户回顾会', 'quarterly business review', 'executive business review', 'value review'. Do NOT use for one-time first-value proof, single sales-call debrief, internal project retrospective, or the renewal/expansion/referral negotiation itself (downstream success-renewal-management / success-expansion / success-referral-generation; this skill only plants triggers + hands off)."
license: MIT
version: 0.0.1
tags: [sales, customer-success, post-sales, qbr, ebr, china, b2b, 业务回顾, 复盘, 续约]
---

# 业务回顾·复盘（success-business-review）

## Overview

客户上线、首价值证明之后，定期与客户做业务回顾会议（QBR/EBR），证明持续价值、对齐下期目标、识别续约/增购/转介绍机会。**业务回顾不是产品使用汇报，是对齐目标 → 核证据判红黄绿 → 设下期 joint plan → 埋触发点**。

边界（详见 frontmatter）：新客首价值证明的一次性收尾（其价值定义/基线/证据/叙事能力在本场景复用）、单次销售沟通复盘、内部项目复盘沉淀、续约/增购/转介绍本身（下游场景，本 skill 只埋触发点+交接指针）。

## 主线：定目标 → 核证据判红黄绿 → 建叙事 → 设 joint plan → 埋钩子 → 内部 prep+leakage

### 一、定回顾目标与受众（会前）

对齐 **1-3 个关键价值指标**（outcomes 不是 activities）+ baseline + 上轮承诺清单 + 中国决策层三层：一把手（战略级 EBR，看 Strategic 层）/ 分管副总（季度 QBR，看 Operational 层）/ 部门负责人+执行层+champion（看 Tactical 层）。

**先闭环上轮**：会前拉上轮承诺清单逐条标状态（delivered/partial/not delivered/descoped），会上先报上轮再提新 work——上轮没认账，这轮没人信。无 baseline = 按首价值证明流程补齐，或上线 30 天内回推+客户确认。无 telemetry 替代见 `references/china-adaptation.md`。

### 二、核进展证据判红黄绿（会中核心）

**层 1 — 承诺逐条四态**（不软化）：delivered（兑现）/ partial（标缺口）/ not delivered（**我方原因认我方原因**，不全推客户依赖）/ descoped by agreement（双方同意调范围）。

**层 2 — success definition 三档**：on_track（绿，进度 ≥70%，正常埋钩子）/ at_risk（黄，30-70% 或阻塞，救计划优先，**不埋 expansion**）/ not_measurable_yet（**第 3 次仍是 = 测量问题，升红**）。

**5 可信度规则**（详见 `references/progress-scoring.md`）：① 坏季度写坏季度（客户 lived it，读「delivered」失信任）；② 不编造（无 source 无 number，Proof Gate）；③ outputs ≠ outcomes；④ 我方原因认我方原因；⑤ not_measurable_yet 第 3 次 = 测量问题升红。

每条证据带 6 维元数据（source/as-of/baseline/current/confidence/attribution + 客户是否接受）。证据 5 级可信度沿用首价值证明五级法。私有化无 telemetry → 业务侧手动数据（审批时长/工单数/人天/合规事件）+ 微信/企微截图作客户原话。

**健康度五维 Green/Yellow/Red**（内部用，**客户面用「目标达成度」红黄绿，不打分给客户看**）：决策层出席率/会前准备/会上参与度/跟进响应率/上轮 action 完成率。

### 三、建价值叙事（会中）

价值三层层级，**聚焦上两层**：Strategic（业务结果/政绩/对标 → 一把手/分管副总）/ Operational（效率/降本/合规避险 → champion）/ Tactical（功能采用 → 执行层）/ Base（不报）。**按受众抬一层**（人民币+业务语言：降本增效/合规避险/政绩/对标，少用海外「board ROI」）。**60% future / 40% past**（政企政绩感平衡）。**单 headline metric**：每版只挑一个最能概括价值的数字当头条。详见 `references/value-narrative.md`。

### 四、设下期 joint plan（会中）

**≤3 commitments**，每个带：date + 双方 owner + agreement state 四态（draft / proposed / agreed[**有 confirmation evidence 才算 committed**] / changed）。单方 owner = 项目计划非合伙；超过 3 个 = 没抓重点。模板见 `references/joint-action-plan.md`。

### 五、埋续约/增购/转介绍触发点（会后）

**含蓄化**（中国含蓄文化，会上埋点不直 ask，会后单独推进）：

- **续约预演**：success plan 进度过半 + 续约前 60-90 天 → 交接 `success-renewal-management`。
- **增购**：**on_track 才埋**；at_risk 跳过（救计划优先）并记原因；客户主动问新场景/使用量超预期 → 交接 `success-expansion`。
- **转介绍**：**客户关系温度计=热/铁** + on_track + 同行业相似需求 → 交接 `success-referral-generation`。ask 靠会后饭局/单独沟通。

**客户关系温度计**（替代 referenceable 字段）：冷（仅业务对接）/温（有私下交流）/热（主动认可+引荐意愿）/铁（愿做标杆）。详见 `references/downstream-hooks.md`。

### 六、内部 prep brief + leakage check（贯穿）

**内部 prep brief**（CSM 独享，不入客户件）：account brief / 活跃风险信号（带证据）/ 扩张 framing / 竞争情报 / stakeholder dynamics（谁在会议室、角色、已知立场）/ talking points / **landmines**（未决工单/已知不满/政治敏感）。

**leakage check**（发客户件前必做）：unsupported attribution / confidential commentary / internal-only data / overstatement / 内部风险语言——查到删。**人工 approval gate** 才发客户件。结构+清单见 `references/internal-prep-and-leakage-check.md`。

## 判定标准（交什么）

1. **会前**：一页纸预发材料 + 微信版摘要（<200 字，1 数字+1 客户认可+1 下步）+ 内部 prep brief。
2. **会上**：客户面精简 deck（60-min agenda：Opening 5 / 业务背景 10 / 价值回顾 15 / 战略讨论 20 / 行动计划 8 / 收尾 2）。
3. **会后**：QBR 复盘文件（YAML：success_definition_status / commitments_delivered/missed / health / 触发点 / next_review + body：承诺兑现/成功定义/下期计划/客户依赖/触发点/下次日期）+ action tracker（≤3 commitments w/ date+owner+agreement state）+ 下游 skill 交接指针。

交付时给用户：1) 复盘文件+红黄绿判定理由；2) 证据覆盖率与类型分布；3) 触发点清单+交接说明；4) 待确认问题（最多 3 个）。

## 常见坑（归因式反例）

| 念头/做法 | 后果 |
|---|---|
| 把产品使用数据当价值报给决策层 | 决策层听不懂、不认账，复盘变功能汇报 |
| 坏季度写成好季度 / 估算当确认 / 泛 ROI 无基线 | 客户 lived it 一查翻车，被 CFO 戳穿，信任崩+续约/增购/转介绍全烧 |
| 会上直 ask 续约/增购/转介绍 | 中国含蓄文化伤关系，ask 没挣来反显功利 |
| 只报过去不报未来 / 只报未来不闭环上轮 | 上轮没认账=信任崩；未来没规划=变流水账 |
| 内部风险语言泄露进客户件 | 政企敏感，leakage 一次信任崩，后续邀不到决策层 |
| not_measurable_yet 用到第 3 次复盘 | 早期诚实晚期 evasive，success definition 虚设 |
| 一份叙事给所有受众 / 6 页 deck 给政企副总 / 假定有完整 telemetry | 使用层虚、决策层没耐心、私有化无替代证据，复盘卡死 |
| 复盘完不埋钩子 / health score 打分给客户看 | 续约时被动重解释价值；客户不接受被「打分」 |

## References

- `references/review-cadence-and-timeline.md` — T-28~T+3 时间线 + cadence + 60-min agenda
- `references/progress-scoring.md` — 承诺四态 + success 三档 + 5 可信度规则 + 证据 6 维 + 健康度五维
- `references/value-narrative.md` — 价值三层层级 + 按受众 3 版叙事 + headline metric + 无 telemetry 替代
- `references/joint-action-plan.md` — ≤3 commitments + agreement state 四态 + confirmation evidence
- `references/downstream-hooks.md` — 触发点含蓄化 + 门槛 + 客户关系温度计 + 下游交接
- `references/china-adaptation.md` — 决策层三层 + 无 telemetry 替代 + 微信汇报 + 合规适配 + 验收挂钩
- `references/internal-prep-and-leakage-check.md` — 内部 prep brief + leakage check + approval gate
