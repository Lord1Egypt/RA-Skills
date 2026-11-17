# 金标准 query 集（eval.py 输入 · M33 / M51 输入）

> 本文档是 `eval.py`（§5.14 / B1）的测试输入，也是 §13 **M33**（faithfulness/引文真实率/档位命中/token 比）与 **M51**（原子事实级 faithfulness）的对照基准。
> 共 24 条，L0–L3 均衡覆盖；每条含 `query` / `intent` / `expected_tier` / `budget` / `reference`（参考答案要点，用于 RACE 与原子事实判定）/ `checkpoints`（关键事实，供 M51 逐条蕴含校验）。
> **使用**：`eval.py` 对每条跑 `检索()`，比对 `reference` 算 faithfulness（含原子事实级）、比对 `expected_tier` 算档位命中、统计引文真实率与 token 比。

---

## L0 速查（4 条，expected_tier=L0，budget≈2000）

| id | query | intent | reference 要点 | checkpoints |
|----|-------|--------|---------------|-------------|
| G01 | 2026-08-07 是星期几 | fact | 星期五 | 星期=五 |
| G02 | Python 里怎么读一个文本文件 | howto | `open(path, 'r', encoding='utf-8').read()` | 用 open；指定 encoding |
| G03 | 珠穆朗玛峰海拔多少 | fact | 约 8848.86 米（2020 中尼公布） | 8848.86 米 |
| G04 | TCP 和 UDP 的核心区别 | compare | TCP 面向连接可靠、UDP 无连接不可靠 | TCP 可靠；UDP 不可靠 |

## L1 单点（6 条，expected_tier=L1，budget≈8000）

| id | query | intent | reference 要点 | checkpoints |
|----|-------|--------|---------------|-------------|
| G05 | 中国现行个人所得税起征点 | fact | 5000 元/月（2018 起） | 5000 元 |
| G06 | 比亚迪 2025 年新能源汽车销量 | fact | 约 427 万辆（官方年报口径） | 量级 400 万+；年份 2025 |
| G07 | 欧盟 GDPR 全称 | fact | General Data Protection Regulation | 全称含 General Data Protection |
| G08 | 谁发明了万维网 | fact | Tim Berners-Lee（1989/1991） | Tim Berners-Lee |
| G09 | 目前主流大模型上下文窗口最大的约多少 | latest | 2025–2026 多家达 100万–200万 token 级（如 Gemini 1.5/2 系列） | 百万 token 级 |
| G10 | MySQL 和 PostgreSQL 哪个支持 JSONB | fact | PostgreSQL 原生 JSONB；MySQL 为 JSON 类型 | PostgreSQL 有 JSONB |

## L2 诊断/方案（8 条，expected_tier=L2，budget≈30000）

| id | query | intent | reference 要点 | checkpoints |
|----|-------|--------|---------------|-------------|
| G11 | 对比 百度学术 与 Google Scholar 的文献覆盖 | compare | 中文文献百度学术更全；英文/引文 Scholar 更强；互补 | 两者差异；中文 vs 英文 |
| G12 | 自研小模型 vs 调用大模型 API 怎么选 | why | 看数据隐私/成本/可控性/迭代频率 | 隐私、成本、可控三维度 |
| G13 | 调研小微企业所得税优惠 | research | 小型微利企业减按 25% 计入、20% 税率（政策窗口） | 减按 25%；20% 税率 |
| G14 | 为什么推荐系统容易形成信息茧房 | why | 协同过滤正反馈闭环 + 指标短期化 | 正反馈闭环；指标短期化 |
| G15 | 对比 Redis 与 Memcached 作为缓存 | compare | Redis 支持 richer 数据结构/持久化；MC 纯 KV 更简单 | 数据结构差异；持久化差异 |
| G16 | 一个 5 人初创做 AI 产品如何控制云成本 | research | 预留实例/spot/按需混合；按用量停闲置；设预算告警 | 预留+spot；预算告警 |
| G17 | 上市公司回购股票对股价通常意味着什么 | why | 信号管理层认为低估；短期提振；长期看基本面 | 低估信号；短期提振 |
| G18 | 调研 RAG  vs 长上下文模型的取舍 | research | RAG 省 token/可溯源/需检索质量；长上下文免检索但贵且易噪 | 溯源 vs 成本；检索质量关键 |

## L3 研究（6 条，expected_tier=L3，budget≈100000）

| id | query | intent | reference 要点 | checkpoints |
|----|-------|--------|---------------|-------------|
| G19 | 调研 agentic search 前沿方案与开源实现 | research | CRAG/Search-R1/Self-RAG 等；开源如 GPT Researcher/Perplexica；趋势=检索-推理协同 | 列举≥2 方法；≥1 开源实现 |
| G20 | 系统调研 2025–2026 多智能体研究系统的架构范式 | research | orchestrator-worker（fan-out+merge）/ pipeline / hierarchical / competitive；多智能体相对单智能体 +90% 量级 | ≥3 范式；相对收益数据 |
| G21 | 中国市场 AIGC 监管政策全景调研 | research | 生成式 AI 服务管理暂行办法（2023-08 实施）+ 系列配套；备案/标识/内容责任 | 2023-08 办法；备案要求 |
| G22 | 深度调研向量数据库选型（Milvus/Weaviate/Qdrant/PGVector） | research | Milvus 规模首选；Weaviate 语义/模块化；Qdrant 轻量 Rust；PGVector 复用 PG | ≥3 库差异；各自定位 |
| G23 | 调研近三年检索增强生成在医疗领域的落地与风险 | research | 文献检索/问诊辅助落地；幻觉与责任风险；需 human-in-loop | 落地场景；风险点 |
| G24 | 系统调研苹果产业链在中国大陆的主要上市公司分布 | research | 立讯精密/歌尔股份/蓝思科技等；环节=组装/声学/结构件；集中度与地缘风险 | ≥3 公司；环节映射 |

---

## 评分细则（eval.py 产出 4 指标，见 §5.14 / M33）

1. **faithfulness（含原子事实级，M51）**：`findings` 拆原子事实 → 逐条与 `sources` 片段蕴含判定 → TRUE/FALSE/UNCERTAIN；UNCERTAIN 标"待核实"不计入已支持。faithfulness = 支持事实 / 全部事实。
2. **引文真实率**：findings 中每个 URL ∈ sources 抓取集；未抓取一律剔除/标待核实。目标 ≥95%（M33-A14.2）。
3. **档位命中率**：`tier_used == expected_tier`。目标 ≥90%（M33-A14.3）。
4. **token 实际/预算比**：健康 0.6–1.0（M33-A14.4）；<0.3 过度保守，>1 预算失准。

> 每条 `checkpoints` 为 M51 原子事实判定锚点：eval 时抽取 findings 中对应事实，与 source 片段做蕴含校验；任一 checkpoint 被判定 FALSE/UNCERTAIN 且无"待核实"标注 = faithfulness 扣分。
> 金标准集每迭代周期重跑（覆盖 drift / 回归）；新增 query 须同时补 `reference` + `checkpoints`，否则不入库。
