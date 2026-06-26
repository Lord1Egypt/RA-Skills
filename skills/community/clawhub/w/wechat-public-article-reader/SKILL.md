---
name: wechat-reader
description: >
  读取微信公众号文章内容，返回标题、公众号名、发布时间和正文。
  使用场景：(1) 用户发来 mp.weixin.qq.com/s/xxx 链接要求阅读或总结，
  (2) 用户提到"微信文章"、"公众号文章"、"帮我看看这篇"并附带微信链接，
  (3) 需要提取微信公众号文章内容进行分析、翻译或摘要。
  不适用于：搜索公众号、浏览公众号历史文章列表、需要登录才能查看的内容。
---

# 微信公众号文章读取

## 使用方式

识别到微信公众号链接（包含 `mp.weixin.qq.com`）时，运行脚本读取：

```bash
# 可读文本输出
python3 {baseDir}/scripts/read_wechat.py "<url>"

# JSON 结构化输出
python3 {baseDir}/scripts/read_wechat.py "<url>" --json
```

## 输出字段

- `title`：文章标题
- `author`：公众号名称
- `pub_time`：发布时间（Asia/Shanghai）
- `content`：正文纯文本（含图片链接标记）
- `url`：原始链接

## 注意事项

- 仅支持公开可访问的文章，已删除或需登录的文章无法读取
- 部分文章标题/作者可能提取不到（微信页面结构变化），正文通常可正常提取
- 图片以 `[图片: url]` 标记保留在正文中
- 无需任何 API Key 或 Cookie，纯 HTTP 抓取
