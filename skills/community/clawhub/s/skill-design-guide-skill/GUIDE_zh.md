# Skill 设计与实践指南

> 全生命周期参考：设计 → 编写 → 审计 → 发布 → 安全对抗 → 维护。
> 取代 SKILL_zh.md v1.4.3 作为权威版本。基于 Anthropic / OpenAI / LangChain 设计原则与 23 个 skill 的双平台治理实践。

---

## 第一部分：认知框架

### 1. Skill 的本质

**Skill 是写给 agent runtime 的执行契约，不是写给人的说明书。**

平台的评测体系、安装命令形态、SKILL.md 的字段设计（`read_when` / `not_for`）都指向同一事实：skill 的主要消费者是 agent——由 agent 按任务需要检索、路由、加载、执行。人类用户偶尔搜索浏览，但不是主路径。

由此推导的优先级：

| 投入项 | 价值 | 原因 |
|---|---|---|
| Hard Rules / Failure Handling / Output Format | **最高** | agent 加载后照着执行——这些段就是运行时行为约束 |
| not_for / read_when | 高 | agent 的路由与排除逻辑；误触发（加载错误 skill + 执行错任务）代价高于漏触发 |
| description 的精确性 | 高 | agent 路由决策的依据；embedding 检索匹配语义 |
| README / 排版美化 | 低 | agent 不读 |

### 2. 三条设计公理

**公理一：简单优先。** 从单个 SKILL.md 开始，复杂度只在简单方案被证明不够时才增加。绝大多数"能跑但架构乱"的 skill 都是违反了这条。

**公理二：职责分离。** LLM 决定做什么（SKILL.md），确定性代码负责执行（scripts/），知识沉淀为可加载资产（references/）。判断力和执行力不混在一个文件里。

**公理三：按需加载。** references 只在使用时加载。一次性把全部参考塞进上下文，既浪费 token 又稀释指令密度。

---

## 第二部分：设计

### 3. Workflow 还是 Agent

一个问题定生死：**任务步骤是否预先确定？**

- 步骤清晰可预测 → **Workflow**（更快、更便宜、可调试）
- 步骤不确定、需要动态规划 → **Agent**（灵活但成本高）

大多数场景是 Workflow。不因为 Agent 听起来高级而选它。

### 4. 五大工作流模式

| 模式 | 最适合 | 陷阱 |
|---|---|---|
| 提示链（Prompt Chaining） | 顺序步骤 + 检查点 | 链过长时中间态丢失 |
| 路由（Routing） | 输入类型明确 → 不同路径 | 路由条件模糊导致错路 |
| 并行化（Parallelization） | 子任务互相独立 | 误把有依赖的子任务并行 |
| 协调者-执行者（Orchestrator-Workers） | 子任务不可预测 | 过度使用——多数场景不需要 |
| 评估器-优化器（Evaluator-Optimizer） | 生成→评估→迭代直到达标 | 无明确达标标准的空转 |

### 5. 结构规范

三层结构与文件职责：

| 层 | 角色 | 位置 |
|---|---|---|
| Brain | 决策逻辑、工作流定义 | `SKILL.md` |
| Hands | 确定性执行 | `scripts/` |
| Session | 知识库、配置、模板 | `references/`、`assets/`、`templates/` |

必需组件：SKILL.md 一个。可选组件按需增加——但四要素（见第 7 节）在 SKILL.md 内不可缺。

---

## 第三部分：编写

### 6. frontmatter 规范

最小攻击面原则：**每个字段都是扫描器的分析面，也是 agent 的路由依据。两者方向一致——写精确，不写多。**

| 字段 | 规范 |
|---|---|
| `name` / `slug` / `displayName` | slug 全小写连字符；发布前查重（见第 12 节） |
| `description` | 一段精确能力陈述：做什么、不做什么、输入输出。embedding 检索匹配语义，**不堆关键词** |
| 中文摘要 | 双语扩大两种语言的语义命中面。写能力概述 + 触发词，位置在 description 内嵌（SkillHub 只索引 description）或 description_zh（ClawHub） |
| `not_for` | **与 read_when 同等重要。** 每条回答"agent 什么情况下会错误地路由到这里"——写相邻任务域的排除 |
| `read_when` | 触发条件写短语；不追求数量 |
| `version` | 语义化版本（见第 17 节） |

