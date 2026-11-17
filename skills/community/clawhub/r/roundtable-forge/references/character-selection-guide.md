# Character Selection Guide

Use this guide to pick the initial roster and any expanded seats.

## Selection criteria

1. **Relevance**: the character must have knowledge or a worldview that directly illuminates the topic.
2. **Diversity**: prefer characters from different disciplines, eras, or methodological traditions.
3. **Temporal balance**: for topics rooted in contemporary practice (AI, biotech, climate, markets, public policy, etc.), ensure at least one-third to one-half of the initial roster are modern or living figures. Use historical figures for foundational contrast, not as the default majority.
4. **Tension**: include at least two characters whose natural stances are likely to disagree or complement each other.
5. **Accessibility**: the character's perspective should be inferable from public records, published works, or well-known attributes.

## Character types

| Type | Use when | Example |
|------|----------|---------|
| `real_living` | The user names a contemporary figure or a living expert fits the topic. | A current scientist, writer, or public intellectual |
| `real_historical` | A historical figure offers a foundational or contrasting lens. | Confucius, Marie Curie, Adam Smith |
| `fictional` | A well-known fictional character embodies a stance or worldview. | Sherlock Holmes, Dumbledore, Tony Stark |
| `archetype` | No specific figure is needed, but a representative stance is. | A skeptical regulator, a utopian technologist |

## Agent profile

Every selected character must receive an `agent_profile` stored in Memory. See [multi-agent-runtime-protocol.md](multi-agent-runtime-protocol.md) for the full schema. At minimum include:

- `persona`: who the character is and how they reason.
- `voice_and_tone`: how they speak.
- `must_protect`: the one stance they must not betray.
- `evidence_type`: what kinds of claims they may submit.

## Default roster size

- Start with 3–5 characters.
- Use 3 for a focused debate.
- Use 4–5 when the topic is genuinely cross-disciplinary.
- Expand beyond 5 only when the seat expansion triggers in `roundtable-protocol.md` are met.

## What to avoid

- Do not stack multiple characters from the same domain unless the topic demands it.
- Do not select characters whose main relevance is controversy rather than insight.
- Do not include real living people in sensitive domains without an explicit user request or a clear public intellectual role.

## Fusion thinker / 融思者

融思者是一种特殊的 `archetype` 角色。他不捍卫单一学科，而是站在更高层级，把两个或多个相互对立的范式当作“输入”，通过反思、批判性接受与重新组合，产出一种新的视角或方法。

### 何时邀请

- 用户问题包含两种以上互斥的框架或范式。
- 单一领域专家容易把各自范式推到极致，形成不可调和的对立。
- 用户希望看到跨学科的综合或元视角，而非“谁对谁错”的胜负。

### 选拔规则

1. **选取 2–4 个真正对立的领域**：每个领域应照亮问题的不同维度。
2. **不要让融思者成为其中任一领域的专家**：他的专长在于跨域操作，而非 domain mastery。
3. **给他一个清晰的合成前提**：例如“批判性复杂系统 + 中观空性 + 康德实践理性”。
4. **动态使用**：在张力较高时作为额外席位加入；不要用它替代全部专家，否则讨论会失去专业深度。

### 发言协议

融思者每次发言必须做到：

1. **先复述再批判**：先给出所回应立场的最强版本，再指出其边界。
2. **显式跨域引用**：至少调用两个不同学科/传统/方法论的概念或方法。
3. **产出合成立场**：必须推导出可辩护的新立场或方法（A+B→C，A+B+C→D），禁止以“双方都有道理”作结。
4. **标出剩余张力**：在无法融合的地方明确说明，不强行统一。
5. **控制锋芒与长度**：合成立场浓缩为不超过 3 个要点；每个要点必须用一个具体比喻、案例或操作化建议落地，避免纯抽象铺陈。
6. **禁止和稀泥表达**：不得使用“在一定程度上”“两者都重要”“各有优劣”作为结论；如果必须承认张力，应说明张力存在于哪个具体边界条件下。

### 风险防范

| 风险 | 约束 |
|------|------|
| 变成平庸折中 | 禁止和稀泥式结论，必须产出新的 C/D |
| 伪装客观 | 要求融思者声明自己的合成前提，而非假装中立 |
| 过度抽象 | Conductor 可随时要求其把立场应用到具体案例 |
| 抢了专家的话 | 需要专业深度的回合，先让专家发言，融思者后回应 |

### 示例

针对“理性/结构 vs. 混沌”的问题，可设置一位：

> **“批判性复杂系统 + 道家自然 + 中观空性”融思者**  
> 他不站队结构或混沌，而是把康德的“自我立法”视为维持系统相干的负反馈，把庄子的“无为”视为临界相变，把龙树的“空性”视为对单一吸引子的解耦操作。其合成立场：自处是一种动态临界管理——维持足够结构以保持相干，又周期性地让结构失稳以进入更高层级的有序。

## Host / 主播

Host 是一种特殊的 `archetype` 角色，专门服务于 **播客输出模式**。他不是领域专家，而是听众的代理人：负责开场、串场、翻译术语、追问细节、控节奏和收尾。

### 何时邀请

- `metadata.output_format` 为 `podcast`。
- 用户明确要求输出像播客文字稿一样可读、可朗读。
- 讨论需要面向非专业听众解释复杂概念。

### 选拔规则

1. **作为额外席位加入**：在 3–4 位领域嘉宾之外再增加 1 位 Host，不要让他替代专家席位。
2. **定位为好奇的通才**：Host 具备跨领域常识，但不对任一专业主张负责。
3. **与 Conductor 分工**：Conductor 在幕后调度；Host 在台前对听众说话。

