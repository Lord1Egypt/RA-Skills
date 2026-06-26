# Scrapling Fetch 使用指南

## 快速开始

```bash
# 最简单的用法
python3 scripts/scrapling_fetch.py "https://example.com/article"

# 限制输出长度
python3 scripts/scrapling_fetch.py "https://example.com" 10000
```

## 抓取模式

### Basic 模式（默认）

使用 HTTP 请求抓取，速度快，适合静态页面。

```bash
python3 scripts/scrapling_fetch.py "https://example.com" --mode basic
```

**适用场景：**
- 静态 HTML 页面
- 无反爬保护的网站
- 博客、新闻等文章页面

### Stealth 模式

使用隐身浏览器抓取，可绕过 Cloudflare 等反爬机制。

```bash
python3 scripts/scrapling_fetch.py "https://protected-site.com" --mode stealth
```

**适用场景：**
- 有 Cloudflare 保护的网站
- 有反爬检测的页面
- Basic 模式返回空内容时

## 输出格式

### 文本格式（默认）

```bash
python3 scripts/scrapling_fetch.py "https://example.com"
```

输出：
```
# 文章标题

正文内容（Markdown 格式）...
```

### JSON 格式

```bash
python3 scripts/scrapling_fetch.py "https://example.com" --json
```

输出：
```json
{
  "url": "https://example.com",
  "title": "文章标题",
  "content": "正文内容...",
  "selector": "article",
  "length": 5234,
  "truncated": false,
  "mode": "basic"
}
```

## 高级用法

### 抓取新闻网站

```bash
# 新闻网站通常有反爬保护
python3 scripts/scrapling_fetch.py "https://news-site.com/article/123" --mode stealth
```

### 抓取技术博客

```bash
# 技术博客通常是静态页面
python3 scripts/scrapling_fetch.py "https://tech-blog.com/post" 50000
```

### 批量抓取脚本

```bash
#!/bin/bash
# batch_fetch.sh

urls=(
    "https://site1.com/article1"
    "https://site2.com/article2"
    "https://site3.com/article3"
)

for url in "${urls[@]}"; do
    filename=$(echo "$url" | md5sum | cut -d' ' -f1)
    python3 scripts/scrapling_fetch.py "$url" > "output/${filename}.md"
    sleep 2  # 避免请求过快
done
```

## 选择器策略

脚本按以下优先级尝试正文选择器：

1. `article` - HTML5 语义化文章标签
2. `main` - HTML5 主内容标签
3. `.post-content` - WordPress 等常见博客
4. `.article-content` - 新闻网站常见类名
5. `.entry-content` - 另一种常见博客类名
6. `.post-body` - 文章正文类名
7. `[class*='body']` - 包含 body 的任意类名
8. `[class*='content']` - 包含 content 的任意类名
9. `#content` - content ID
10. `#main` - main ID
11. `body` - 最后回退

## 与 AI 配合使用

抓取内容后直接传递给 AI 处理：

```bash
# 抓取文章内容并保存
content=$(python3 scripts/scrapling_fetch.py "https://example.com" 20000)

# 让 AI 总结内容
echo "请总结以下文章：\n\n$content" | ai-chat
```

## 常见问题

### Q: 为什么抓取的内容为空？

A: 可能原因：
1. 网站有反爬保护 → 使用 `--mode stealth`
2. 网站需要 JavaScript 渲染 → 使用 `--mode stealth`
3. 选择器未命中 → 使用 `--debug` 查看

### Q: 如何抓取需要登录的页面？

A: 需要配合 Session 使用，参考 Scrapling 官方文档中的 Session 功能。

### Q: 抓取速度慢怎么办？

A: 
1. 优先使用 `--mode basic`
2. 减少输出字符数
3. 检查网络连接

## 性能建议

- **静态页面** → `--mode basic`（约 1-2 秒）
- **反爬页面** → `--mode stealth`（约 5-10 秒）
- **批量抓取** → 添加延迟，避免触发限制
