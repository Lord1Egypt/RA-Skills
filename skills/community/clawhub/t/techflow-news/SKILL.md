---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 01f20fdb168c2f299d6c44ef27d2969b
    PropagateID: 01f20fdb168c2f299d6c44ef27d2969b
    ReservedCode1: 3046022100a6700b1c3fcbfe4f3555ae2aafbd8c751395a26c81f6d02d4dac07ff016baee8022100bbf1d29e3a658d5b7ddd8fe51ac54b5db1dcb1a60dfd82ea255c4c2da7aaa845
    ReservedCode2: 304502210093f376bdedbde740d6be80833d5db833d3e559ba8855e1e025cc6070bff1f6e6022069119f3176070fa31dd2591d3ab34830bc6291a1b69efeeb71ebfe66e59e62b7
description: 深潮TechFlow新闻聚合爬取。爬取https://www.techflowpost.com/?lang=zh-CN当天的文章，形成表格（日期、文章、主要内容、网址），并给出一段简短总结。用于用户询问"今天有什么新闻"、"汇总今天的文章"等场景。
license: MIT
name: techflow-news
version: 1.0.0
---

# TechFlow 新闻聚合

爬取深潮TechFlow网站当天文章，整理成表格并总结。

## 使用方法

1. 使用 extract_content_from_websites 工具提取网页内容
2. URL: `https://www.techflowpost.com/?lang=zh-CN`
3. 提取信息：文章标题、发布日期、主要内容摘要、文章链接

## 输出格式

### 表格部分

| 日期 | 文章 | 主要内容 | 网址 |
|------|------|----------|------|

### 总结部分

- 提取3-5个核心热点
- 用简短段落总结当天主要话题

## 注意事项

- 筛选当天（2026年X月X日）发布的文章
- 区分"深度文章"和"7x24h快讯"
- 文章链接需要补充完整URL（https://www.techflowpost.com + 相对路径）
