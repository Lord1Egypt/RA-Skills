---
name: Signal-Search
description: 答案质量层搜索/增强检索 skill：搜信息、做调研、对比、查资料、信源比对、事实核查时启用。不做链接列表——返回带加权打分(SBA)、事实级来源锚定(M51)、分层深度(L0–L3)与 token 预算封顶的干净答案；无广告、零 key、可嵌入，被其它 skill 当检索原语调用（由调用方注入 LLM 与抓取能力）。
version: 1.2.0
---

# Signal-Search

一款"搜索 + 增强搜索"工具产品：对外暴露干净检索原语 `retrieve(query, constraints, budget)`，按需求复杂度在 L0–L3 自动路由、动态选源、控 token 预算、对信源自动比对打分、证据足够即自动停止。被其它类别工具当"检索能力"消费——**不是用来编排其它搜索 skill**。

**答案质量层定位**：答案质量 > 链接数；无广告、直接给答案；引用真实可溯（M51 事实级锚定，可导出 BibTeX/Markdown/RIS/CSL/NoteExpress）；分层深度（`depth="quick|standard|deep"`）；更轻——库而非产品，不绑 LLM、不 spawn agent、无多模态/前端，LLM 与抓取由调用方注入。真·子 agent 派发由调用方注入 `agent_fn`（库不 spawn agent）；HITL 大纲确认交互见 `scripts/research_cli.py`；参考模板见 `examples/agent_dispatch.py`。

## 何时用
用户要搜信息、做调研、对比、查资料，或别的 skill 需要检索时。

## 标准调用契约
`retrieve(query, constraints={language,domain,freshness,max_sources,required_tier,source_prefs}, budget=token软上限)`
→ `{findings, sources[], scores[], confidence, token_used, exhausted, tier_used, trace}`
（详见 `references/` 各规范与 `scripts/` 实现；config.json 为引擎单真相源。）

## 档位路由 L0–L3
- **L0 速查**（日期/语法/命令/定义，唯一可验证）→ 预算 2k，1 源，禁思维链。
- **L1 单点**（谁/多少/是什么）→ 预算 8k，1–3 源。
- **L2 诊断/方案**（对比/为什么/怎么选/风险）→ 预算 30k，3–8 源，多源对比+验证。
- **L3 研究**（调研/前沿/学术）→ 预算 100k，≤20 源，planner→并行 crawler→publisher。
- 默认 **L1**；用户可 `/signal L3 调研 X`、`/signal L2 对比 A B` 显式覆盖。详细规则见 `references/tier-policy.md`。

### 档位速查表（该选哪一档）
不确定时默认 **L1**；涉及"对比/风险/为什么"升 **L2**；"调研/学术/前沿"升 **L3**。

| 你的查询长这样 | 推荐档位 | 触发写法示例 | 说明 |
|---|---|---|---|
| "今天周几" / "Python 怎么读文件" / "GDP 是什么" | **L0 速查** | `/signal 今天周几` | 单一可验证事实，最省 token |
| "iPhone 17 起售价" / "北京常住人口多少" | **L1 单点** | `/signal iPhone 17 起售价` | 一个明确事实点 |
| "A 与 B 哪个好" / "为什么通胀" / "方案怎么选" | **L2 诊断** | `/signal L2 对比 方案A 方案B` | 需多源对比、强制反面论证防偏颇 |
| "XX 技术最新进展" / "XX 领域综述" / "XX 风险研究" | **L3 研究** | `/signal L3 调研 XX 技术` | 需文献/多源深挖、planner→并行 crawler |

> 口诀：事实速查用 L0/L1，要"比"和"为什么"用 L2，要"深"和"学术"用 L3。

## 意图与查询规划
先判意图（`fact/compare/howto/why/research/latest/verify`），`confidence<0.6` 向用户澄清（最多 1 轮）。再按四范式拆解：成分型 fan-out 并行 / 多跳串行 / 实体锚定 / 迭代重写。宽度上限 L2≤8、L3≤20。方法论见 `references/intent-decomposition.md`。

## 信源打分原则（SBA）
每源五维（credibility/relevance/recency/authority/bias），综合 `weighted=0.35·cred+0.30·rel+0.15·rec+0.15·auth+0.05·(1−bias)`。**按 weighted 加权合成，不按数量投票**；冲突：高 weighted 优先，低 weighted 显式标"存在相反观点"。内置可信度表见 config.json。

## 自适应停止原则
- L0/L1（缩范围）：预算即停，标 `exhausted=False`；1–2 源一致即停。
- L2/L3（保覆盖）：覆盖饱和度即停（子问题全答/引用收敛/单源饱和/缺口闭合）；预算仅兜底，先到未饱和须标 `exhausted=True` 且不静默标完整。
- "决定不检索"是一等能力：**`research()` 现在在检索前自主判定**——空/纯寒暄、关于本能力自身的提问、过于含糊无实体的疑问，直接拒答或澄清（返回 `skipped`+`skip_reason`），不浪费检索与落盘；正常 L0–L3 可检索查询一律放行。判定见 `route.should_skip_search`（`decide_not` 为其兼容别名）。每次停止必写 `trace.stop_reason`。详见 `references/tier-policy.md` §4。

