# Internal Prep Brief & Leakage Check（internal-prep-and-leakage-check）

> 配套 SKILL.md 主线第六步。采用 internal prep appendix + leakage check + CSM 内部 prep brief 双件分离。

## 一、双件分离原则

| 件 | 受众 | 内容 | 分发 |
|---|---|---|---|
| 客户面 deck/材料 | 客户决策层+champion | 价值叙事+红黄绿（目标达成度表述）+joint plan | 会前 T-7 预发+会中用 |
| 内部 prep brief | CSM+销售独享 | 风险信号+扩张 framing+竞争情报+雷区+谈判姿态 | CSM 内部，不入客户件 |

**铁律**：两件物理分离，内部 prep brief 的任何内容不得出现在客户面材料。最后做 leakage check 防泄露。

## 二、内部 Prep Brief 结构

### 1. Full Account Brief
- 客户背景+合同信息+续约节点+ARR/合同额。
- 上轮 QBR 承诺+兑现状态+缺口。
- success plan baseline→target 进度。

### 2. 活跃风险信号（带证据，不入客户件）
- 未兑现承诺（含我方原因）。
- 客户不满信号（工单/投诉/微信抱怨截图）。
- 决策层变动（一把手/分管副总换人）。
- 竞品渗透信号。
- 每条标：信号+证据+影响+建议应对。

### 3. 扩张 Framing（会后单独推进用）
- 增购机会（客户主动问的新场景+使用量超预期+兄弟部门）。
- 增购触发测算（见 `references/downstream-hooks.md`）。
- at_risk 时标注「跳过 expansion，救计划优先」。

### 4. 竞争情报
- 竞品动态+客户对竞品态度+我方差异化点。
- 客户面不提竞品（除非客户主动问），内部 prep brief 记录供 CSM 把握方向。

### 5. Stakeholder Dynamics（谁在会议室）
| 与会人 | 角色 | 上次互动 | 已知立场 | 应对 |
|---|---|---|---|---|
| 张副总 | 分管副总 | 上月微信认可 | 支持但关心 ROI | 给 Strategic 层+headline metric |
| 李主任 | 部门负责人 | 上季 QBR | 关心处室覆盖 | 给 Tactical 层+补救计划 |
| 王副主任 | champion/信息中心 | 经常互动 | 强力推动者 | 给详细版做内推 |

### 6. Talking Points
- 开场：对齐议程+确认目标。
- 价值回顾：headline metric+3 证据+客户原话。
- 战略讨论：合规适配进展+下期规划。
- 行动计划：≤3 commitments 提客户方 owner。
- 收尾：感谢+下步。

### 7. Landmines（雷区，必避）
- 未决 support 工单（会前确认状态，客户问起如何答）。
- 已知不满（某次培训缺席/某功能 bug）。
- 政治敏感（部门间矛盾/决策层换届）。
- 上轮未兑现承诺（如何诚实表述不甩锅）。
- 禁谈话题（竞品/价格/合同条款，除非客户主动问）。

## 三、Leakage Check 清单（发客户件前必做）

发客户面材料（deck/一页纸/微信版/post-QBR summary）前，逐项查：

| # | 查项 | 查法 | 查到 |
|---|---|---|---|
| 1 | unsupported attribution | 无证据的归因（「客户说很好」无截图） | 删或补证据 |
| 2 | confidential commentary | 内部评论（「客户领导不懂技术」） | 删 |
| 3 | internal-only data | 内部数据（成本/利润率/内部成本推算） | 删 |
| 4 | accidental overstatement | 夸大（partial 写 delivered / estimated 写 confirmed） | 改回真实状态 |
| 5 | 内部风险语言 | 风险信号/扩张 framing/竞争情报/landmines 的语言 | 删 |
| 6 | 我方原因内部表述 | 「我方培训资源排期问题」→ 改为客观「处室覆盖 3/5，下季补齐 5」 | 改为客观表述 |
| 7 | health score 字眼 | 「health score」/「打分」→ 改为「目标达成度」 | 改表述 |

**人工 approval gate**：CSM review + leakage check 通过后才发客户件。不自动 publish/email。post-QBR summary 同样走 leakage check。

## 四、Post-QBR Summary（会后 follow-up）

会后 T+1~T+3 发客户 follow-up：
- **客户面版**：post-QBR summary（承诺兑现+success definition 状态+下期 plan+action items），走 leakage check，CSM review 后发。
- **微信版**：<200 字摘要发客户群。
- **正式邮件版**：客户面版+附件，发客户决策层+champion。
- **内部版**：内部 prep brief 更新（会中新信号+action tracker+触发点），CSM+销售内部存档，交接下游 skill。

## 五、反例（归因式）

| 念头/做法 | 后果 |
|---|---|
| 内部风险语言泄露进客户件 | 政企敏感，leakage 一次信任崩，后续复盘邀不到决策层 |
| 无 leakage check 直接发 | 内部评论/风险信号/我方原因表述泄露，客户翻车 |
| 自动 publish/email 不走 approval gate | 未经 CSM review 的材料出错，客户面尴尬 |
| 内部 prep brief 与客户件混在一个文件 | 物理不分离，leakage 风险倍增 |
| 我方原因写成内部语言给客户看 | 「我方培训资源排期问题」→ 客户觉得甩锅或窥见我方内部问题 |
| health score 字眼给客户 | 客户不接受被「打分」，觉得被评判 |
