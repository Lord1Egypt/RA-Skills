# RSS-Brew 新功能架构设计：HN/Reddit 多源接入 + Phase B 前 Enrichment

作者：Chongzhi（架构设计）  
日期：2026-03-21  
原则：**现有稳定 pipeline 不改语义、不改默认行为；全部新增能力均为可选 additive path。**

---

## 0. 现状基线（从代码确认）

已确认当前主链路：
- 入口：`scripts/run_pipeline_v2.py`
- Fetch：`scripts/core_pipeline.py`
  - 仅消费 `sources.yaml` 中 RSS source（`name/url/deepset_eligible`）
  - URL canonicalize + `processed-index.json`（hash(url)）去重
  - 输出 `new-articles.json`
- Phase A：`scripts/phase_a_score.py`
  - 输入 `new-articles.json`，输出 `scored-articles.json`
- Phase B：`scripts/phase_b_analyze.py`
  - 从 `summary/text` 生成分类、双语摘要、deep_analysis
- state/manifest：run 级 staged→committed 已稳定

结论：要满足“100%不影响生产路径”，必须做到：
1. 默认 flag 全关（行为与今天完全一致）；
2. 新字段仅追加，不替换旧字段；
3. dedup 仍走同一 `processed-index.json`。

---

## 1) 功能1：多源接入（HN + Reddit）

## 1.1 目标
在不破坏 RSS 获取逻辑的前提下，新增可选采集源：
- Hacker News（top stories）
- Reddit（指定 subreddit JSON）

输出统一为与现有 `new-articles.json` 兼容的 article schema：
- 必须保留：`source/source_url/title/url/published/summary/text`
- 可追加：`origin_type`、`external_id` 等扩展字段

## 1.2 新增文件设计

### A. `scripts/source_hn.py`
职责：拉取 HN top stories 并标准化为 article list。

建议接口：
```python
def fetch_hn_articles(limit: int, lookback_hours: int, timeout: float) -> list[dict]:
    ...
```

输入来源：
- `https://hacker.news/v0/topstories.json`
- `https://hacker.news/v0/item/<id>.json`

输出单条 article（兼容现有 schema）：
```json
{
  "source": "Hacker News",
  "source_url": "https://hacker.news/",
  "title": "...",
  "url": "https://...", 
  "published": "2026-03-21T07:10:00+00:00",
  "summary": "HN score: 182 | comments: 74 | by: username",
  "text": "HN context + linked page snippet fallback",
  "origin_type": "hn",
  "external_id": "hn:12345678"
}
```

实现要点：
- 若 item 无 `url`（Ask HN）可降级到 `https://news.ycombinator.com/item?id=<id>`。
- `text` 优先用 linked URL 做 trafilatura；失败则用 HN title + metadata 兜底，避免空文本。

### B. `scripts/source_reddit.py`
职责：拉取 subreddit JSON 并标准化。

建议接口：
```python
def fetch_reddit_articles(subreddits: list[str], per_subreddit: int, lookback_hours: int, timeout: float) -> list[dict]:
    ...
```

使用 endpoint：
- `https://www.reddit.com/r/{subreddit}/hot.json?limit={n}`（或 top/new，配置化）
- Header 设置 UA，避免 429

输出单条 article：
```json
{
  "source": "Reddit:r/MachineLearning",
  "source_url": "https://www.reddit.com/r/MachineLearning/",
  "title": "...",
  "url": "https://...", 
  "published": "2026-03-21T06:50:00+00:00",
  "summary": "Reddit score: 540 | comments: 91 | author: ...",
  "text": "post selftext or linked page snippet",
  "origin_type": "reddit",
  "external_id": "reddit:t3_abcd12"
}
```

实现要点：
- `url` 统一转绝对 URL（reddit 相对链接要补全）。
- `text` 优先 selftext，若为空则抓外链正文（复用 `extract_text` 逻辑）。

### C. `scripts/source_registry.py`
职责：统一调度多源 connector，返回标准 article 列表。

建议接口：
```python
def fetch_non_rss_articles(config: dict, hours: int) -> list[dict]:
    # fan-out hn/reddit fetchers; normalize schema
```

---

## 1.3 集成点设计（最小侵入）

### 方案：在 `core_pipeline.py` 内新增“可选非RSS分支”
保持现有 RSS for-loop 不动，仅追加：
1. 新增 `--enable-hn` / `--enable-reddit` / `--social-config`
2. RSS抓取完成后，调用 `source_registry.fetch_non_rss_articles(...)`
3. 对返回结果复用同一套流程：
   - `canonicalize_url` -> `hash_url`
   - `processed-index` 去重
   - `normalize_title` 标题去重
   - 写入同一 `new_articles`