## token 预算原则
软上限 + 早停；到顶停并标注 `exhausted`。省 token 七法（prompt 裁剪/上下文剪枝/预检索过滤/工具输出压缩/prompt caching/输出长度控制/模型路由）见 `references/token-optimization.md`。每多花一批 token 前问"会改变结论/动作吗"，答否即停。

## 验证护栏
- 只引 `sources` 中**实际抓取**的 URL；未抓取标"待核实"。
- **事实级核验（M51）**：findings 拆原子事实 → 逐条与 source 片段做蕴含判定 → TRUE/FALSE/UNCERTAIN；UNCERTAIN 显式标"待核实"，不计入已支持，faithfulness 按原子事实计。
- L2/L3 强制**反面检索**（`criticism/limitations/失败/无效`）。
- 结论依赖代码必须实际执行验证（"读过即跑"）。
- 合规护栏（默认开）：尊重 robots.txt、PII 脱敏不落库原文、限速 ~1req/14s、登录墙/付费墙源跳过。见 `references/anti-scraping.md` §6。

## 被其它类别工具调用（辅助补齐检索短板）
作为检索原语被 ChatGPT、Claude、Perplexity、Kimi、Gemini 等 AI 助手，以及各类投研、调研、深度分析工具消费——它们各自在自身领域强、但做检索差。Signal-Search **只返回带打分与置信度的干净结果，不替调用方决策**。

**接入 LLM 的默认行为 = 调用方 LLM 自动接管**：当调用方（上层 agent / 调用本 skill 的 LLM）需要接入 LLM 时，**默认激活的就是该调用方 LLM** 来充当 `agent_fn` / `tier_classify_fn` / `conflict_check_fn`——哪个 LLM 调用就用哪个，无需用户注入、无需额外配置。M51 语义冲突检测同理：`conflict_check_fn` 由调用方把其 LLM 包成回调注入（参考实现见 `examples/conflict_llm.py` 的 `make_llm_conflict(llm_fn)` 适配器），**库内不持有任何 LLM key、不 spawn 第二条连接**。学术源 DOI 回填同理：`doi_resolver` 由调用方注入其书目源（S2/Crossref/自有库），**库内不内置任何书目源、不读环境变量**。未接 LLM 时库内启发式降级（内部按维度 `retrieve()` + 规则分档 + M51 零检测），零依赖可跑。

## 已实装质量层能力（P0–P2 缺口修复）
以下能力均已落地并通过单测回归；零依赖为默认路径，重依赖（sentence-transformers 等）一律 config 开关、默认关、try/except 降级。

- **自主不检索（P0-3）**：`research()` 检索前用 `route.should_skip_search` 判定；空/寒暄、关于本能力自身的提问、过于含糊无实体的疑问 → 直接拒答/澄清（`skipped`+`skip_reason`），不检索不落盘。
- **置信度=答案正确性（P0-2）**：`report.confidence_of` 由"来源打分均值"改为融合 **M51 TRUE 率 + 引文真实率（VERITAS）+ 不确定性条数** 合成，度量"答案对不对"而非"来源像不像"。
- **M51 事实锚定加固（P0-1）**：否定/极性检测 + 关键实体（数字/专名）命中 + 锚定覆盖阈值三道闸门，堵住"共享≥1词即 TRUE"的假 TRUE；语义后端（sentence-transformers）经 `semantic_fact_verify`+`embed.py` 可选启用。
- **时效性衰减（P1-4）**：`score._recency` 抽年份 → 按 `freshness` 窗口线性衰减，接入打分与排序；近窗口查询优先新闻类引擎（若配置）。
- **预算线性修正（P1-5）**：`budget.estimate` 按查询长度 + 子问题数线性修正，封顶不出界。
- **失败可见性（P1-6）**：connector 抓取 warnings 显式进入 `research()`/`orchestrate` 返回 `meta.warnings`。
- **Vault 默认关（P1-7）**：`research()` 默认纯内存，仅显式 `vault_dir` 或 `cfg.research.vault_enabled=True` 才落盘，避免污染 cwd。
- **缓存默认开（P2-10）**：`cache` 默认启用，带 TTL + 内容哈希，避免重复检索（默认关硬门槛中其余增强项仍保持关）。
- **内联引用 M31（P2-9）**：`report.synthesize` 输出行内 `[n]` 标记 + 编号来源列表，论断句↔来源可追溯。
- **多语种分词（P2-11）**：`common.tokenize` 对 CJK 拆 1–3 gram、其余脚本按词切分（覆盖 ja/ko/ar 等）；增强版见"补强"。
- **可嵌入 SDK（P2-14）**：`research_cli.research(query, on_progress=...)` 非交互、带阶段进度回调（`start/tier/skipped/outline/warnings/done/error`）；HITL 大纲确认见 `research_interactive`。

