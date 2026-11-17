# Signal-Search

> 很多人在钻研搜索，很少人在乎答案。

Signal-Search 是一个**答案质量层**。它不返回一堆链接让你自己挑——它返回经过加权打分、事实锚定、预算封顶的干净答案。无广告，引用可溯，深度随问题自适应，零成本可嵌入到别的工具里。

一行定位：检索原语 `retrieve(query, constraints, budget) → {findings, sources, scores, confidence, token_used, exhausted, tier_used, trace}`。

---

## 为什么不是又一个搜索工具

多数搜索工具做三件事：**返回一个链接列表、按商业排序塞广告、把来源的真假交给你判断。**

Signal-Search 把起点换掉了——先想清楚你要的到底是什么，再决定查多深、花多少、信哪些。这不是又一个引擎列表，而是一层**调度智能**：把"检索深度 / 信源选择 / token 预算"动态匹配到当前任务。

说到底，我们和别的搜索工具在乎的不是同一件事。它们数的是"又抓回了多少条"；我们盯的是"你问的那一个，到底答对了没有"。所以同样是搜，我们替你多做几步：把问题想透、再去查、查到够为止，最后只把能站住脚的结论递给你——每条还标出来源，你不光能看，还能自己复核。

---

## 三个不同

**1. 答案质量层，不是链接列表**
- 每条结论按 **SBA（信源加权打分）** 排序，冲突观点并存而非被吞掉。
- 每条事实锚定到**真实抓取的 URL（M51 事实级锚定）**，可导出 BibTeX / Markdown 引用。
- 不确定的，明说"待核实"——不假装知道。

**2. 深度自适应，且知道何时停下**
- **L0 速查 → L3 深度研究**，库按问题复杂度自动选档，你也能一句话指定深度。
- **token 预算封顶**：每多花一批 token 前先问"会改变结论吗"，答否即停。
- "**决定不检索**"是一等能力——无谓检索反而降质，这有论文支撑（TASR 2025：固定 k=5 检索仅 62.6% 调用量即达 94.8% 效果）。

**3. 更轻，可嵌入，零 key**
- **库，不是产品**：不绑 LLM、不 spawn agent、无多模态 / 前端，可随手嵌入。
- **零密钥自持**：LLM、抓取、书目源都由调用方注入，库内不持有任何 key、不 spawn 第二条连接。
- **被其它工具当检索原语调用**——ChatGPT、Claude、Perplexity、Kimi、Gemini 等 AI 助手，以及各类投研、调研、深度分析工具，拿去补自己的检索短板，只拿干净结果，不替它们决策。

---

## 对比知名 agent 搜索 / 深度研究工具，我们创新在哪（联网盘点 2026-08）

下文盘点业界公认、口碑高的 agent 搜索与深度研究工具，作为对标对象（数据来自 2026 年公开评测与厂商披露：ai-pedias、aiagentrank、aisotools、极客公园、界面新闻、今日头条、稀土掘金、CSDN 等）。它们强在哪、弱在哪，一张表说清 Signal-Search 补的是哪一层。

