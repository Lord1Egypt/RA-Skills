# Commands Reference — 完整参数说明

## search.py 主入口

### 通用搜索

```bash
python3 scripts/search.py --query "关键词" [选项]
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `--query`, `-q` | str | (必填) | 搜索关键词，中文自动路由百度学术，英文全源并发 |
| `--source`, `-s` | str | `all` | 数据源：`arxiv`, `semantic_scholar`, `pubmed`, `crossref`, `baidu_scholar`（逗号分隔），或 `all` |
| `--max`, `-n` | int | `10` | 最大返回条数 |
| `--year-from` | int | 无 | 起始年份（含） |
| `--year-to` | int | 无 | 截止年份（含） |

中文搜索示例：

```bash
# 中文关键词自动路由百度学术
python3 scripts/search.py -q "深度学习 图像识别"

# 指定只用百度学术
python3 scripts/search.py -q "自然语言处理 预训练模型" -s baidu_scholar -n 10
```

英文搜索示例：

```bash
# 全源搜索 NLP 论文，近 3 年
python3 scripts/search.py -q "natural language processing" --year-from 2023 -n 15

# 只在 arXiv 搜索
python3 scripts/search.py -q "diffusion model" --source arxiv

# PubMed 搜医学
python3 scripts/search.py -q "cancer immunotherapy checkpoint" --source pubmed -n 20
```

### 百度学术配置

百度学术通过百度千帆平台 API 接入，需设置环境变量：

```bash
export BAIDU_QIANFAN_API_KEY="bce-v3/ALTAK-xxx"
```

获取方式：https://console.bce.baidu.com/qianfan/ais/console/apiKey

未配置时，百度学术源自动跳过，不影响其他源。

### DOI 查询

```bash
python3 scripts/search.py --doi "DOI"
python3 scripts/search.py --doi "DOI" --bibtex
```

| 参数 | 说明 |
|---|---|
| `--doi` | 要查询的 DOI（以 10. 开头） |
| `--bibtex` | 同时输出 BibTeX 格式引用 |

### 引用追踪

```bash
python3 scripts/search.py --citations "paper_id" [--max N]
python3 scripts/search.py --references "paper_id" [--max N]
```

paper_id 为 Semantic Scholar 的 40 位哈希 ID，需从搜索结果中获取。

### 作者检索

```bash
python3 scripts/search.py --author "作者名" [--max N]
```

---

## 各数据源 API 模块

### arxiv_api.py
```python
from arxiv_api import search
results = search("transformer", max_results=10)
```

### semantic_scholar_api.py
```python
from semantic_scholar_api import search, get_citations, search_author
```

### pubmed_api.py
```python
from pubmed_api import search
results = search("cancer immunotherapy", max_results=10, year_from=2023)
```

### crossref_api.py
```python
from crossref_api import get_by_doi, get_bibtex
paper = get_by_doi("10.1038/nature14539")
bib = get_bibtex("10.1038/nature14539")
```

### baidu_scholar_api.py
```python
from baidu_scholar_api import search
results = search("深度学习", max_results=10, enable_ai_abstract=True)
```

环境变量：`BAIDU_QIANFAN_API_KEY`（必填，否则返回空列表）

---

## 输出格式

所有命令输出 JSON（`--bibtex` 除外）。

成功时：
```json
{"query": "...", "sources": [...], "count": N, "results": [...]}
```

百度学术结果额外包含 AI 智能摘要（`aiAbstract`）。
