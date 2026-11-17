# 时空智能分析法 · 数据源说明

> 时空智能分析法的数据采集策略：4 层数据源 + 自动 fallback + 本地缓存。

---

## 一、数据源优先级

| 优先级 | 数据源 | 类型 | 适用场景 |
|--------|--------|------|---------|
| 🥇 | **academic-workflow**（已存在的 skill）| 学术文献（OpenAlex + Semantic Scholar + Crossref + arXiv + PubMed）| 纵向历史 + 横向学术对比 |
| 🥈 | **DuckDuckGo 免费搜索** | 通用网络 | 近期事件、新闻、用户口碑 |
| 🥉 | **GitHub（gh CLI）** | 代码库 + commit 频率 + issue | 技术路线 + 项目健康度 |
| 4 | **本地缓存**（7 天有效） | 历史查询 | 避免重复抓取 + 离线回退 |

---

## 二、academic-workflow skill 复用方式

### 已有的能力

`academic-workflow/scripts/research.py` 提供：

```python
from research import (
    search_openalex,       # OpenAlex（无需 API key，2亿+记录）
    search_semantic_scholar,  # Semantic Scholar（CS领域最全）
    search_crossref,       # Crossref（期刊元数据）
    search_arxiv,          # arXiv（预印本，PDF 可下载）
    search_pubmed,         # PubMed（生物医学方向）
)
```

### 时空智能分析法调用方式

```python
import sys
sys.path.insert(0, '/Users/neocross/.hermes/skills/openclaw-imports/academic-workflow/scripts')
from research import search_openalex, search_arxiv

# 纵向：拉时间线
results = search_openalex(
    'design thinking artificial general intelligence',
    start_date='2020-01-01',
    end_date='2026-09-06',
    sort='date',  # 按时间排序
    max_results=30
)

# 横向：拉竞品/替代方案的学术研究
results = search_arxiv('AI co-creation design thinking', max_results=10)
```

### 注意事项

- **OpenAlex 返回的数据字段有时为 None**（如 `publication_year`），需要 fallback 到 Semantic Scholar 补全
- **Semantic Scholar 无 key 时限速 1 req/s**——批量查询需 30+ 秒
- **arXiv 关键词要英文**——中文搜索质量差

---

## 三、DuckDuckGo 通用搜索（无需 API key）

```python
from duckduckgo_search import DDGS

def search_web(query: str, max_results: int = 10) -> List[dict]:
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", ""),
                "fetched_at": datetime.now().isoformat(),
            })
    return results
```

适用场景：
- 近期新闻（最近 30 天）
- 用户口碑（Reddit / 微博 / X）
- 公司新闻（官网 / 主流媒体）

---

## 四、GitHub 抓取（需 gh CLI）

```bash
gh search repos "X" --limit 10 \
  --json name,description,url,stargazersCount,createdAt
```

适用场景：
- 开源项目健康度（star 趋势、commit 频率）
- 技术路线分析（看 README / 源码）

---

## 五、本地缓存策略

**缓存位置**：`~/.hermes/spatiotemporal-cache/<md5(query)>.json`

**TTL**：7 天（自动失效）

**好处**：
- 避免重复抓取（学术 API 有速率限制）
- 离线回退（断网时仍可看历史数据）
- 跨会话复用

```python
import hashlib, json, time
from pathlib import Path

CACHE_DIR = Path('~/.hermes/spatiotemporal-cache').expanduser()

def cache_key(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()[:12]

def cache_get(query: str, max_age_days: int = 7):
    f = CACHE_DIR / f"{cache_key(query)}.json"
    if f.exists() and (time.time() - f.stat().st_mtime) / 86400 < max_age_days:
        return json.loads(f.read_text())
    return None

def cache_put(query: str, results: list):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    f = CACHE_DIR / f"{cache_key(query)}.json"
    f.write_text(json.dumps(results, ensure_ascii=False, indent=2))
```

---

## 六、数据可信度分级

| 来源 | 可信度 | 适用 |
|------|--------|------|
| OpenAlex / Semantic Scholar 论文 | ⭐⭐⭐⭐⭐ | 学术事实 |
| arXiv 预印本 | ⭐⭐⭐⭐ | 前沿观点（需注意未审稿）|
| 公司官网 / SEC / 政府公告 | ⭐⭐⭐⭐⭐ | 公司事实 |
| 主流媒体（NYT / Reuters / 36 氪）| ⭐⭐⭐⭐ | 公开事件 |
| 行业分析（IDC / Gartner）| ⭐⭐⭐⭐ | 趋势判断 |
| 自媒体 / 个人博客 | ⭐⭐ | 仅作辅助 |
| Reddit / X / 论坛 | ⭐⭐⭐ | 用户口碑（需多源验证）|

---

## 七、数据空白处理

**原则**：宁可显示「数据不足」，不可编造。

