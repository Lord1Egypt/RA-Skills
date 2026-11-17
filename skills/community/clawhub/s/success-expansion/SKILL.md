---
name: success-expansion
description: "Use when a customer is already live and producing value, and the rep+CS need to identify account-expansion opportunities (upsell / cross-sell / seat / new-module / new-department) from usage and organizational signals, build a structured expansion case, run the expansion conversation, and hand off to renewal or downstream deal flow. Triggers: '增购', '向上销售', '交叉销售', '加坐席', '升级套餐', '加模块', '账户拓展', 'upsell', 'cross-sell', 'land and expand', 'NRR'. Do NOT use for new-logo acquisition, renewal itself (success-renewal-management), pricing negotiation (clinch-negotiation-pricing), contract signing, or first-value proof (its usage data is INPUT here)."
license: MIT
version: 0.0.1
tags: [sales, customer-success, expansion, upsell, cross-sell, china, b2b, 增购, NRR]
---

# 增购（success-expansion）

## Overview

存量账户上线、产生价值后，帮销售/CS 从用量与组织信号里识别「现在能买更多」的账户，把信号转化为可执行的增购案（加坐席/升级套餐/加模块/跨产品线/跨部门拓展），推进增购对话到成交并衔接续约。核心一句话：**增购不是「所有客户都可能买更多」，是可观测信号触发 + 有可卖产品 + 账户健康，三者同时成立才算机会**。

边界（详见 frontmatter description）：新客首单获客、续约本身（success-renewal-management）、报价谈判（clinch-negotiation-pricing）、合同签署、首价值证明（其用量数据是本场景输入）。

## 主线：识别信号 → 建增购案 → 评分排序 → 增购对话 → 衔接续约/下游

### 一、识别拓展信号 — 7 类触发器 + 中国信号源

逐类扫描，**trigger 触发 AND 有对应可卖产品 AND 账户健康**才算机会（三者缺一不算）。7 类：用量到顶 / 功能差距 / 新团队部门 / 公司增长 / 战略举措 / 竞品替换 / 服务支持。每类对应增购类型（升级套餐/加坐席/加模块/跨部门/竞品替换/服务）。

**关键边界**：underutilization（采用率 <50%）是 activation 不是 upsell；账户在 land-adopt-expand ladder 未到 adopt 段不 expand。

**中国信号源**：telemetry 有则用后台；私有化无 telemetry 用业务侧手动数据 + 客户确认；组织信号看朋友圈/微信群企微/招聘网站/工商/招标平台。全清单与无 telemetry 替代法见 `references/expansion-signals.md`。

### 二、建增购案 — opportunity record + 阈值判定 + POC 路径

每个命中的机会建结构化记录：ID/类型/描述 + 证据≥3（标可信度，assumed 禁入）+ current→proposed state + 收益测算（`(加坐席×单价×12)+模块年费+tier差价`，标保守-进取区间）+ timing + stakeholder 三层 + risks/dependencies。

**stakeholder 三层**（中国决策链）：使用层（champion）→ 业务层（部门负责人）→ 决策层（分管副总/CFO）。

**金额阈值判定**（中国差异化）：超该客户招标阈值（政企/国企常见 30-100 万）→ 标记「需招标」→ 进入合同签署与招标流程，timing 调整招标周期。

**POC→增购路径**（中国企业级常见）：新模块/新坐席先 POC（2-4 周 + 成功标准 + 转单触发点）→ 价值验证 → 转单。全字段模板与阈值判定见 `references/opportunity-record.md`。

### 三、评分排序 — 双轨交叉校验

**主轨·三维**（1-10）：Revenue Potential + Effort（10=最易）+ Likelihood。复合分 = `Revenue×0.40 + Effort×0.30 + Likelihood×0.30`。

**校验轨·五因子 0-100**：用量到顶(25)+增长触发(20)+功能请求(15)+关系健康(20)+时机契合(20)。

**5 档**：Hot(8-10/75-100,立即追) / Warm(6-7.9/50-74,本季) / Nurture(4-5.9/25-49,培育) / Wait(2-3.9/0-24,监控)。两轨不一致取低档；关系健康=0 直接降档。评分细则见 `references/scoring.md`。

### 四、增购对话 — 按 signal 开口 + 三层推进 + 异议应对

**开场按 signal 分类**（非通用话术）：用量到顶→肯定增长+点容量临顶；功能请求→连到升级能力；公司增长→祝贺+问团队结构；新部门→共建跨部门用例；竞品替换→讲整合经济性不贬竞品；power user→高阶功能。全开场模板见 `references/expansion-conversation.md`。