**海外（agent 搜索 / 深度研究）**
- **Perplexity**：最出名的 AI 搜索，"直接给带引用的答案"开创者；Pro Search 深度研究、Focus 模式（学术 / YouTube / Reddit）；免费有限 + Pro $20/月。NewsGuard 实测其约 47% 会复读虚假信息（2025-08）。
- **OpenAI ChatGPT Search / Deep Research**：内嵌 ChatGPT，对话式联网、行内引用；Deep Research 自主浏览产出 5–30 分钟、带密集引用的报告；Plus $20/月。
- **Google Gemini / AI Mode / Deep Research**：原生谷歌搜索 + Gemini；Deep Research 长程规划-浏览-写简报；AI Mode 免费。2026 年 Gemini 在开放网络推荐份额激增近三倍（BrightEdge，2026）。
- **Microsoft Copilot / Bing**：集成必应；官方自己写"仅供参考、勿用于重要建议"（TechCrunch 2026-04）。
- **Brave Search（Leo）**：独立索引、不追踪；Leo 助手带引用；免费 + Premium $3/月。
- **Kagi**：付费无广告、可高度定制；$5–25/月。
- **You.com / YouPro**：agentic 搜索，多步研究 + 引用 / 代码 / 图像模式；$15/月。
- **Phind**：开发者向，代码优先答案带引用；免费 + Pro $20/月。
- **Felo**：跨语言搜索，自动脑图 / 幻灯片；$14.99/月、有免费档。
- **Genspark**：把结果合成结构化 "Sparkpage" 文章、多智能体 Super Agent；免费 + Plus $19.99/月，宣称无广告无 SEO 操纵。
- **Manus**：通用自主智能体，云端规划-浏览-写码-执行，信用点计费，免费档 + ~$20–200/月。

**国内（中文 AI 搜索主力）**
- **秘塔 Metaso**：中文口碑最佳，"无广告直达"；"先想后搜 / 先搜后扩"直至逻辑闭环、Agentic Search 一次 5–15 步工具调用、学术覆盖 PubMed / 中科院分区；免费 + API 按量。
- **Kimi（月之暗面）**：百万级上下文，联网搜索 + 文件分析，深度研究 / Agent / PPT；免费。
- **360 纳米 AI 搜索（n.cn）**：无广告、多模型协作、文件解析、脑图 / PPT；免费 + ¥19.9/月起。
- **天工 / 智谱清言 / 豆包 / 腾讯元宝 / 文心 / 百度 AI 深度搜索** 等：综合 AI 助手或搜索底座，覆盖日常与国内政务 / 百科场景（CSDN 2026 国内 15 家盘点）。

| 你真正在乎的 | 知名 agent 搜索工具（Perplexity / 秘塔 / ChatGPT / Manus…） | Signal-Search |
|---|---|---|
| 源覆盖谁说了算 | 厂商固定一套源，你接不进自己的私有库 / 学术库 / 内部知识库 | 你喂什么源就用什么源——`web_fetch=` 传你的学术库、内部库、干净 API，**源覆盖上限 = 你接入的总和** |
| 该查多深 | 档位由产品定（秘塔三档、Perplexity Deep Research 2–4 分钟、ChatGPT / Gemini Deep Research 5–30 分钟），你改不了 | **L0–L3 按复杂度自适应路由，你也能一句话指定**，token 预算封顶 |
| 来源可信吗 | 引用质量参差、照样幻觉：NewsGuard 测 Perplexity ≈47% 复读虚假信息（2025-08）；Relum 测 ChatGPT 35% / Gemini 38% 幻觉率（2025-12）；哥伦比亚大学 Tow Center 测生成式搜索源识别错误率偏高 | **SBA 加权打分 + M51 事实锚定到真实抓取 URL + 强制反面检索**，存疑明说"待核实" |
| 广告 / 立场 | Google AI Overviews 已插广告（2025 起）；微软自写"Copilot 仅供参考、勿用于重要建议"（TechCrunch 2026-04） | **无广告、不按商业立场排序**，不确定就标"待核实" |
| 能嵌进我的工具吗 | 多为完整闭源产品 / 按量 API（Perplexity $20、You.com $15、Kagi $5–25/月、秘塔 API 按量） | **检索原语契约，零 key 可跑**，被其它 skill 直接消费，需更强能力时由调用方注入 LLM / 抓取 |
| 成本可控吗 | 订阅制 / 按量计费，检索尽力而为无预算 | **token 预算 + 早停**，超支即标注、不静默截断 |
| 更轻 | 多为完整产品，自带多模态 / 前端 / 自研 Agent（Manus / Genspark 还产 PPT、打电话） | 库而非产品，专注质量层，重活交给调用方 |

