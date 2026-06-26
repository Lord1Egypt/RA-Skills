---
name: wechat-article-exporter
description: 微信公众号推文长截图导出工具。支持多种链接格式，自动处理懒加载图片、视频占位符、底部工具栏遮挡等问题。触发词：微信文章导出、公众号截图、推文保存、mp.weixin.qq.com。
author: codebuddy
version: "3.1.0"
tags:
  - wechat
  - 微信
  - 公众号
  - 推文
  - 截图
  - mp.weixin.qq.com
allowed-tools: Bash, Read, Write
---

# 微信公众号推文长截图导出工具

将微信公众号文章导出为长截图，完美保留原文排版。

## 触发词

- "微信文章导出"、"公众号文章截图"、"推文保存"
- "微信截图"、"公众号导出"
- 发送包含 `mp.weixin.qq.com` 的链接

## 执行命令

```bash
python3 /workspace/wechat-article-exporter/scripts/wechat_screenshot.py "<URL>" -o /workspace/output