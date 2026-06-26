# 心理学文献检索助手

通过免费学术 API 快速检索心理学相关文献。

## 功能特性

### 🔍 多数据源检索
- **Semantic Scholar** - 覆盖广，含摘要
- **OpenAlex** - 开放获取信息全
- **CrossRef** - DOI 元数据权威

### 📄 完整文献信息
- 标题、作者、年份、期刊
- 被引次数、摘要、DOI、链接
- 开放获取标识

### 📝 引用格式化
- 自动生成 APA 引用格式

## 快速开始

```python
from literature_search import LiteratureSearch

searcher = LiteratureSearch(email="your_email@example.com")

# 检索文献
papers = searcher.search(
    query="social cognition attention",
    source="semantic_scholar",
    limit=10,
    year_from=2020
)

# 生成 APA 引用
for paper in papers:
    print(searcher.format_apa(paper))
```

## 系统要求

- Python 3.8+
- 无需额外依赖（仅用标准库）
- 需要网络连接

## 作者

@zhan599 - 华南师范大学应用心理学

## 许可证

MIT