```
[场景]
找不到 X 在 2024 年的具体数据。

[错误处理]
不要写：「2024 年 X 大约是 Y」（编造）
要写：「数据不足，无法确认 2024 年 X 的具体值；建议从 [source A] / [source B] 进一步查询。」
```

---

## 八、抓取失败时的 fallback

| 失败源 | 降级方案 |
|--------|---------|
| OpenAlex 超时 | 换 Semantic Scholar |
| Semantic Scholar 超时 | 换 arXiv |
| arXiv 超时 | 换 DuckDuckGo |
| DuckDuckGo 超时 | 用本地缓存（即使过期）|
| 全部失败 | 报告「数据采集失败」，请求用户手动补充 |

---

## 九、中文源 / 院校官方源附录（2026-09-08 实证教训）

**问题**：当前 4 层数据源**主要覆盖英文 + 国际**。中国 / 院校官方 / 中文媒体的研究对象（如"国内数字媒体艺术 × AIGC 教育改革"）用 OpenAlex + arxiv + DuckDuckGo 命中率 < 30%。

**解决方案**：按场景分层加 4 类源。

### 9.1 中文搜索引擎

```python
# 百度（需注意排名商业化）
# 知乎搜索（中文社区深度内容）
# 微信搜一搜（公众号文章，需特殊 API 或 web scraping）
# 小红书搜索（年轻人关注的领域）
# 微博搜索（实时事件 + 大 V 评论）
```

**操作**：用 web_search + 限定 site: 或 限定中文关键词。

### 9.2 院校官方网站

中国高校官网通常更新慢（6-12 个月滞后），但**重要的课程改革、人事变动、会议报道都有**。

**已知有效源**（按领域）：

| 领域 | 主要院校 | 关键 URL 模式 |
|------|---------|------------|
| 美术 / 设计 | 中央美院、中国美院、广州美院、清华美院 | `cafa.edu.cn / caa.edu.cn / gzarts.edu.cn / tsinghua.edu.cn` |
| 综合大学 | 清华、同济、上交、北大、复旦 | `*.edu.cn` |
| 工科设计 | 同济、北航、东南、华南理工 | `*.edu.cn/design` |
| 高职 / 应用型 | 山东工艺美院、广州番禺职院 | `sdada.edu.cn / gzpyp.edu.cn` |

**操作**：直接 `web_search "中央美术学院 AIGC 课程改革 2025"` 或 `web_extract <官网URL>`。

### 9.3 学术中文学术库（v2.0.1 待补）

⚠️ **缺失源**（待 v2.1 加入）：
- **CNKI（中国知网）** — 中文期刊最全，但需订阅
- **万方数据** — 学位论文、会议论文
- **CSSCI（中文社会科学引文索引）** — 高质量中文期刊
- **维普** — 期刊检索

**临时方案**：用 web_search 限定 `site:cnki.net` 或 `site:wanfangdata.com`，或直接用 DuckDuckGo 搜中文关键词。

### 9.4 国际艺术设计院校对照（v2.0.1 待补）

⚠️ **缺失源**（待 v2.1 加入）：
- **RISD**（罗德岛设计学院）
- **Parsons**（帕森斯）
- **RCA**（皇家艺术学院）
- **MIT Media Lab**
- **Carnegie Mellon School of Design**

**临时方案**：用 web_search "Parsons design school AIGC curriculum 2025"。

### 9.5 实证记录（2026-09-08 数字媒体艺术研究）

| 数据缺口 | 实际影响 | 当前缓解 |
|---------|---------|---------|
| 中文 arxiv 结果少 | "数字媒体艺术+AIGC"在 arxiv 上只有 3-5 篇相关 | 用 web_search 中英文关键词 |
| 院校官网滞后 | 央美/国美最新课程改革只能查到 2025-04 之前的内容 | 接受数据滞后，明确标注时间 |
| 缺学生反馈数据 | 没有"学生对 AIGC 课程的真实评价" | 暂用第六届论坛报道作为间接源 |
| 缺国际比较 | 没有 RISD/Parsons 等的对比 | 暂用 arxiv 英文论文作为间接对照 |

### 9.6 改良路径（v2.1 待办）

1. 加 CNKI 搜索模块（需要订阅 key）
2. 加"院校官网批量抓取"脚本（domain 限定）
3. 加"微信公众号文章"抓取（需要专用工具）
4. 加"小红书 + 知乎"用户口碑抓取

---

## 十、跨 skill 数据源协作

| skill | 数据源能力 | 调用方式 |
|------|----------|---------|
| **arxiv** | 单 arxiv 检索 | `skill_view(name='arxiv')` |
| **blogwatcher** | RSS / 博客订阅监控 | 自动 cron |
| **competitor-news-monitor** | 竞品新闻监控 | 自动 cron |
| **grounded-citations** | 引用溯源 + 覆盖率审计 | 必调用 |
| **academic-workflow** | OpenAlex / S2 / Crossref / arXiv / PubMed | Python 模块 |
| **llm-wiki** | 长期知识库 | 自动 |