**不要加的字段**：防御性免责声明堆砌、NOT disclaimer 列表、过度收窄的触发前置条件——这些会制造 description 与正文的新矛盾面。

### 7. 正文四要素

| 要素 | 作用 | 写法 |
|---|---|---|
| **步骤标签** | 声明每步是 `[Deterministic]` 还是 `[LLM]` | 判断逻辑标 LLM，可验证执行标 Deterministic |
| **Hard Rules** | 不可违反的行为约束，优先于一切其他考虑 | 编号列表，每条可判定 |
| **Failure Handling** | 失败场景 → 动作的决策表 | 覆盖输入缺失、外部依赖失败、数据不足、意图越界 |
| **Output Format** | 输出的精确结构 | 文件路径、章节骨架、字段——agent 照此生成 |

### 8. 风险警告写法

**写行为类别的通用原则，不写具体机制。**

| ✅ 安全写法 | ❌ 危险写法 |
|---|---|
| "AI guidance is probabilistic; require human review before execution" | "executable rules can take action (red-line reductions)" |
| "all action triggers require human review" | "`send_*.py` pushes holdings to external messaging platforms" |

原因：具体能力会被扫描器双向误读——既读成能力承诺（与 description 矛盾），又读成风险路径（数据外发）。同一句话可同时触发三层 finding。

---

## 第四部分：审计与脱敏

### 9. 泄漏扫描清单

发布前对全部文件扫描：

- 个人路径与用户名（home 目录、`.workbuddy` 等）
- 凭据形态（token 前缀、API key 模式、Authorization 头）
- 数据库与文档 ID
- 公司与产品专名（产品线命名、内部系统、客户名）
- 内部约定（私有阈值、渠道配置、内部流程术语）

**区分代码与数据**：检测凭据的正则表达式代码是代码，不是泄漏——扫描命中后人工确认语义再放行。

### 10. 私有 skill 公开化

私有 skill 发布脱敏版的原则：

1. **保守 patch**——只改 frontmatter 和通用段落，不重写正文
2. 私有约定（内部阈值、渠道限制、私有命名）不进公开版
3. not_for 已有的高质量边界声明保留不动
4. 私有版与公开版各自演进，公开版更新频率刻意低于私有版

---

## 第五部分：发布

### 11. 发布分级（Release Type Gate）

| 级别 | 定义 | 要求 |
|---|---|---|
| **新 skill** | slug 不存在于平台 | 全流程：脱敏 → 结构完整性 → 审批展示 → 发布 → 安装验证 |
| **内容更新** | 新增 references / 新章节 / scope 变化 | 脱敏 → 审批展示 → 发布 |
| **patch** | 措辞、frontmatter、版本号 | 脱敏 → 发布 |

**核心纪律：指令是做事的授权，不是跳过质量流程的授权。** 用户说"发"之后，新发布仍需展示将要发布的完整内容（slug / 版本 / description / 文件清单）等待确认。批量操作最容易在这里失守——第一个走捷径，后面全部沿用。

### 12. slug 预检

发布前必须检查 slug 归属：

- 平台查无此 slug → 可发布
- 返回自己的 skill → 正常 bump 版本
- **多 owner 同名（AMBIGUOUS）→ 换 slug，绝不硬发**

硬发同名 slug 会产生 ghost record：slug 索引有记录、owner 查询找不到，CLI 永久报错且无修复接口。此时唯一出路是换新 slug 重发，旧记录自然流失。

### 13. 双平台适配

| 维度 | ClawHub | SkillHub |
|---|---|---|
| 中文位置 | `description_zh` 字段 | `description` 字段内嵌（搜索只索引 description） |
| 扫描器 | SkillSpector | 无同类 |
| 版本历史 | 累积 changelog | 覆盖式——每次 publish 重置历史显示 |
| 文件限制 | 宽松 | 部分文件类型不允许（如 LICENSE） |

**已知坑**：经平台间自动同步渠道创建的 skill，后续 CLI 发布报"已存在"但搜索不到（隐藏记录）。发布失败先查原因再重试——立即换版本号盲重试有制造重复记录的风险。

