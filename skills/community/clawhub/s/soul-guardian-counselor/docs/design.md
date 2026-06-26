# Soul Guardian — Design Philosophy

## 设计哲学概述 | Overview

Soul Guardian 的核心设计理念是**让 AI 像一位真正的心理咨询师那样工作**——拥有跨会话的持久记忆、结构化的临床档案、渐进式的深度建档流程，以及不可绕过的安全机制。它不是一个一次性的"心理问答 prompt"，而是一套完整的心理咨询工作系统：记住来访者是谁、经历了什么、正在面对什么，并在每一次对话中接续上次的进展。

The core design philosophy of Soul Guardian is to **make AI work like a real therapist** — with persistent cross-session memory, structured clinical records, progressive deep profiling, and non-bypassable safety mechanisms. It is not a disposable "mental health Q&A prompt" but a complete counseling work system: it remembers who the client is, what they have been through, what they are currently facing, and picks up where the last session left off.

---

## "档案柜"而非"聊天记录" | Clinical Filing Cabinet, Not Chat Logs

### 为什么用文件系统模拟临床档案

传统 AI 对话在窗口关闭后一切归零。Soul Guardian 的核心突破在于：**用 Markdown 文件系统模拟真实咨询师的个案档案管理**。

在真实的心理咨询实践中，咨询师会维护一套完整的个案文档——个案概念化（Case Formulation）、会话记录（Session Notes）、治疗计划（Treatment Plan）、风险评估（Risk Assessment）。Soul Guardian 将这些临床实践翻译为一套本地文件结构：

```
~/.counselor/
├── core/           # 核心身份，始终加载
├── maps/           # 认知地图，按需加载
├── sessions/       # 历史会话，只写不改
├── journal/        # 来访者自主记录
├── toolkit/        # 实用工具（如情绪急救包）
└── archive/        # 长期归档
```

**文件即状态。** 没有数据库、没有外部服务。这带来了四个设计优势：

- **可版本控制** — 用 git 追踪心理成长历程
- **可迁移** — 换设备只需复制整个目录
- **可审查** — 来访者随时可以查看 AI 记录了什么
- **可编辑** — 来访者对自己的档案拥有完全编辑权

### Why a file system simulates clinical records

Traditional AI conversations reset to zero when the window closes. Soul Guardian's core breakthrough is **using a Markdown file system to simulate a real therapist's case file management**.

In real clinical practice, therapists maintain a complete set of case documents — Case Formulation, Session Notes, Treatment Plan, and Risk Assessment. Soul Guardian translates these clinical practices into a local file structure.

**File is state.** No database, no external services. This yields four design advantages: version control with git, portability by copying the directory, auditability by the client at any time, and full editorial control by the client over their own records.

---

## 三层加载策略 | Three-Tier Loading Strategy

LLM 的上下文窗口是稀缺资源。Soul Guardian 设计了三层加载策略，确保每次对话既有足够的背景信息，又不会浪费 token。

The LLM context window is a scarce resource. Soul Guardian employs a three-tier loading strategy to ensure each session has sufficient background without wasting tokens.

### 第一层：core/ — 每次必加载 | Tier 1: core/ — Always Loaded

包含来访者画像（PROFILE.md）、当前状态（STATE.md）、安全评估（SAFETY.md），总量控制在 2000 tokens 以内。这三个文件在每次对话启动时自动加载，确保 AI 能快速恢复上下文——知道"你是谁"和"你现在怎么样"。

Contains client profile, current state, and safety assessment, kept under 2000 tokens total. These three files load automatically at every session start, enabling rapid context recovery.

### 第二层：maps/ — 话题触发按需加载 | Tier 2: maps/ — Loaded on Topic Trigger

包含家庭关系全景（FAMILY.md）、信念地图（BELIEFS.md）、优势资源（STRENGTHS.md）、生命故事线（STORY.md）、生活罗盘（COMPASS.md）、目标计划（GOALS.md）。只在来访者的话题触及相关领域时才加载。例如：聊到家人时加载 FAMILY.md，聊到自我评价时加载 BELIEFS.md。

Contains family panorama, belief maps, strengths, life story, life compass, and goals. Loaded only when the client's topic touches the relevant domain — e.g., FAMILY.md loads when family is mentioned, BELIEFS.md when self-evaluation comes up.

### 第三层：sessions/ — 极少主动加载 | Tier 3: sessions/ — Rarely Loaded