**一句话讲透定位**：它们是"固定源 + 固定产品"的搜索产品；Signal-Search 是"调度智能 + 你自己的源"的质量层。只要把**网址 + key** 接进 `web_fetch` / `docs`——Perplexity 的干净 API、Tavily、Exa、arXiv、Semantic Scholar、你的内部知识库——**源覆盖上限 = 你接入的总和**；它们做不到的"用你的源、按你的深度、在你自己的工具里跑"，正是我们的主场。

> 数据来源（公开披露，2025–2026）：Relum《AI 可靠性报告》（2025-12，幻觉率）；NewsGuard（2025-08，实时新闻虚假信息复读率）；哥伦比亚大学 Tow Center 生成式搜索溯源测试（源识别错误率）；TechCrunch（2026-04-05，Copilot 服务条款 disclaimer）；Google 官方博客（AI Overviews 广告上线）；Brave / Kagi / 秘塔 Metaso 官方（定价与模式）。具体数值以各来源最新披露为准。

---

### 接入你自己的知识库（私有源 / 内部资料库）

别的搜索产品吃的是厂商固定的公开网；Signal-Search 让你把**自己的**知识库、公司内部资料库、甚至一个内部 API，当作一等源接进来——和那 65 个公开源走同一套质量层（加权打分、事实锚定、去重、预算封顶），不是外挂、不是事后拼接。

接法只要一段配置，不用写一行代码：

```json
// config.json → clean_sources.custom_sources
[
  {
    "id": "my_kb",
    "name": "公司内部知识库",
    "url_template": "https://kb.internal/api/search?q={q}",
    "json_items": "results",
    "item_map": {"url": "link", "title": "t", "snippet": "s"},
    "quality": "A",
    "source_type": "internal"
  }
]
```

- `{q}` 自动编码成查询词；返回 JSON 按 `json_items`（结果数组路径）+ `item_map`（字段映射）抽成统一文档。
- 要带鉴权：模板里放 `{token}`，设 `"key_env": "KB_API_KEY"`，值从环境变量读入——没填 key 就不激活（opt-in），不泄露也不联网。
- 想让它只在相关查询时出现：加 `"topics": ["corp"]`；什么都不写则默认**每次都打**（你主动接的源，就该被打）。
- 接进来后，它在 SBA 打分里和公开源**平等竞争**——内部资料若质量高，自然排到前面。这样"源覆盖上限 = 你接入的总和"才真正落地，而不是一句口号。

---

## 开箱即得干净源（含国内权威）

默认开（config `clean_sources.enabled: true`，零 key、零配置）。库内预灌 **65 个干净源**，按 `source_type`（academic / gov / vendor / unknown）进 SBA 加权打分——不是又一个链接列表，而是已经按信源权重排好序的干净材料。

**三档可切（config `clean_sources.default_tier`）**

| 档位 | 覆盖范围 | 源数 | 何时用 |
|---|---|---|---|
| `lite` | 国际通用引擎 + 通用参考（维基 / 维基数据 / 互联网存档） | 12 | 速查、省流量 |
| `standard`（默认） | `lite` + 学术 API + 权威标准 + 国外行业 keyless + 国内权威 + 隐私/独立引擎 | 61 | 通用调研、投研、学术 |
| `full` | 同 `standard`（隐私/独立引擎已并入） | 61 | 与 `standard` 当前等权，预留扩展位 |

**源分八类（quality 为注册表元数据 + `describe_clean_sources()` 报告用；打分实际走 `source_type`）**

