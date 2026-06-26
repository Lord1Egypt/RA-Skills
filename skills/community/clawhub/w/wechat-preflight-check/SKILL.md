---
name: wechat-preflight-check
description: 用于微信公众号发布前检查 Markdown 文章
---

# 微信公众号发布前检查工具

## 用途
在将 Markdown 文章发布到微信公众号之前，进行自动化检查以确保文章格式正确、素材齐全。

## 何时调用
当用户要求检查微信公众号文章是否符合发布标准时调用此 skill。

## 检查项清单
1. 是否存在 frontmatter（YAML 头部信息）
2. 是否存在 title（文章标题）
3. 是否存在 cover（封面图片）
4. cover 是否为可访问 URL 或存在的本地文件
5. Markdown 文章内的图片路径是否存在
6. 是否发现 Obsidian wiki 图片链接 ![[...]]（微信不支持）
7. 是否存在未标注语言的 fenced code block

## 执行命令
```bash
python3 scripts/check.py <markdown_file>
```