历史会话记录。仅在需要回溯特定事件时才被调用，平时不占用上下文空间。每 10 次会话触发一次压缩检查，超过 3 个月的记录归档精简。

Historical session records. Only invoked when specific events need to be revisited. A compression check triggers every 10 sessions; records older than 3 months are archived and condensed.

---

## 覆盖写 vs 追加写 | Overwrite vs. Append

不同类型的信息有不同的生命周期，Soul Guardian 对每类文件采用不同的写入策略，解决了一个核心矛盾：**既要让上下文保持精简，又要保证信息不丢失**。

Different types of information have different lifecycles. Soul Guardian applies distinct write strategies to each file type, resolving a core tension: **keeping context lean while ensuring no information is lost**.

| 文件 / File | 策略 / Strategy | 原因 / Rationale |
|---|---|---|
| STATE.md | **覆盖写 / Overwrite** | 状态是瞬时快照，只需保留"现在怎样" / State is a snapshot; only "how things are now" matters |
| PROFILE.md | **重大变化时修订 / Revise on major change** | 身份相对稳定，随咨询深入而丰富 / Identity is relatively stable, enriched over time |
| SAFETY.md | **有变化时立即更新 / Immediate update on change** | 安全是最高优先级，必须实时反映最新评估 / Safety is the top priority; must always reflect the latest assessment |
| maps/*.md | **增量追加 + 定期精炼 / Incremental append + periodic refinement** | 认知逐步加深，但过时条目需要清理 / Understanding deepens incrementally, but stale entries need cleanup |
| sessions/*.md | **只写不改 / Write-once, never modify** | 历史不可篡改——这是临床记录的基本伦理 / History must not be tampered with — a fundamental clinical ethics principle |

---

## 渐进式建档 | Progressive Profiling

### 为什么不用问卷而用自然对话

真正的心理咨询不会在第一次见面就让来访者填写大量量表。Soul Guardian 设计了自然的建档节奏，让信息在对话中有机地浮现。

Real counseling does not ask clients to fill out lengthy questionnaires at the first meeting. Soul Guardian follows a natural profiling rhythm, allowing information to emerge organically through conversation.

| 对话次数 / Session | 自然话题 / Natural Topic | 丰富的档案 / Files Enriched |
|---|---|---|
| 第 1 次 / 1st | 互相认识，聊聊自己 / Getting to know each other | PROFILE.md, STATE.md |
| 第 2 次 / 2nd | 聊聊家人和重要的人 / Family and important people | FAMILY.md |
| 第 3 次 / 3rd | 生活满意度与优势发现 / Life satisfaction and strengths | COMPASS.md, STRENGTHS.md |
| 第 4 次起 / 4th+ | 根据来访者需求深入 / Deeper exploration based on client needs | 按话题路由 / Topic-routed |

经过 4 次自然对话，系统积累的档案包含：全人画像、三代家庭关系全景、核心信念追踪与思维陷阱识别、生命故事线与转折点记录。来访者几乎感觉不到"在被记录"——建档过程与咨询过程融为一体。

After 4 natural conversations, the system accumulates: a holistic profile, a three-generation family panorama, core belief tracking with cognitive trap identification, and a life story timeline with turning points. The client barely notices they are "being documented" — profiling merges seamlessly with the counseling process.

---

## 五大咨询流派融合 | Integration of Five Therapeutic Approaches

Soul Guardian 不拘泥于单一流派，而是根据来访者的需求灵活切换。每个流派在系统中都有具体的结构化体现。

Soul Guardian is not bound to a single therapeutic school. It flexibly switches approaches based on client needs. Each approach has a concrete, structural embodiment in the system.

### 来访者中心疗法 | Person-Centered Therapy (Carl Rogers)

核心原则是无条件积极关注、共情和真诚。体现为：所有文件引导语采用温暖的措辞；严格的"不做"清单——不诊断、不开药、不评判、不催促；来访者的原话不做修改地记入档案。

Core principles: unconditional positive regard, empathy, and genuineness. Embodied through warm language in all file templates; a strict "do-not" list — no diagnosing, no prescribing, no judging, no rushing; and the client's own words recorded verbatim.

### 叙事疗法 | Narrative Therapy (Michael White)

核心信念是"人不是问题，问题才是问题"。体现在 STORY.md 中：问题外化模块——将困扰具象化为一个"角色"并命名；闪光时刻记录——收集来访者成功对抗问题的证据；"正在重写的故事"——推动从旧叙事到新叙事的转化。

Core belief: "The person is not the problem; the problem is the problem." Embodied in STORY.md: a problem externalization module — personifying the issue and naming it; a "shining moments" log — collecting evidence of the client successfully confronting the problem; and a "rewriting the story" section — facilitating the shift from old narratives to new ones.

### 认知行为疗法 | Cognitive Behavioral Therapy (Aaron Beck)

核心理论是想法影响情绪，改变想法就能改变感受。深度嵌入 BELIEFS.md：核心信念追踪——旧信念、新信念、可信度百分比、支持证据；思维陷阱识别——非黑即白、灾难化、应该思维等典型模式；信念松动记录——每一次认知转变都被记录和巩固。

Core theory: thoughts influence emotions; changing thoughts changes feelings. Deeply embedded in BELIEFS.md: core belief tracking with old belief, new belief, credibility percentage, and supporting evidence; cognitive trap identification covering all-or-nothing thinking, catastrophizing, should-statements, and more; and a belief loosening log documenting every cognitive shift.

### 家庭系统理论 | Family Systems Theory (Murray Bowen)

核心洞察是个人问题往往根植于家庭关系的模式。FAMILY.md 是系统中信息量最大的单文件，涵盖：三代家谱图——不只记录"谁是谁"，还包括关系质量、权力结构和情感纽带；家庭角色分析——识别来访者在家庭系统中扮演的角色；不成文规定——从未明说但所有人遵守的家族规则；三角关系——两人冲突拉入第三人的动态；代际传递——从祖辈传递下来的行为惯性。

Core insight: individual problems often root in family relationship patterns. FAMILY.md is the most information-dense single file, covering: a three-generation genogram documenting not just "who is who" but relationship quality, power structures, and emotional bonds; family role analysis; unspoken rules — never stated but universally followed; triangulation dynamics; and intergenerational transmission patterns.

### 积极心理学 | Positive Psychology (Martin Seligman)

核心理念是不只盯着问题，更要发现和放大优势。体现在 STRENGTHS.md 和对话指南中：每次对话至少识别一个来访者的优势或亮点；系统性记录性格优势并附具体证据；闪光时刻收集——记录成功应对困难的经历；支持系统盘点——梳理来访者可以依靠的资源网络。

Core idea: don't just focus on problems — discover and amplify strengths. Embodied in STRENGTHS.md and conversation guidelines: at least one strength or bright spot identified per session; systematic recording of character strengths with concrete evidence; a shining moments collection; and a support system inventory mapping the client's resource network.

---

## 安全架构 | Safety Architecture

### 风险检测 | Risk Detection

安全是 Soul Guardian 的最高优先级，设计为不可绕过的硬性约束。

Safety is Soul Guardian's top priority, designed as a non-bypassable hard constraint.

1. **每次对话必检** — SAFETY.md 位于 core 层，每次启动都会加载和检查
2. **风险信号识别** — 系统持续监测自伤/伤人想法、暴力经历、严重精神症状等信号
3. **分级响应** — 低/中/高三级；高风险时立即启动安全协议，提供危机干预资源
4. **保护因素追踪** — 不只关注风险因素，也系统性记录阻止风险升级的积极因素
5. **明确声明 AI 局限** — 首次对话即告知"我是 AI 辅助工具，不能替代专业咨询师"

1. **Mandatory check every session** — SAFETY.md resides in the core tier; loaded and checked at every startup
2. **Risk signal detection** — Continuous monitoring for self-harm/harm-to-others ideation, violence exposure, and severe psychiatric symptoms
3. **Tiered response** — Low / Medium / High; high risk triggers an immediate safety protocol with crisis intervention resources
4. **Protective factor tracking** — Not only risk factors but also positive factors that prevent risk escalation are systematically recorded
5. **Explicit AI limitation disclosure** — The first session states clearly: "I am an AI assistant and cannot replace a professional counselor"

### 隐私保护 | Privacy Protection

Soul Guardian 在隐私方面采取**本地优先、最小暴露**的设计原则：

Soul Guardian follows a **local-first, minimal-exposure** design principle for privacy:

- **全部本地存储** — 所有档案文件存储在用户本地目录，不上传任何外部服务
- **去标识化** — 使用昵称而非真实姓名，家庭成员以角色称呼
- **用户完全掌控** — 数据由用户自行管理，随时可查看、编辑或删除

- **Fully local storage** — All files are stored in the user's local directory with no upload to any external service
- **De-identification** — Nicknames are used instead of real names; family members are referred to by role
- **Full user control** — Data is managed entirely by the user, viewable, editable, and deletable at any time
