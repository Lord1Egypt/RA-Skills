---
name: web-data-extractor
description: 网页数据采集器，支持 CSS 选择器/XPath 提取、批量抓取、自动分页、数据导出（CSV/JSON/Markdown）。
metadata:
  openclaw:
    requires:
      bins:
        - web_fetch
        - read
        - write
---

# 网页数据采集器 v1.0.0

从网页批量提取结构化数据，支持多种选择器和导出格式。

## 功能特性

### 1. CSS 选择器提取
```javascript
// 提取所有标题
web_fetch({"url": "https://example.com"})
// 使用 CSS 选择器提取特定元素
```

### 2. XPath 提取
```javascript
// 支持 XPath 路径提取复杂结构
```

### 3. 批量抓取
- 自动分页处理
- URL 列表批量处理
- 并发控制

### 4. 数据导出
- CSV 格式
- JSON 格式
- Markdown 表格

## 快速使用示例

```javascript
// 提取文章列表
const articles = extractData({
  url: "https://blog.example.com",
  selector: ".article-card",
  fields: {
    title: "h2.title",
    link: "a[href]",
    date: ".publish-date"
  }
})

// 导出为 CSV
exportToCSV(articles, "output.csv")

// 导出为 JSON
exportToJSON(articles, "output.json")

// 批量抓取多页
const allData = scrapeMultiple({
  baseUrl: "https://example.com/page/",
  pages: 10,
  selector: ".item"
})
```

## 使用场景

1. **市场调研** - 抓取竞品价格、产品信息
2. **内容聚合** - 收集多源内容
3. **数据分析** - 提取公开数据集
4. **舆情监控** - 追踪 mentions、评论
5. **SEO 分析** - 抓取关键词排名

## 注意事项

- 遵守目标网站的 robots.txt
- 控制抓取频率，避免被封
- 仅抓取公开数据

## 定制开发

需要定制化数据采集、清洗或自动化工作流？

📧 联系：careytian-ai@github

---

## 许可证

MIT-0