这样的好处：
- dedup 与 metadata 完全共享，不新增状态文件；
- run-stats 可以直接扩展 `by_source` 统计，不改主结构。

---

## 1.4 `sources.yaml` 扩展（向后兼容）

当前 `SourcesConfig` 只接受 `sources: [{name,url,deepset_eligible}]`。建议扩展为：

```yaml
sources:
  - name: "TechCrunch"
    url: "https://techcrunch.com/feed/"

extra_sources:
  hn:
    enabled: false
    limit: 30
    lookback_hours: 48
  reddit:
    enabled: false
    mode: "hot"
    per_subreddit: 20
    subreddits:
      - "venturecapital"
      - "startups"
      - "MachineLearning"
      - "technology"
    lookback_hours: 48
```

兼容策略：
- `extra_sources` 缺失时默认禁用；
- `load_sources()` 保持原返回不变；另加 `load_extra_sources()`；
- 不触碰老 `sources` 字段语义。

---

## 1.5 去重方案（共享 processed-index）

继续使用现有规则：
- 统一 canonical URL
- `url_hash = sha256(canonical_url)`
- `processed-index.json[url_hash] = canonical_url`

新增补强（可选，不影响旧行为）：
- 对 HN/Reddit 补写 metadata：
  - `metadata[url_hash].origin_type`
  - `metadata[url_hash].external_id`
- 若 external URL 缺失（如纯社区帖），使用稳定 canonical permalink（HN item 链接 / Reddit comments 链接），确保可 dedup。

---

## 2) 功能2：Content Enrichment（Phase B 前 web context）

## 2.1 目标
对 Phase A 高分文章（`score >= 4`）在进入 Phase B 前做背景检索补全，生成 `enrichment.web_context` 供 Phase B prompt 使用。

## 2.2 新增文件设计

### A. `scripts/phase_enrich_context.py`
职责：读取 `scored-articles.json`，仅处理高分文章，调用 Tavily，写回增强版 scored 输出。

建议 CLI：
```bash
python3 scripts/phase_enrich_context.py \
  --input staged/scored-articles.json \
  --output staged/scored-articles.enriched.json \
  --min-score 4 \
  --max-results 5 \
  --max-snippets 3 \
  --timeout 20
```

建议内部接口：
```python
def enrich_articles(payload: dict, min_score: int, tavily_cfg: dict) -> dict:
    ...
```

### B. `scripts/tavily_client.py`
职责：轻量 Tavily client 封装（避免把 phase 脚本写得过重）。

参考：
- `/root/.openclaw/workspace/skills/openclaw-tavily-search/scripts/tavily_search.py`

实现要求：
- 读取 `TAVILY_API_KEY`（`~/.openclaw/.env`）
- 简单重试 + rate limit 退避

---

## 2.3 enrichment 字段 schema（追加字段，不改旧字段）

给每篇高分 article 增加：

```json
"enrichment": {
  "status": "ok|skipped|error",
  "provider": "tavily",
  "query": "...",
  "fetched_at": "2026-03-21T08:30:00+00:00",
  "web_context": [
    {
      "title": "...",
      "url": "https://...",
      "snippet": "...",
      "source": "web"
    }
  ],
  "error": "...optional..."
}
```

规则：
- 低分（<4）可不带 enrichment，或 `status=skipped`。
- 查询失败不应中断主 pipeline：写 `status=error` 并继续。

---

## 2.4 集成点设计（run_pipeline_v2）

在 `phase_a_score.py` 之后、`phase_b_analyze.py` 之前插入可选阶段：

1. 现状：`staged_scored` -> `phase_b`
2. 新流程（flag on）：
   - `phase_enrich_context.py` 输入 `staged_scored`
   - 输出 `staged_scored_enriched`
   - `phase_b` 改用 enriched 输入

建议新增变量：
- `staged_scored_enriched = staging_dir / "scored-articles.enriched.json"`

若 feature 关闭或 enrich 失败：
- 回退输入为 `staged_scored`，确保与现有一致。

---

## 2.5 Phase B prompt 最小改动

在 `phase_b_analyze.py::analyze_one()` 里追加一段可选上下文，不改 JSON 输出协议。

