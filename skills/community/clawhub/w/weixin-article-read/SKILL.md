---
name: weixin-article-read
description: 读取微信公众平台文章内容（mp.weixin.qq.com）。当用户发送微信文章链接、需要读取微信文章内容、提取公众号文章时自动激活。支持突破微信反爬限制，获取完整文章文本。
---

# 微信文章读取技能

## 功能说明

读取微信公众平台（mp.weixin.qq.com）文章内容，突破反爬限制，还原干净的文章文本。

## 使用场景

- 用户发送微信文章链接，需要读取内容
- 需要提取公众号文章进行总结、分析
- 微信文章链接需要突破反爬获取原文

## 核心脚本

```bash
# 使用方法
python3 scripts/read_weixin_article.py <微信文章URL>

# 示例
python3 scripts/read_weixin_article.py "https://mp.weixin.qq.com/s/kItlJmjOnq6p6tXtYGHrGQ"
```

## 技术实现

1. 使用 `curl` 模拟移动端 User-Agent 获取页面
2. 使用 BeautifulSoup 解析HTML
3. 提取 `id="js_content"` 或 `class="rich_media_content"` 的文章主体
4. 清理脚本、样式等干扰元素，还原干净文本

## 注意事项

- 微信文章有反爬限制，必须使用移动端 User-Agent
- 部分文章可能因权限问题无法完整获取
- 成功读取后记得向用户确认内容是否正确