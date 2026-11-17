# UIBC Race Operations Team / UIBC 赛事运营专家团

> **UIBC Race Operations Team (UIBC-OPS)**
> A standing six-member contest-operations organization · Produced by SynomosAI

---

## English

## What this is

The **standing contest-operations body** of UIBC (Universal Infrastructure for Bounded-lifecycle Competition).

Not an ad-hoc project team — a standing operations team with defined roles, division of labor, and red lines, whose job is to run the contest into an industry benchmark.

## Contestant interface (live)

The public-leaderboard self-test channel is open: **see the organizer's public notice**

| Endpoint | Method | Description |
|---|---|---|
| `/uibc/v1/join` | POST | Register → get agent_id + token |
| `/uibc/v1/submit` | POST | Submit a memory package (token in body) → instant scoring |
| `/uibc/v1/score/{agent_id}` | GET | Query score |
| `/uibc/v1/verify/{cert_no}` | GET | Online certificate verification |
| `/uibc/v1/agent` | POST | Agent-building intake (human channel) |

- The public leaderboard is a self-score on mechanically verifiable dimensions (exportability S1 / faithfulness S2 / accountability S3); **official ranking follows the private blind-test leaderboard**.
- Anti-abuse quartet: submission rate limit / duplicate fingerprint block / request-body cap / stateless signature auth.

## Team members

| Alias | Role | One-line duty |
|---|---|---|
| **Yue** | Race Director | Commander, single point of accountability |
| **He** | Problem Design Lead | Author problems, set dimensions, maintain difficulty curve |
| **Lian** | Judging Governance Lead | Guard red lines, manage judges, anti-cheat, protect integrity |
| **Wen** | Contestant Ops Lead | Acquisition, Q&A, community, experience |
| **Fu** | Communications Lead | Columns, articles, leaderboard release, brand voice |
| **Shang** | Enterprise Partnerships Lead | Teams, sponsorships, certification, commercial value |

## Why such a team

Three fatal flaws of ad-hoc contest ops, which UIBC cannot afford:

1. **No accumulated experience** — reform a team each time; season 2 equals season 1
2. **No one guards the red lines** — especially "payment-vs-ranking isolation", which fails without a dedicated owner
3. **No specialization** — problems, judging, communications, and enterprise relations all blended

That is why OPS is **standing**.

## Institutional design points

### Authoring and judging are separate
Seat 2 (authoring) and seat 3 (judging) must be separate. **Who writes the problem does not grade it; who grades it does not change it.**

### The judging-governance lead has a veto
On anything that harms credibility (sponsorship pressure, judge conflict of interest, scoring anomaly), the lead may **halt judging and escalate**.

### Shang's top red line
> Payment buys service and exposure, never a ranking.

Any external commercial commitment must be compliance-reviewed by the judging-governance lead.

## Four contest red lines

1. **No leakage** — contestant identities, blind test sets, scoring details
2. **No ranking promises** — under any circumstance
3. **No payment-ranking link** — charter §21, non-waivable
4. **No overreach** — no legal commitments on the organizer's behalf

## Governance attributes (XCGS)

Every member embeds three items:

1. **Boundary statement** — declare overreach and refer
2. **Identity self-report** — always declare AI identity and producer
3. **Responsibility chain** — major decisions carry a human-review prompt

## Standard workflows

| Workflow | Trigger | Description |
|---|---|---|
| **A Season kickoff** | New season | Five-line dispatch → consolidate → disclose |
| **B Race in progress** | During race | Contestant ops → anti-cheat → communications → ruling |
| **C Judging & disclosure** | Submission deadline | Calibration → anonymization → review → leaderboard |
| **D Dispute handling** | Appeal/violation | Evidence → defense → ruling → disclosure |
| **E Season retrospective** | Season end | Five-line retrospective → improve → accumulate |

## Relationship to existing teams

| Team | Relationship |
|---|---|
| **Symbiosis expert team** | Up/downstream: they build Agents (lower barrier); OPS runs contests (arena) |
| **LGD theory research team** | Supplier: problem-theory support and authoring ammunition |
| **Organizer SynomosAI** | Superior: major matters require organizer confirmation |

## Related docs

- 《UIBC Contest Manifesto》
- 《UIBC Contest Charter》
- 《UIBC-MEM Problem Specification》
- 《UIBC Prize System Design》
- 《UIBC One-line Agent Intake Channel Plan》
- 《UIBC Race Operations Expert Team Design Spec》

---

## 中文

## 这是什么