当前 prompt 仅含 `Content:`。新增：
```text
Web Context (optional, external references):
- [title] snippet (url)
...
Use this only as supporting context; prioritize original article content.
```

关键点：
- 不改 `SYSTEM` 输出 JSON 契约；
- 不新增必填字段；
- 仅当 `enrichment.web_context` 存在时拼接。

---

## 3) 集成安全策略（feature flags/env vars/dry-run）

## 3.1 Feature Flags（默认全关）

在 `run_pipeline_v2.py` 新增 CLI 参数：
- `--enable-hn`
- `--enable-reddit`
- `--enable-enrichment`

对应环境变量兜底：
- `RSS_BREW_ENABLE_HN=0|1`
- `RSS_BREW_ENABLE_REDDIT=0|1`
- `RSS_BREW_ENABLE_ENRICHMENT=0|1`

优先级：CLI > ENV > 默认 false。

## 3.2 错误隔离

- HN/Reddit 拉取失败：记录 warning + run_stats，不让 core pipeline fail（除非显式 strict mode）。
- Tavily 失败：article 级 `status=error`，不阻断 Phase B。

可新增 strict 开关（默认 false）：
- `RSS_BREW_EXTRA_SOURCES_STRICT=0|1`
- `RSS_BREW_ENRICH_STRICT=0|1`

## 3.3 Dry-run 支持

- 当 orchestrator `--mock` 打开时：
  - enrichment phase 进入 mock 模式（不调用 Tavily，构造 deterministic fake snippets）
  - HN/Reddit 可允许真实抓取（可配置）或 mock payload

新增参数：
- `phase_enrich_context.py --mock`
- `core_pipeline.py --mock-extra-sources`（可选）

---

## 4) 实现优先级与工作拆分

## P0（低风险基础，先落地）
1. `phase_enrich_context.py` + `tavily_client.py`（独立阶段，易回滚）
2. `phase_b_analyze.py` prompt 微改，读取 enrichment（可空）
3. `run_pipeline_v2.py` 增加 `--enable-enrichment` 编排分支

验收：
- 默认无 flag 时产物 byte-level 行为近似不变（允许时间戳变化）
- 开启 enrichment 时 `scored-articles.enriched.json` 正确生成

## P1（多源接入）
1. `source_hn.py`、`source_reddit.py`、`source_registry.py`
2. `core_pipeline.py` 添加可选 extra-source 分支
3. `sources.yaml` 支持 `extra_sources` 扩展解析

验收：
- `processed-index.json` hash 逻辑不变
- `new-articles.json` schema 对下游兼容

## P2（可观测性和稳定性）
1. run-stats 增加：`hn_fetched/reddit_fetched/enriched_ok/enriched_error`
2. retry/backoff + 429 handling
3. 小规模灰度：先 `--enable-enrichment`，后 `--enable-hn`，最后 `--enable-reddit`

---

## 5) 回滚与发布策略

- 所有新能力都可通过 flag 立即关闭，回到旧路径；
- 不修改已有产物关键文件名（新增仅 added file）；
- 先在 `python3 -m rss_brew.cli dry-run --debug` 灰度验证，再进入 cron。

推荐上线顺序：
1. 上 enrichment（默认 off）
2. 验证后开 enrichment
3. 上 HN connector（默认 off）
4. 上 Reddit connector（默认 off）

---

## 6) 关键接口草图（便于工程落地）

### core_pipeline 新参数（建议）
```bash
--enable-hn
--enable-reddit
--social-config /path/to/sources.yaml
--extra-source-timeout 12
```

### orchestrator 新参数（建议）
```bash
--enable-enrichment
--enrichment-min-score 4
--enrichment-max-results 5
```

### phase_enrich_context 输出文件
- `scored-articles.enriched.json`（新增）
- 保持 `scored-articles.json` 原有语义

---

## 7) 最终架构决策（摘要）

1. **不改主干默认行为**：所有新功能默认关闭，保障现有 cron/生产 100% 无感。
2. **多源并入 core fetch，但走同一 dedup index**：HN/Reddit 结果统一 canonicalize+hash，与 RSS 共用 `processed-index.json`。
3. **Enrichment 作为独立可选 phase 插入 A→B 之间**：失败降级不阻断，产物追加 `enrichment.web_context`。
4. **Phase B 仅做 prompt 级最小改动**：利用 enrichment 作为辅助背景，不改变输出 JSON 契约。
5. **工程实施按 P0→P1→P2 分阶段灰度**：先 enrichment 再多源，逐步开关，始终可一键回滚。