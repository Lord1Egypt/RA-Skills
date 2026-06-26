---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: "00000000000000000000000000000000"
    PropagateID: "00000000000000000000000000000000"
    ReservedCode1: 3044022008ad98e4a61f124b07916990e20c2c86d59d551d839df0b9c207cc26e28b695902200745c5c38a091af93cde3661469ff503f986f8255ed2f490232ffcb22c4ee2cb
    ReservedCode2: 3046022100b4520a31f66e0ffcea18e4aa458fd0b975c7c4016fa890cf411b74c4896469ba022100b83a16d148f9456fe998c67234c2cad311417ee908bd07bbee5d046669534b41
description: |-
    当需要获取网页内容时使用（搜索结果页面、博客文章、文档等）。使用 URL 转 Markdown 服务将网页转换为可读文本。
    触发场景：用户说"帮我查一下"、"看看这个链接"、"获取 xx 的信息"等需要上网抓信息的情况。
name: web-fetcher
---

# 网页抓取

当需要获取网页内容时，按以下顺序尝试：

## 首选方案：URL 转 Markdown 服务

1. **markdown.new/** (推荐)
   - 用法：在网址前加 `https://markdown.new/`
   - 例如：`https://markdown.new/https://example.com`
   - 适合 Cloudflare 支持的网站

2. **r.jina.ai/** (备用)
   - 用法：在网址前加 `https://r.jina.ai/`
   - 例如：`https://r.jina.ai/https://example.com`
   - 兼容性好

3. **defuddle.md/** (备用)
   - 用法：在网址前加 `https://defuddle.md/`
   - 例如：`https://defuddle.md/https://example.com`

## 备选方案：爬虫工具

如果以上服务都无法获取，尝试 Scrapling：
- 地址：https://github.com/D4Vinci/Scrapling
- 用法：`pip install scrapling` 后使用

## 使用流程

1. 先尝试 `r.jina.ai/{url}` （最稳定）
2. 如果失败，尝试 `markdown.new/{url}`
3. 再失败，尝试 `defuddle.md/{url}`
4. 都失败再考虑 Scrapling

## 注意事项

- 不需要配置任何搜索 API
- 这些服务会将网页转换为纯文本/ Markdown 格式
- 适合大多数静态网页
- 对于需要登录的页面可能无效
