# OpenAlex API 使用说明

OpenAlex 是一个免费的学术文献数据库，包含超过 2.5 亿篇论文。

## 基本信息

- **API 地址**: `https://api.openalex.org`
- **认证**: 可选（提供 email 可提高限额）
- **限制**: 免费用户每秒 10 次请求

## 常用查询

### 按关键词搜索

```python
import requests

url = "https://api.openalex.org/works"
params = {
    "search": "thermoelectric",
    "sort": "cited_by_count:desc",
    "per_page": 10
}

response = requests.get(url, params=params)
data = response.json()

for work in data["results"]:
    print(work["title"], work["cited_by_count"])
```

### 按日期筛选

```python
params = {
    "search": "heat pipe",
    "filter": "from_publication_date:2026-01-01",
    "sort": "publication_date:desc"
}
```

### 按概念筛选

```python
# 热电材料概念 ID
params = {
    "filter": "concepts.id:C2778405530",
    "sort": "publication_date:desc"
}
```

## 返回字段

| 字段 | 说明 |
|------|------|
| `id` | 论文唯一标识 |
| `title` | 标题 |
| `doi` | DOI |
| `publication_date` | 发布日期 |
| `cited_by_count` | 被引次数 |
| `authors` | 作者列表 |
| `primary_location.source.display_name` | 期刊名 |
| `abstract` | 摘要 |

## 提高限额

提供 email 作为 User-Agent：

```python
headers = {
    "User-Agent": "mailto:your@email.com"
}
response = requests.get(url, headers=headers)
```

## 最佳实践

1. **缓存结果**：避免重复请求相同数据
2. **分页获取**：使用 `page` 参数分页
3. **精简字段**：使用 `select` 参数只获取需要的字段

```python
params = {
    "search": "thermoelectric",
    "select": "id,title,doi,publication_date,cited_by_count",
    "per_page": 50
}
```

---

# arXiv API 使用说明

arXiv 是预印本论文库，主要覆盖物理、计算机科学、数学等领域。

## 基本信息

- **API 地址**: `http://export.arxiv.org/api/query`
- **认证**: 无需
- **限制**: 每次请求间隔 3 秒

## 常用查询

### 按关键词搜索

```python
import feedparser

query = "all:machine learning"
url = f"http://export.arxiv.org/api/query?search_query={query}&start=0&max_results=10"

feed = feedparser.parse(url)
for entry in feed.entries:
    print(entry.title, entry.published)
```

### 按分类筛选

```python
# cs.LG = 机器学习
query = "cat:cs.LG"
```

### 按日期排序

```python
url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending"
```

## 返回字段

| 字段 | 说明 |
|------|------|
| `entry.id` | 论文 ID |
| `entry.title` | 标题 |
| `entry.summary` | 摘要 |
| `entry.published` | 发布日期 |
| `entry.authors` | 作者列表 |
| `entry.link` | PDF 链接 |

## 最佳实践

1. **使用 feedparser**：解析 XML 更方便
2. **控制频率**：每次请求后等待 3 秒
3. **限制结果数**：建议每次不超过 100 条
