# Web Crawl Skill - Usage Examples

## Basic Usage

### 1. Crawl Single URL

```python
# In Python
import asyncio
from web_crawl import crawl_url

result = asyncio.run(crawl_url(
    url="https://example.com",
    mode="markdown",
    max_length=10000
))
print(result)
```

### 2. Parallel Crawl Multiple URLs

```python
from web_crawl import parallel_crawl

urls = [
    "https://site1.com/article",
    "https://site2.com/guide",
    "https://site3.com/docs",
]

result = asyncio.run(parallel_crawl(
    urls=urls,
    mode="markdown",
    max_length=8000
))
print(result)
```

## Deep Research Workflow

### Step 1: Search for Sources

```python
web_search:0 {
  "query": "OpenManus-Max features comparison",
  "count": 8
}
```

### Step 2: Crawl Top Results

```python
exec:1 {
  "command": "cd ~/.openclaw/workspace-main/skills/web-crawl && python3 -c \"import asyncio; from web_crawl import parallel_crawl; print(asyncio.run(parallel_crawl(['https://url1.com', 'https://url2.com'], mode='markdown', max_length=8000)))\""
}
```

### Step 3: Analyze and Synthesize

Use the crawled content to:
- Extract key findings
- Compare sources
- Identify unique insights
- Cite sources

## Extraction Modes Explained

| Mode | Best For | Output Format |
|------|----------|---------------|
| `text` | Quick reading | Plain text |
| `markdown` | Content creation | Formatted Markdown |
| `links` | Discovery | List of links |
| `structured` | Data extraction | JSON metadata |
| `full` | Complete analysis | Markdown + Links |

## Advanced: CSS Selector Targeting

```python
# Extract only the article content
result = asyncio.run(crawl_url(
    url="https://example.com/page",
    mode="markdown",
    selector="article.main-content"  # CSS selector
))
```

## Research Templates

### Product Research

```python
# Research a product
queries = [
    "ProductName review 2024",
    "ProductName vs competitor",
    "ProductName pricing features",
]

# 1. Search each query
# 2. Crawl top 3 results per query
# 3. Synthesize pros/cons, pricing, features
```

### Company Research

```python
# Research a company
queries = [
    "CompanyName funding valuation",
    "CompanyName leadership team",
    "CompanyName recent news",
]

# 1. Search for company info
# 2. Crawl official site + news sources
# 3. Extract funding, team, products
```

### Technology Research

```python
# Research a technology
queries = [
    "TechnologyName documentation",
    "TechnologyName getting started",
    "TechnologyName github examples",
]

# 1. Search for docs and tutorials
# 2. Crawl official docs + GitHub
# 3. Extract key concepts and examples
```

## Integration with OpenClaw

When user asks for research:

1. **Understand intent**: What type of research? (product, company, tech, topic)
2. **Generate search queries**: Use research.py templates
3. **Execute search**: Use web_search tool
4. **Crawl sources**: Use web_crawl tool
5. **Synthesize**: Analyze and present findings

### Example Session

**User**: "研究一下 OpenManus-Max"

**Assistant**:
```
我来为你深度研究 OpenManus-Max。首先搜索相关信息...

[Use web_search for multiple queries]

找到以下关键来源：
1. GitHub 官方仓库
2. 技术博客分析
3. 社区讨论

现在抓取详细内容...

[Use parallel_crawl on top URLs]

## 研究发现

### 核心特性
- ...

### 架构设计
- ...

### 与 OpenManus 对比
- ...

### 优势与局限
- ...

---
来源：
- [1] GitHub: OpenDemon/OpenManus-Max
- [2] 技术博客分析
- [3] 社区讨论
```