---

## 第六部分：安全对抗

### 14. 扫描器三层诊断

安全/策略扫描器报 finding 后，**先诊断层级再动手**：

| 层 | 信号 | 修法 |
|---|---|---|
| **L1 表面** | finding 引用 frontmatter 措辞 | 改措辞 |
| **L2 行为不匹配** | 引用正文步骤，根因是 description 与正文矛盾 | 对齐二者（改任一侧） |
| **L3 能力本身** | 问题在 skill 的核心能力（第三方画像、可执行交易、数据外发） | 设计决策——接受 finding 或重构 scope，措辞修复无效 |

### 15. 修复与回滚原则

1. **不反射性地加免责声明或收窄触发词。** 对 L2/L3 这样做往往制造新的矛盾面（声明说 A、正文做 B → 新的 L2）。
2. **修复两轮后 finding 反而增加 → 回滚。** 每个 frontmatter 新字段都是扫描器的新分析面。回到最后通过版本的 frontmatter + 保留正文实质改进，是最快路径。
3. **平台 moderation CLEAN 但第三方扫描器仍报 → skill 已可用。** 第三方 finding 是信息性的，不阻断安装。是否继续修取决于是否反映真实风险。

### 16. 冻结机制

内容本身站在政策线上的 skill（第三方人格侧写、可执行交易框架），**非必要不更新**——每次重发都是一次重新扫描。必须更新时：frontmatter 保持最小、只改正文、改前预判扫描器的读法。

---

## 第七部分：维护

### 17. 版本语义

| 变化 | 版本 |
|---|---|
| 破坏性变更（接口、输出格式不兼容） | major |
| 新章节、新 references、scope 调整 | minor |
| 措辞修正、frontmatter 补充、元数据 | patch |

### 18. 审计节奏

定期盘点线上全量：版本、更新时间、moderation 状态、与本地 diff。动作规则：

- 有实质增量 → 发布
- 本地落后线上 → 不反向推
- 同版无 diff → 不动
- 超期未更新但无增量 → 按 frontmatter 标准对齐补 patch（如补 not_for）

**审计防误判**：结构检查用不区分大小写的匹配——"Hard rules" 与 "Hard Rules" 是同一要素；步骤是否带 `[deterministic]` 标签比章节标题命名更能反映结构完整性。

### 19. 经验回流

每次踩坑提炼的原则，回写进两个治理 skill：

- **设计原则** → skill-design-guide（本文档的维护主体）
- **发布流程** → skill-audit-publish（Release Type Gate / 诊断框架）

让下一次执行自动继承，而不是依赖对话记忆。本文档每次重大经验后更新版本号并在更新日志记录。

---

## 反模式速查

| 反模式 | 修正 |
|---|---|
| 过度工程 | 从单个 SKILL.md 开始 |
| 全量预加载 | references 按需加载 |
| 上帝 Skill | 一个 skill 做一件事 |
| 全 LLM | 确定性步骤用脚本 |
| 无护栏 | 四要素齐全 |
| 模糊输出 | Output Format 定义精确结构 |
| 关键词堆砌 | 精确能力陈述 |
| 缺 not_for | 按相邻任务域补排除 |
| 免责声明堆砌 | 风险警告写通用原则 |
| 同名 slug 硬发 | 预检，冲突即换名 |
| finding 后反射加声明 | 先诊断层级 |
| 修复越修越多 | 回滚 frontmatter |
| 私有约定进公开版 | 脱敏检查 |

---

## 更新日志

- **v2.0.0**（2026-08-24）：全面重写。新增 agent-first 认知框架（Principle Two）、frontmatter 路由规范、风险警告写法、审计脱敏、发布分级、slug 预检、双平台适配、扫描器三层诊断、回滚原则、冻结机制、版本语义、审计节奏、经验回流。取代 v1.4.x 作为权威版本。
- v1.4.3（2026-06-23）：恢复显示名称；目录合并
- v1.4.0（2026-06）：渐进式加载重构
- v1.3.0：添加使用场景，中英双版本
- v1.2.0：平台无关化重写