## 补强（零依赖重实现，P2 增强项加深）
在前序 P0–P2 轻量实现基础上，对三项做"更重"的零依赖实现；均保持默认关/零依赖路径、不触碰合约硬门槛，并已通过单测回归（rerank 24+6、dedup、tokenize 各用例全绿，eval 离线命中率 1.0）。

- **语义 rerank（零依赖重排）**：新增 `scripts/rerank.py`，复用 `embed.py` 的真实/降级（64 维关键词哈希）向量做"查询 × 候选源"余弦重排；`method` 支持 `semantic`/`bm25_rrf`/`hybrid`（α 融合），结果写入独立 `rerank_score` 键，`orchestrate.retrieve` 在截断前接入、`report` 在有该键时优先按它排序与呈现。`config.rerank.enabled` 默认 `false`（合约硬门槛），仅开启且非 `SIGNAL_SEARCH_OFFLINE` 时介入；无 sentence-transformers 自动走降级向量、不强制加载重依赖，embed 任意异常均降级 lexical 基线、绝不让主检索崩溃。
- **simhash 主通道去重**：`dedup.near_dup` 升级为 simhash 64-bit + 4×16-bit LSH 分桶主通道（汉明距 ≤ threshold 即近似重复，`threshold` 形参真正生效），Jaccard 词重叠作全量二级兜底（覆盖"措辞不同但词集高度重叠"的短摘要），URL 精确去重与保序不变；性能由 O(n·m) 全配对降至近 O(n)（结果集 ≤ max_sources）。
- **多语种分词增强**：`common.tokenize` 由"纯 CJK 2-gram"增强为 CJK 段 1–3 gram + 内置紧凑词典最大正向匹配（捕捉更完整词边界），日文假名纳入 n-gram，韩文/阿拉伯文等按 Unicode 词切分；仍零依赖、纯正则/内置词典，且为旧 bigram 行为的超集，不破坏以 tokenize 为输入的打分/去重语义。

## 渐进式披露
`config.json` 激活时读（引擎单真相源）；`references/*.md` 与 `scripts/*.py` 按需读（反爬/意图/档位/省 token/金标准集等详版）。

## 常见问题（FAQ）
- **Q：结果会缓存吗？** 会，且默认开（`cache.enabled=true`），带 TTL + 内容哈希，相同/近似查询直接命中，避免重复检索，无需手动管理。
- **Q：中文搜索质量一般怎么办？** 默认中文引擎（百度/搜狗等）偏"水"。专业/学术场景请在 `config.json` 启用 `academic` 类源或接入 Tavily 等付费 API；也可在 `constraints` 用 `source_prefs` 指定只用权威源。
- **Q：语义核验 / rerank 需要装重依赖吗？** 不需要。`config.rerank.enabled` 与语义后端（`sentence-transformers`）均默认关；未安装时自动走零依赖降级向量与启发式，不强制加载重依赖、不崩溃。
- **Q：怎么只用某类源（只搜国内 / 只搜学术）？** 在 `constraints` 设 `domain`（`CN`/`INT`/`ACADEMIC`）或 `source_prefs`；`config.json` 的 `engines` 按 `region`/`best_for` 分类，可组合过滤。
- **Q：什么情况下它"决定不检索"？** 空/纯寒暄、关于本能力自身的提问、过于含糊无实体的疑问——`research()` 检索前用 `route.should_skip_search` 判定，返回 `skipped`+`skip_reason`，不浪费检索与落盘。
- **Q：TLS 证书校验能关吗？** 默认开启（更安全）。仅当在**受信任的内网或测试环境**时，才可在 `config.json` 设 `scrape.tls_verify=false`；关闭后会打印一次 MITM 风险提示并写入 `meta.warnings`。公网环境务必保持开启。
- **Q：离线环境能用吗？** 可以。设 `SIGNAL_SEARCH_OFFLINE=1` 后，语义 rerank 等需联网能力自动退避、降级为 lexical 基线，主检索不受影响。

## 限制与警告汇总
- **中文默认引擎偏水**：专业/论文级结论建议启用 `academic` 源或接付费 API；中文学术库通常只能取到题录摘要，全文需接机构库。
- **需调用方注入 LLM**：M51 语义冲突检测、语义 rerank 等依赖 LLM/向量后端，由调用方以回调注入；**库内不持有任何 LLM key、不读环境变量、不 spawn 第二条连接**。未注入时走零依赖启发式降级。
- **合规护栏（默认开）**：尊重 robots.txt、PII 脱敏不落库原文、限速约 1 req/14s、登录墙/付费墙源自动跳过。
- **TLS 校验（默认开）**：`scrape` 默认校验证书；仅受信任内网/测试可关 `scrape.tls_verify=false`，关闭有中间人劫持风险。
- **失败隔离**：单源不可达/超时自动跳过并写入 `meta.warnings`，不会让整个检索崩溃；`meta.warnings` 可见，便于排查。
- **预算封顶**：到达 token 预算即停并标注 `exhausted`；L2/L3 以覆盖饱和优先，预算仅兜底。