1. 国际通用引擎 ×9（Google / Google 香港 / DuckDuckGo / Yahoo / Startpage / Brave / Ecosia / Qwant / WolframAlpha，B 档，默认开）
2. 通用参考 ×3（Wikipedia / Wikidata / Internet Archive，A 档）
3. 学术 API ×7（OpenAlex / Crossref / Semantic Scholar / PubMed / Europe PMC / bioRxiv / arXiv，A 档，多 keyless REST）
4. 权威标准 ×8（W3C / IETF RFC / WHATWG / MDN / Unicode / TC39 / OpenAPI / GitHub，A 档）
5. 国外行业 keyless ×16（SEC EDGAR / World Bank / ClinicalTrials / openFDA / CourtListener / DataEuropa / NOAA / USGS / NASA / IMF / OECD / WHO / CDC / ECDC / UK data.gov.uk / RePEc·IDEAS，A 档）
6. 隐私/独立补充 ×3（Mojeek / MetaGer / SearxNG，B/A 档）
7. 国内权威 ×15（国家标准全文公开系统 / 国家法律法规数据库 / 国家企业信用信息公示系统 / 中国政府网 / 国家统计局 / 国家自然科学基金委 / 中国科学院 / 国家哲学社会科学文献中心 / 中国知网 / 万方 / 国家科技图书文献中心 / 国家药监局 / 中国临床试验注册中心 / 国家卫健委 / 国家科技基础条件平台，A/B 档）
8. AI 原生搜索 API ×4（Tavily / Exa / Perplexity / Brave Search API，**默认关、env 注入即活**）

**和"调用方注入"不冲突：三条要点**

- **`web_fetch=` 仍最高优先**：你传了抓取器，库就改用它，绕开全部内建源——这是既定契约，干净源只是在"你没传"时补位。理论上，只要把网址 + key 接进 `web_fetch` / `docs`，**我们的源覆盖上限 = 你接入的总和**。
- **`keyless_meta` 源只给题录**：知网 / 万方 / 国家哲学社会科学文献中心 / 国家科技图书文献中心为 `keyless_meta`，默认只回题录/摘要级数据；要全文，把你的机构库/书目源通过 `web_fetch=` 注入即可。
- **keyed AI 搜索 API 留门**：Tavily / Exa / Perplexity / Brave 默认不激活（无 key 不联网），在 config 或 env 填 `TAVILY_API_KEY` 等即活，走统一质量层。

**健壮性**：CN 沙箱内不可达的源（如偶发封锁的政府站点）自动静默跳过，不影响其它源；测试/离线环境下默认不触发联网（可用 `SIGNAL_SEARCH_CLEAN_ON` 强制开、`SIGNAL_SEARCH_OFFLINE` 强制关），不破坏现有门禁。

> 源清单、分类、`source_type`、`quality` 与每源可达性快照，运行 `from clean_sources import describe_clean_sources; print(describe_clean_sources())` 实时查看。

### 源路由：按需选源，不再全扇出

源越多越不能每次都打全部——那等于把 PubMed / IMF / 国家法律法规库一并灌进同一次查询，既浪费网络与延迟，又让无关源噪声稀释 SBA 打分。这是检索系统的经典「数据库选择 / 源路由（source routing）」问题，已有大量实证研究支撑本设计：

- **RAGRoute（arXiv:2502.19280）**：over-selecting 会稀释相关性、引入噪声，需轻量路由器只选相关子集；
- **Learning to Route（arXiv:2510.02388）**：规则路由胜过静态全连，盲连多源反而降质；
- **Agent-Level MoE（agentpatternscatalog / programmer.ie）**：最朴素路由器就是 Python 关键词规则——**零 key、零延迟、确定性**。

本库默认开启源路由（config `clean_sources.routing`），`build_clean_fetch` 在并发前先 `select_sources(query, sources, cfg)` 过滤，**下游去重 / SBA / M51 全不变**：