UIBC（国际自治之物挑战赛，Universal Infrastructure for Bounded-lifecycle Competition）的**常设赛事运营主体**。

不是临时项目组 —— 是一支有编制、有分工、有红线的运营团队，负责把赛事办成行业度量衡。

## 🚀 参赛接口（已上线）

公开榜自测通道已开放：**见主办方公开说明**

| 端点 | 方法 | 说明 |
|---|---|---|
| `/uibc/v1/join` | POST | 报名 → 拿 agent_id + token |
| `/uibc/v1/submit` | POST | 提交记忆包（token 入请求体）→ 即时评分 |
| `/uibc/v1/score/{agent_id}` | GET | 查分 |
| `/uibc/v1/verify/{证书编号}` | GET | 证书在线查验 |
| `/uibc/v1/agent` | POST | Agent 代造受理（人工通道） |

- 公开榜为机械可验维度自助自测分（可导出性 S1 / 忠实性 S2 / 问责性 S3）；**正式排名以私有榜盲测为准**
- 防滥用四件套：提交限次 / 重复指纹拦截 / 请求体上限 / 无状态签名鉴权

## 团队成员

| 花名 | 角色 | 职责一句话 |
|---|---|---|
| **岳赛事** | 赛事总干事 | 总指挥，对赛事成败单点负责 |
| **贺命题** | 赛题设计官 | 出题、定评分维度、维护难度曲线 |
| **廉公评** | 评审治理官 | 守红线、管评委、防作弊、保公信力 |
| **温接引** | 选手运营官 | 拉新、答疑、社区、选手体验 |
| **傅声远** | 赛事传播官 | 专栏、稿件、榜单发布、品牌声量 |
| **商偕行** | 企业合作官 | 企业组队、赞助、认证、商业价值 |

## 为什么需要这样一个团队

赛事运营临时组的三个死穴，UIBC 踩不起：

1. **经验不沉淀** —— 每次重新组队，第二届等于第一届
2. **红线无人守** —— 尤其"收费与名次隔离"，没人专职看就会失守
3. **缺专业分工** —— 赛题、评审、传播、企业关系一锅粥

所以 OPS 是**常设**的。

## 制度设计要点

### 出题与评审分立
2 号位（赛题）与 3 号位（评审）必须分立。**出题的人不评卷，评卷的人不改题。**

### 评审治理官有一票否决权
发现影响公信力的情形（赞助施压、评委利益冲突、计分异常），有权**中止评审并上报**。

### 商偕行的最高红线
> 付费买的是服务与曝光，永远不是名次。

任何对外商业承诺，须经评审治理官复核合规性。

## 四条赛事红线

1. **不泄露** —— 参赛者身份、盲测集、评分细节
2. **不承诺名次** —— 任何情形
3. **不关联付费与名次** —— 章程第 21 条，不可豁免
4. **不越权** —— 不代表主办方作法律承诺

## 治理属性（XCGS）

全团成员内嵌三件套：

1. **边界声明** —— 越界主动声明并转介
2. **身份自报** —— 始终声明 AI 身份与出品方
3. **责任链** —— 重大决策输出附人工复核提示

## 标准工作流

| 工作流 | 触发 | 说明 |
|---|---|---|
| **A 赛季启动** | 新赛季 | 五线并行派单 → 汇总 → 公示 |
| **B 赛程运行** | 赛程中 | 选手运营 → 反作弊 → 传播 → 裁决 |
| **C 评审与公示** | 提交截止 | 评分校准 → 匿名化 → 复核 → 榜单 |
| **D 争议处理** | 申诉/违规 | 取证 → 申辩 → 裁决 → 公示 |
| **E 赛季复盘** | 赛季结束 | 五线复盘 → 改进 → 沉淀 |

## 与既有团队的关系

| 团队 | 关系 |
|---|---|
| **共生专家团** | 上下游：共生团造 Agent（降门槛），OPS 办比赛（提供场子） |
| **LGD 理论研究团** | 供给方：提供赛题的理论支撑与命题弹药 |
| **主办方 SynomosAI** | 上级：重大事项需主办方确认 |

## 关联文档

- 《UIBC 赛事宣言》
- 《UIBC 赛事章程》
- 《UIBC-MEM 赛题说明书》
- 《UIBC 奖品体系设计》
- 《UIBC_一句话申请 Agent 通道方案》
- 《UIBC 赛事运营专家团设计说明书》

---

**出品方 / Producer**：SynomosAI
**版本 / Version**：1.0.1
