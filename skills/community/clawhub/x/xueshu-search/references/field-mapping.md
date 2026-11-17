# Field Mapping — 返回字段详解

所有数据源的结果经过 `normalize_result()` 统一为以下字段。

## 统一字段

| 字段 | 类型 | 说明 | 可能为空？ |
|---|---|---|---|
| `source` | str | 数据来源：`arxiv` / `semantic_scholar` / `pubmed` / `crossref` / `baidu_scholar` | 否 |
| `id` | str | 源内唯一标识：arXiv ID / S2 paper ID / PMID / DOI | 否 |
| `title` | str | 论文标题 | 可能 |
| `authors` | list[dict] | 作者列表，每项 `{"name": "..."}` （S2 还有 `authorId`） | 可能 |
| `abstract` | str | 摘要（PubMed 默认不返回 abstract，需额外请求） | 可能 |
| `year` | int\|null | 发表年份 | 可能 |
| `published` | str | 发表日期字符串（格式因源而异） | 可能 |
| `doi` | str | DOI 标识符 | 可能 |
| `url` | str | 论文在线地址 | 可能 |
| `pdf_url` | str | PDF 直链（arXiv 提供，S2 仅 OpenAccess 论文） | 可能 |
| `citation_count` | int\|null | 被引次数（仅 S2 和 CrossRef 提供） | 可能 |
| `venue` | str | 发表场所（期刊/会议名） | 可能 |
| `categories` | list[str] | 学科分类标签（仅 arXiv） | 可能 |

## 各源特有字段（不在统一输出中）

### arXiv: `arxiv_api.py` 原始返回额外字段

- `arxiv_id`: arXiv 标识符（如 `1706.03762`）
- `updated`: 最后更新日期
- `categories`: arXiv 分类（如 `cs.CL`, `stat.ML`）

### Semantic Scholar: `semantic_scholar_api.py` 原始返回额外字段

- `paperId`: 40 位 S2 paper ID（即统一字段的 `id`）
- `externalIds`: 外部 ID 集合（DOI, ArXiv, MAG, PMID 等）
- `openAccessPdf`: OA PDF 信息（url, status）
- `publicationVenue`: 发表场所详情（含 type）
- `journal`: 期刊信息（name, volume, pages）

### PubMed: `pubmed_api.py` 原始返回额外字段

- `source_journal`: 来源期刊名
- `pub_types`: 发表类型列表（如 `["Journal Article", "Review"]`）

### CrossRef: `crossref_api.py` 原始返回额外字段

- `container`: 容器（期刊/会议/书籍名）
- `publisher`: 出版商
- `type`: 作品类型（`journal-article`, `book`, `proceedings-article` 等）
- `is-referenced-by-count`: 被引次数（即统一字段的 `citation_count`）

### 百度学术: `baidu_scholar_api.py` 原始返回额外字段

- `aiAbstract`: AI 智能生成的论文摘要（需 `enable_ai_abstract=true`，默认开启）
- `keyword`: 检索关键词
- `publishInfo`: 发布信息（`journalName` 等）
- 不返回作者列表和引用次数

## 去重逻辑

`deduplicate()` 函数分两级去重：

1. **DOI 去重（优先级最高）**：相同 DOI → 保留 `_score_richness()` 最高的版本
2. **标题去重**：无 DOI 或 DOI 不同但标题完全相同（小写、去尾部句号）→ 保留信息最丰富的版本

`_score_richness()` 评分规则：
- 有 abstract：+3
- 有 DOI：+2
- 每个作者：+1（最多 +5）
- 有 citation_count：+1
- 有 pdf_url：+1

## 排序逻辑

`rank()` 排序优先级：
1. 被引次数降序（citation_count desc）
2. 发表年份降序（year desc）

## 使用建议

向用户展示结果时：
- **优先展示 citation_count 高的**（领域影响力指标）
- **标注来源**（arXiv = 预印本，PubMed = 生物医学，S2 = 综合）
- **对缺失字段友好**（如 PubMed 无 abstract 时可以提示用户点击 url 查看）
- **DOI 是金标准**（有 DOI 的论文更可信）