- **通用保底**：9 个国际引擎 + 3 个参考源**始终纳入**（召回地板，避免漏通用信息）；用户显式注入 key 的 keyed 源也始终纳入（尊重 opt-in 意图）。
- **主题专家源**：中英关键词词典识别查询意图（学术 / 开发 / 金融 / 宏观 / 医疗 / 法律 / 政务统计 / 气候航天 / 隐私 / 国内权威），按命中强度降序加入，受 `max_sources`（默认 16）截断。例：「深度学习最新论文综述」→ 仅加 OpenAlex / Crossref / SemanticScholar / PubMed；「最好的咖啡机推荐」→ 只打通用引擎，**零噪声源**。
- **未识别主题**：默认仅返回保底集（通用查询不再误伤专业源）；`fallback_to_tier: true` 时才补满其余源保召回。
- **绝不空打**：保底集恒非空；`mode: "off"` 或 `enabled: false` → 退回全扇出旧行为，**向后兼容零差异**。
- **LLM 路由器 = 调用方注入**（零 key 默认）：`build_clean_fetch(..., router_fn=callable)` 传入 `(query, candidates) -> List[source]`，即用即用，无则启发式。

| 配置项 | 默认 | 含义 |
|---|---|---|
| `routing.enabled` | `true` | 总开关 |
| `routing.mode` | `select` | `select` 按需选源；`off` 全扇出（旧行为） |
| `routing.max_sources` | `16` | 单次并发源数上限（保底 ~12 已计入） |
| `routing.include_general_floor` | `true` | 始终含通用引擎保召回 |
| `routing.fallback_to_tier` | `false` | 未识别查询是否补满整档 |
| `routing.router` | `heuristic` | 默认启发式；调用方经 `router_fn=` 注入 LLM 路由 |

## 实测说了算

- **230 passed**（pytest，含源路由 / 私有源接入 / 缓存与并发单测）/ **金标准档位命中 24/24** / **pyflakes 零告警**（隔离 venv 复验，2026-08-14）。
- 真实抓取：`retrieve("TCP 和 UDP 的核心区别")` 命中 baike.baidu.com 真实答案页，M51 首次把每条事实锚定到真实 URL，不再是空壳。
- 研究编排层 `research()` 圈复杂度 53→12，顶层 `retrieve()` 52→B 档以下——重活都被拆成单一职责，好维护、好测。

---

## 如实说

我们把局限摆出来，因为含糊其辞才是真风险：

- **默认引擎收敛为百度 / 搜狗**（轻量优先），其余 9 个国际引擎（Google / DuckDuckGo 等）已预灌进干净源、由路由层按需调用，调用方也可用 `web_fetch` 抓好后喂入——不是少，是更轻。
- **默认事实锚定是关键词基线**；语义级核验需本地装 `sentence-transformers`（~1GB），缺失自动降级，不报错。
- **落地页抓取受合规限速偏慢**（默认 ≈14s/请求），开 `cache.enabled` 可显著提速。
- **SearXNG 需本地 Docker 实例**，代码已接入、单测齐全，待你激活。
- **中文 SERP 噪声大**：默认引擎（百度 / 搜狗）的落地页多为 SEO 聚合、营销软文，难出论文级干净答案。要规避，把"抓取"这一环交给你自己的干净源即可——给 `retrieve()` / `research()` 传入 `web_fetch=你的抓取函数`：它可以是已去噪的多引擎 `web_fetch`、学术源（arXiv / Semantic Scholar），或 Tavily / Exa / Perplexity 这类干净 API。库会改用你的抓取器，绕开默认中文 SERP 噪声。
- **抓取默认校验 TLS 证书**：`scrape` 默认开启证书校验（更安全）；仅在受信任内网 / 测试时可在 `config.json` 设 `scrape.tls_verify=false`（关闭会打印一次 MITM 风险提示）。公网环境务必保持开启。

---

## 怎么用

```bash
# 依赖（已验证 managed Python 3.13.12 venv）
PY=.../envs/default/Scripts/python.exe
$PY -m pip install trafilatura curl_cffi requests lxml markdownify

# 一句话检索
from orchestrate import retrieve
r = retrieve("TCP 和 UDP 的核心区别", {"max_sources": 3}, 6000)
print(r["findings"], r["sources"], r["tier_used"], r["confidence"])

# 用深度档位
r = retrieve("RAG 与长上下文怎么取舍", {"max_sources": 8}, 30000, depth="deep")

# 外部 docs 直进质量层（agent 用 web_fetch 抓好多引擎结果）
r2 = retrieve("TCP 和 UDP 的核心区别",
          docs=[{"url": "https://example.com/a", "text": "TCP 面向连接、可靠传输…"}])
```