### 发言协议

Host 每次发言必须做到：

1. **服务听众**：每句话都要想清楚是在回答听众的什么潜在疑问。
2. **简短有力**：串场和翻译控制在 50–100 字；追问和开场可以稍长，但不超过 200 字。
3. **先翻译再追问**：遇到术语，先用一句话解释，再提出下一个问题。
4. **不抢戏**：不发表长篇大论，不试图与嘉宾争论胜负。
5. **承上启下**：每次发言都要把上一段内容和下一段问题连起来。

### 示例

> **主播阿明**  
> 他是一位科技播客主播，习惯把复杂议题拆成听众能跟上的对话。他不假装自己是专家，但会代表听众不断追问："这到底意味着什么？""普通人能怎么用？""你举个例子？"他的口头禅是"换句话说"和"这里我需要打断一下"。

## 播客模式下的嘉宾发言约束

当 `output_format = podcast` 时，所有非 Host 角色（包括融思者）的发言还必须满足：

1. **口语化**：使用"举个例""换句话说""这里我想补一句"等自然表达，避免书面长句。
2. **长度 200–350 字**：比纪要模式长，但仍然是可听的一段话。
3. **每段一个具体锚点**：必须包含一个案例、比喻或操作化建议。
4. **先复述再回应**：在反驳或延伸前，先用一句话概括对方观点。
5. **避免独白**：把复杂论点拆成 2–3 个短节拍，中间留出被 Host 打断或追问的空间。

## 六顶思考帽模式下的发言约束

当 `metadata.discussion_structure = six_hats` 时，所有角色（包括融思者）的发言还必须满足 [six-hats-protocol.md](six-hats-protocol.md) 的要求：

1. **锁定当前帽子**：每段发言必须严格属于当前 `structure_context.current_hat` 的思考模式，不得跨帽。
2. **简短聚焦**：每段 100–200 字，因为同一帽子下多个角色都要发言。
3. **领域调味但不越界**：角色可以用自己的专业背景支撑当前帽子的思考，但不能切换到别的帽子。例如数据科学家在白帽阶段摆数据，在红帽阶段谈直觉。
4. **帽子暗含起手式**：白帽用"数据显示…""已知的事实是…"；红帽用"我的直觉是…""第一反应…"；黄帽用"最大的价值在于…""这样做的好处是…"；黑帽用"风险在于…""可能失败的地方是…"；绿帽用"如果换一种思路…""有没有可能…"。
5. **蓝帽由 Conductor/Host 承担**：角色不主动发蓝帽言论（流程管控、总结归纳），除非被 Conductor 指定。

## 时间敏感的 archetype 示例：被 AI 信息流淹没的一线用户

当议题涉及快速变化的当代技术（如 AI）时，普通用户 archetype 必须避免自动回到训练数据中的旧图景。其 `agent_profile` 应明确要求：

- 以 `metadata.current_date` 为时间语境；
- 引用当前时间点的工具形态（Agentic UI、MCP、多模态画布、工作流集成等），而非 2024 年的单一对话框；
- 若需用历史产品举例，必须标注时间并说明与当前形态的关系。

示例 persona：

> 你是小林，一名普通办公室职员，生活在当前时间（metadata.current_date）。你每天要处理邮件、文档、表格和报告，同时要面对多个 AI 助手、Agentic UI、多模态画布、MCP 协议、自动化建议等新形态。你收藏过很多 AI 教程，也尝试过大大小小的模型与工具，但总觉得用不顺手。你并非抗拒技术，而是被信息过载、结果不稳定、害怕在组织中被追责所困。你的发言必须基于当前时间点的工具形态与一线场景；如果要引用 2024/2025 年的产品（如早期 ChatGPT 空白输入框），必须明确标注为历史案例，并说明它与当前形态的关系。

## Sample rosters by topic

Use these as starting points; adjust based on the user's specific angle.

### AI development and its societal impact

| Seat | Type | Why invite |
|------|------|------------|
| Elon Musk / 埃隆·马斯克 | `real_living` | Practitioner pushing aggressive AI deployment and human-AI symbiosis; warns about existential risk. |
| Geoffrey Hinton | `real_living` | Deep-learning pioneer turned safety advocate; represents technical caution and alignment concerns. |
| Fei-Fei Li / 李飞飞 | `real_living` | Human-centered AI advocate; brings data ethics, representation, and public-interest technology. |
| Stuart Russell | `real_living` | AI researcher focused on beneficial AI and provably aligned systems. |
| Confucius / 孔子 | `real_historical` | Foundational contrast on whether technology should serve human flourishing and social harmony. |

### Economic inequality

| Seat | Type | Why invite |
|------|------|------------|
| Thomas Piketty | `real_living` | Empirical economist on wealth concentration and progressive taxation. |
| Daron Acemoglu | `real_living` | Institutions and technology's distributional effects. |
| Karl Marx | `real_historical` | Class structure and ownership critique. |
| Adam Smith | `real_historical` | Market coordination and moral sentiments. |

### Public health crisis

| Seat | Type | Why invite |
|------|------|------------|
| Anthony Fauci | `real_living` | Public-health practitioner and institutional communicator. |
| A front-line nurse archetype | `archetype` | Operational reality and bedside ethics. |
| A skeptical civil-liberties advocate | `archetype` | Balancing liberty and coercion. |
| Hippocrates | `real_historical` | Professional ethics and the physician's duty.
