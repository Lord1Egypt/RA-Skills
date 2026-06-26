---
name: wechat-articles
description: 抓取微信公众号文章并转换为Markdown格式。当用户提供微信文章链接（mp.weixin.qq.com）或要求抓取/保存/下载公众号文章时触发。
---

# 微信公众号文章抓取

抓取微信公众号文章，提取标题、作者、公众号名称、正文内容和图片，转换为干净的Markdown格式保存。

## 使用方式

用户提供微信文章链接，例如：
- `https://mp.weixin.qq.com/s/xxxxx`
- `https://mp.weixin.qq.com/s?__biz=xxx&mid=xxx&idx=1&sn=xxx`

## 抓取流程

1. **接收链接** - 用户提供微信文章URL
2. **浏览器抓取** - 使用Playwright打开链接，等待页面加载完成
3. **提取内容** - 获取标题、作者、公众号名称、正文HTML
4. **转换Markdown** - 将HTML转换为干净的Markdown格式
5. **保存文件** - 以标题为文件名保存到指定目录

## 内容提取选择器

微信文章页面的关键元素：

```
标题:     #activity-name
作者:     #js_name (公众号名称)
正文:     #js_content
发布时间: #publish_time
```

## 执行脚本

```bash
python3 ~/.nvm/versions/node/v24.14.0/lib/node_modules/openclaw/skills/wechat-articles/scripts/fetch_article.py "<URL>" [--output <目录>]
```

脚本会：
- 用Playwright headless浏览器打开链接
- 等待页面加载完成（最多30秒）
- 提取并转换为Markdown
- 保存为 `<标题>.md`

## 输出格式

生成的Markdown文件结构：

```markdown
---
title: 文章标题
author: 公众号名称
url: https://mp.weixin.qq.com/s/xxxxx
fetched: 2024-01-15T10:30:00Z
---

# 文章标题

> 作者：公众号名称

正文内容...

[图片说明](images/xxx.jpg)
```

## 图片处理

- 默认下载图片到同目录的 `images/` 子文件夹
- Markdown中图片引用相对路径
- 可用 `--no-images` 参数跳过图片下载

## 注意事项

- 微信文章可能有防爬机制，首次访问可能需要等待更长时间
- 部分文章需要微信内打开才能查看完整内容（如付费文章）
- 如果抓取失败，可能需要用户提供截图或手动复制内容