论文 / 调研级编排：

```python
from research import research
out = research("TCP 和 UDP 的核心区别及原理", tier="L2")  # L2: 拆 5 维度, 单次 retrieve()
print(out["tier"], out["schema"], out["findings"], out["uncertainties"])
# tier="L3" 走多轮精炼; agent_fn= 注入子 agent 派发
```

返回结构：

| 字段 | 含义 |
|------|------|
| `findings` | 先答后源的合成结论 |
| `sources` | 去重后、按 SBA 加权截断的文档 |
| `scores` | 每个源的 SBA 打分明细 |
| `confidence` | 加权置信度 0–1 |
| `token_used` | 粗估 token 消耗 |
| `exhausted` | 是否因预算先到而**未**穷尽（禁止静默截断） |
| `tier_used` | 实际档位 L0/L1/L2/L3 |
| `uncertainties` | 顶层不确定项 `[{fact, reason}]` |

**真实返回样例**（`retrieve("TCP 和 UDP 的核心区别", {"max_sources": 3}, 6000)`，默认配置，已脱敏）：

```json
{
  "findings": "TCP 与 UDP 的核心区别在于连接性与可靠性：TCP 面向连接、提供可靠有序传输（确认/重传/流量控制），适合网页、文件、邮件；UDP 无连接、不可靠但延迟更低，适合实时音视频、游戏、DNS。两者均工作于传输层。",
  "sources": [
    {"url": "https://baike.baidu.com/item/TCP", "title": "TCP（传输控制协议）", "weighted": 0.82},
    {"url": "https://baike.baidu.com/item/UDP", "title": "UDP（用户数据报协议）", "weighted": 0.79}
  ],
  "scores": [
    {"url": "https://baike.baidu.com/item/TCP", "weighted": 0.82, "cred": 0.70, "rel": 0.90, "rec": 0.60, "auth": 0.80, "bias": 0.10}
  ],
  "confidence": 0.81,
  "token_used": 4210,
  "exhausted": false,
  "tier_used": "L1",
  "trace": {"stop_reason": "coverage met", "skipped": false}
}
```

> 语义 rerank（`config.rerank.enabled=true`）开启时，`sources` 额外带 `rerank_score` 键并按其排序；默认关时该键不存在，返回结构与上方一致。单源抓取失败会写入 `trace`/`meta.warnings`（见 SKILL.md FAQ），不会让检索崩溃。

完整可运行最小示例见 **`examples/quickstart.py`**（3 行出结果，含返回字段注释）。

---

## 被其它 skill 调用（检索原语）

Signal-Search 只返回带打分与置信度的干净结果，不替调用方决策。作为检索原语被 ChatGPT、Claude、Perplexity、Kimi、Gemini 等 AI 助手，以及各类投研、调研、深度分析工具消费——它们各自在自身领域强、做检索差。

**接入 LLM 的默认行为 = 调用方 LLM 自动接管**：在支持 LLM 注入的宿主环境（如 CodeBuddy 等 AI 助手）中被调用时，默认激活当前 LLM 充当 `agent_fn` / `tier_classify_fn` / `conflict_check_fn`，无需手写注入；未接入 LLM 时库内启发式降级，零依赖可跑。

全部对外参数与最小注入示例见技术附录 / `examples/`。

---

## 技术附录

### 模块地图（`scripts/`）