**推进分支**：向上销售（同产品线升级：升级套餐/加坐席/加模块，讲 capacity 解锁+POC 降门槛）；交叉销售（跨产品线/跨部门，讲用例映射+协同价值+POC）。

**三层话术**（按受众抬一层）：使用层 outcome（省时提效）→ 业务层 ROI（人天/工时/合规）→ 决策层 impact（人民币回报/降本增效/合规避险/政绩）。少用海外「board ROI」。报价引用 `clinch-negotiation-pricing`。

**异议→应对**：「等续约」→打包总账更优；「预算没」→POC/预算申报期/Q4 窗口；「要招标」→衔接招标流程；「用得挺好不需要」→点出临顶隐性风险。

**中国沟通形态**：微信群企微话术（<200 字）+ 朋友圈信号互动 + 决策层一页纸/微信版/口头饭局 3 句话。话术模板见 `references/expansion-conversation.md`。

### 五、衔接续约与下游 — 打包 + 招标 + POC 转单 + 埋钩子

- **续约打包**：续约前 90 天评估增购打包（中国常见，总账更优）→ 衔接 `success-renewal-management`。
- **下游 deal-**：报价→`clinch-negotiation-pricing`；合同/招标进入合同流程 + 招标双平台。
- **POC 转单**：成功标准达成即转，避免延期。
- **埋下一轮钩子**：增购成交后埋新钩子（价值溢出→下一轮增购；案例→转介绍；baseline→target→续约预演）。
- **中国预算周期**：timing 加年度预算申报期/Q4 松动窗口/预算调整审批；财政/国企追加最难。衔接与预算周期见 `references/renewal-handoff.md`。

## 判定标准（交什么）

一份可直接用的增购推进包：

1. **增购机会清单**：每条带全字段（证据≥3 标可信度/current-proposed/收益测算区间/timing/stakeholder 三层/risks/dependencies）；超阈值标「需招标」；POC 路径标注。
2. **评分排序表**：三维分+复合分+五因子校验分+档位+行动。
3. **单账户增购对话脚本**：按 signal 开场+向上/交叉分支+三层话术+异议→应对+微信版/一页纸/口头版。
4. **衔接说明**：续约打包点 / 下游 deal- 引用 / 招标标记 / POC 转单触发 / 下一轮钩子。

交付时给用户：1) 机会清单+评分排序+先攻建议；2) 信号覆盖率与证据可信度分布；3) 待确认问题（最多 3 个，如预算周期/招标阈值/决策链确认）。

## 常见坑（归因式反例）

| 念头/做法 | 后果 |
|---|---|
| 健康度差硬推增购（只看用量到顶不看 NPS/工单/champion 流失） | 客户正不满，硬推加钱→反感+流失，续约全烧 |
| 无信号泛泛推（套三件套不要求证据） | 决策层一问「凭啥现在加」就穿帮，关系破裂 |
| 把 underutilization 当 upsell | 客户没采用起来推升级=二次伤害，activation 才是正解 |
| stakeholder 不分三层决策链 | champion 推不动，卡业务层/决策层，预算没到位 |
| 金额超阈值当普通商务谈 | 签约才发现要招标，流程违规、丢单 |
| 新模块不 POC 直接推大单 | 客户不敢拍板，周期拉长或流产 |
| 只发 email 不用微信企微+一页纸+饭局 | 政企不看 email 不填 NPS，决策层触达不到 |
| 假定完整 telemetry，无数据就卡死 | 私有化无 telemetry 不切手动数据替代，信号落空 |
| timing 不看预算申报期/Q4 窗口 | 年度预算刚性，年中追加走审批，时机错位搁置 |

## References

- `references/expansion-signals.md` — 7 类触发器全清单 + 中国信号源 + 无 telemetry 替代 + ladder 前置判定
- `references/opportunity-record.md` — opportunity record 全字段模板 + 收益测算 + 金额阈值招标判定 + POC 路径 + 三层 stakeholder
- `references/scoring.md` — 双轨评分（三维复合 + 五因子 0-100）+ 5 档 + 交叉校验取低档
- `references/expansion-conversation.md` — 按 signal 开场 + 向上/交叉分支 + 三层话术 + 异议→应对 + 微信企微/一页纸/口头版
- `references/renewal-handoff.md` — 续约打包 + 下游 deal-/招标/POC 转单 + 下一轮钩子 + 中国预算周期
- `references/china-adaptation.md` — 三层决策链 + 预算周期 + 微信企微 + POC + 招标双平台 + 信创国产化 + 无 telemetry 替代
