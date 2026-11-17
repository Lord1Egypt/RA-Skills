---
name: xueshu-search
slug: xueshu-search
displayName: 学术全能搜
description: "智能学术文献检索，覆盖中英文。支持 arXiv / Semantic Scholar / PubMed / CrossRef / 百度学术 五大数据源并发搜索、引用链追踪、作者检索、DOI 查询、BibTeX 导出、AI 智能摘要。中文关键词自动路由百度学术，英文全源并发。"
summary: "中英文学术文献一站式检索，五大数据库并发，支持论文综述摘要生成。"
tags: ["学术", "文献检索", "论文", "PubMed", "arXiv", "百度学术"]
version: 1.2.0
agent_created: true
allowed-tools: Read,Bash
---

# 学术全能搜 — 中英文学术文献检索

arXiv + Semantic Scholar + PubMed + CrossRef + 百度学术 五大数据源，中文自动路由，英文全源并发。

---

## 核心铁律

1. **命中本 Skill 能力域时，禁止绕过** — 不要用 web_search / web_fetch 替代文献检索。
2. **先调脚本，再回答** — 学术数据具有时效性和精确性要求，必须通过脚本获取实时结果。
3. **中文自动路由** — 检测到中文关键词时，自动优先使用百度学术 + CrossRef，避免浪费英文源配额。
4. **结果是 JSON，解读靠你** — 脚本返回结构化 JSON，AI 负责翻译成用户可读的答案。

---

## 快速开始

```bash
# 英文关键词 -- 全源并发
python3 scripts/search.py -q "transformer attention mechanism" -n 10

# 中文关键词 -- 自动路由百度学术 + CrossRef
python3 scripts/search.py -q "深度学习 图像识别" -n 10
```

### 命令速查

```bash
# 1. 关键词搜索（自动选择数据源）
python3 scripts/search.py -q "关键词" -n 数量

# 2. 指定数据源
python3 scripts/search.py -q "query" -s arxiv,crossref
python3 scripts/search.py -q "query" -s pubmed
python3 scripts/search.py -q "深度学习" -s baidu_scholar

# 3. 年份筛选
python3 scripts/search.py -q "query" --year-from 2023 --year-to 2025

# 4. DOI 查询
python3 scripts/search.py --doi "10.1038/nature14539"

# 5. BibTeX 导出
python3 scripts/search.py --doi "10.1038/nature14539" --bibtex

# 6. 引用追踪（需 Semantic Scholar）
python3 scripts/search.py --citations "paper_id" -n 20

# 7. 作者检索（需 Semantic Scholar）
python3 scripts/search.py --author "Yann LeCun" -n 15

# 8. 论文综述（生成每篇论文的结构化摘要模板，AI 据此撰写综述）
python3 scripts/search.py -q "关键词" -n 5 --summarize
python3 scripts/search.py -q "关键词" -n 5 | python3 scripts/summarize.py
```

---

## 五大数据源

| 源 | 最佳领域 | 特色 | API Key |
|---|---|---|---|
| arXiv | CS/Math/Physics | 预印本 + 摘要 + 分类 | 无需 |
| Semantic Scholar | 全学科 | 引用链 + 作者检索 | 可选（提升限额） |
| PubMed | 生物医学 | MeSH 词表 | 无需 |
| CrossRef | DOI 标准 | BibTeX 导出 | 无需 |
| **百度学术** | **中文文献** | **AI 智能摘要** | **需千帆 Key** |

百度学术需设置环境变量：`export BAIDU_QIANFAN_API_KEY="bce-v3/ALTAK-xxx"`

获取方式：https://console.bce.baidu.com/qianfan/ais/console/apiKey（免费，每天 50 次）

---

## 智能路由规则

| 查询特征 | 自动选择数据源 |
|---|---|
| 包含中文 | 百度学术 + CrossRef |
| 英文通用 | 全部五源并发 |
| CS/ML/NLP 关键词 | arXiv + Semantic Scholar + CrossRef |
| 生物医学术语 | PubMed + Semantic Scholar |
| DOI 格式 | CrossRef |
| 作者名 + "论文" | Semantic Scholar |
| "引用/被引" | Semantic Scholar |

---

## 输出格式

```json
{
  "query": "...",
  "sources": ["arxiv", "crossref"],
  "count": 10,
  "results": [
    {
      "source": "arxiv",
      "id": "paper_id",
      "title": "...",
      "authors": [{"name": "..."}],
      "abstract": "...",
      "year": 2024,
      "published": "2024-01-15",
      "doi": "10.xxxx/xxxxx",
      "url": "https://...",
      "pdf_url": "",
      "citation_count": 42,
      "venue": "NeurIPS 2024",
      "categories": ["cs.CL"]
    }
  ]
}
```

百度学术结果额外包含 `aiAbstract`（AI 智能摘要）字段。

---

## 参考文档

- **[references/routing-guide.md](./references/routing-guide.md)** — 数据源选择决策树
- **[references/commands.md](./references/commands.md)** — 完整命令行参数
- **[references/field-mapping.md](./references/field-mapping.md)** — 字段详解