| 模块 | 职责 |
|------|------|
| `route.py` | 档位路由 + `/signal Lx` 覆盖 |
| `plan.py` | 意图分类 + 查询分解 |
| `connector.py` | 引擎选择（默认百度/搜狗）+ 失败隔离 + 兜底 |
| `search.py` / `deepfetch.py` | 拼 URL / 两跳取源（SERP→落地页，单线程池复用） |
| `scrape.py` | 反爬抓取：curl_cffi→系统 curl→requests 回落 + 退避 + 挑战页检测 + 分层 robots |
| `extract.py` | trafilatura 优先 + 正文抽取 + 蜜罐链接剔除 |
| `dedup.py` | simhash 分块 LSH 近似去重（O(n²)→O(n)） |
| `score.py` | SBA 五维加权打分 |
| `stop.py` / `budget.py` | 模式感知停止 / token 软预算 |
| `report.py` | 先答后源汇总 + 冲突标注 + 置信度 |
| `verify.py` | 引文校验 + 事实级核验（M51 关键词基线 + 可选语义） |
| `research.py` | 研究编排层（CC 53→12）：入口服别→分档→澄清/拆解/派 agent |
| `parallel.py` / `cache.py` / `embed.py` / `trace.py` | L3 并行 / 缓存 / 向量化 / 观测 |

### 默认开关政策

核心 / 护栏类默认开（路由、打分、停止、预算、验证 M51、分层 robots、合规）；实验类（SearXNG、语义核验、重排、动态画像等）默认关，需要时再翻。

`config.json` 硬门槛（任一为 `true` 即违反政策）：`cache.enabled` / `rerank.enabled` / `searxng.enabled` / `dynamic_profiling.enabled` / `conflict_typing.enabled` / `entity_resolution.enabled` / `observability.trace` / `result_driven_rewrite.enabled` 全部默认 `false`；唯一默认开的是 `compliance.enabled`（合规护栏）。

### 研究编排层 `research()`

在 `retrieve()` 质量层之上提供论文 / 调研级编排，借鉴 deep-research 对答案质量有用的机制、按本工具形态重映射（不整体搬其 5 命令工作流 / 不写 yaml / 不内置弹窗）。详见 `SKILL.md` 与 `references/`。

### 合规护栏（M55）

尊重 robots.txt（分层豁免 SERP、落地页严格守）、PII 脱敏不落库原文、限速、登录墙 / 付费墙跳过。详见 `references/anti-scraping.md`。

### 运行测试

```bash
$PY -m pytest tests/ -q
$PY -m scripts.eval        # 金标准档位命中率（离线）
```

---

## 项目结构

```text
Signal-Search/
├── SKILL.md            # CodeBuddy skill 入口：能力声明、档位路由、FAQ、限制汇总
├── README.md           # 本文件（定位、对比、用法、技术附录）
├── config.json         # 引擎与策略单真相源（URL 模板 / 档位 / 护栏默认开关）
├── LICENSE             # MIT
├── .gitignore
├── references/         # 详细设计文档（按需阅读，非必读）
│   ├── anti-scraping.md        # 反爬与合规护栏
│   ├── engines.md              # 引擎口径与 URL 模板
│   ├── eval-golden-set.md      # 金标准评测集
│   ├── intent-decomposition.md # 意图分解
│   ├── tier-policy.md          # 档位路由策略
│   └── token-optimization.md   # 省 token 七法
├── scripts/            # 全部实现（零依赖为主，重依赖默认关）
│   ├── orchestrate.py  # retrieve() 对外入口
│   ├── research.py     # 研究编排层（调研 / 学术）
│   ├── route.py / plan.py / connector.py / search.py / deepfetch.py
│   ├── scrape.py / extract.py / dedup.py / score.py
│   ├── stop.py / budget.py / report.py / verify.py / trace.py
│   └── ...（共 30 个模块，单一职责）
├── tests/              # pytest 单测（约 230 用例）+ conftest.py + fixtures/
└── examples/           # 可运行示例（quickstart.py 等）
```

## 许可证

[MIT](LICENSE) © 2026 Signal-Search contributors

本项目仅含开源代码与文档，不包含任何个人身份信息、密钥、令牌或设备标识。
