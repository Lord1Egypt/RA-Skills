---
name: web-extractor
description: 使用 jina.ai 提取网页干净文本并让 Agent 总结。触发词：提取网页、总结新闻、提取文章、获取页面内容
---

# 网页内容提取技能

使用 r.jina.ai 提取网页干净文本，过滤垃圾代码，提取干货内容。

## 工作流程

### 1. 提取网页内容

```bash
# 提取网页并保存为 md 文件
curl -s https://r.jina.ai/<URL> > /tmp/web-content.md
```

### 2. 读取并总结

让 Agent 读取生成的 md 文件，总结核心观点。

## 使用示例

**用户说："帮我总结这个新闻 https://www.bbc.com/news/tech..."**

执行：
```bash
curl -s "https://r.jina.ai/https://www.bbc.com/news/technology-xxx" > /tmp/news.md
```

然后读取 /tmp/news.md 文件内容，分析并总结。

## 注意事项

- r.jina.ai 会过滤掉 script、nav、广告 CSS 等垃圾代码
- 提取后是极干净的纯文本，对 AI 零负担
- 支持任何新闻网站、技术博客、文章页面
- 文件默认保存到 /tmp/ 目录，可自定义路径