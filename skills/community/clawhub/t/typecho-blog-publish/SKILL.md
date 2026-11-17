---
name: typecho-blog-publish
description: 通过 XML-RPC 自动发布文章到 Typecho 博客。支持文件读取、草稿模式、标签管理。
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: ["python3"]
    primaryEnv: "BLOG_PASSWORD"
    optionalEnv: ["BLOG_URL", "BLOG_USERNAME", "BLOG_XMLRPC"]
---

# Typecho 博客发布技能

使用此技能来自动发布文章到你的 Typecho 博客。

## 配置

在 `.env` 文件中配置以下环境变量：

| 变量 | 说明 | 默认值 |
|---|---|---|
| `BLOG_URL` | 博客地址 | `http://yuanblog.tk:9980` |
| `BLOG_USERNAME` | 博客用户名 | `admin` |
| `BLOG_PASSWORD` | 博客密码（必需） | - |
| `BLOG_XMLRPC` | XML-RPC 路径 | `/index.php/action/xmlrpc` |

## 使用方法

### 1. 发布文章

```bash
# 从文件发布（推荐）
python3 {baseDir}/scripts/publish_post.py --file article.md

# 保存为草稿
python3 {baseDir}/scripts/publish_post.py --file article.md --draft

# 直接发布
python3 {baseDir}/scripts/publish_post.py "标题" "内容" "分类"
```

### 2. 智能配图与上传

```bash
# 智能搜索配图（基于主题关键词）
python3 {baseDir}/scripts/smart_image.py "AI 技术 未来"

# 上传图片到博客媒体库
python3 {baseDir}/scripts/upload_image.py image.jpg

# 组合使用：搜索+上传
python3 {baseDir}/scripts/smart_image.py "AI团队协作" && \
python3 {baseDir}/scripts/upload_image.py /tmp/theme_test.jpg
```

### 3. 管理博客

```bash
# 查看统计
python3 {baseDir}/scripts/manage.py stats

# 列出文章
python3 {baseDir}/scripts/manage.py list 10

# 删除文章
python3 {baseDir}/scripts/manage.py delete 123

# 查看最近文章详情
python3 {baseDir}/scripts/manage.py list 5
```

### 3. 批量操作

```bash
# 批量发布
python3 {baseDir}/scripts/batch_publish.py articles

# 批量保存草稿
python3 {baseDir}/scripts/batch_publish.py articles --draft
```

## 功能特性

- ✅ 支持文件读取（自动解析 Markdown 头部）
- ✅ 支持草稿模式（`--draft` 参数）
- ✅ 支持标签（tags）
- ✅ 自动日志记录（`publish_log.txt`）
- ✅ 友好的错误处理
- ✅ 智能配图（通过 `smart_image.py` 匹配主题图片）
- ✅ 图片上传（支持 Unsplash 高质量图片）
- ✅ 正确日期处理（避免 1970-01-01 bug）
- ✅ 分类兼容性（自动使用默认分类）

## 示例

### 示例 1：发布技术文章

```bash
python3 {baseDir}/scripts/publish_post.py --file ai-tutorial.md
```

### 示例 2：保存为草稿稍后发布

```bash
python3 {baseDir}/scripts/publish_post.py --file draft.md --draft
```

### 示例 3：带图片的文章发布

```markdown
---
title: "你的文章标题"
categories: []
tags: ["AI", "技术"]
date: "2026-03-27"
draft: false
---

# 文章标题

![图片描述](图片URL)

文章内容...
```

```bash
# 1. 智能搜索配图
python3 {baseDir}/scripts/smart_image.py "AI 技术"

# 2. 上传图片  
python3 {baseDir}/scripts/upload_image.py /tmp/theme_test.jpg

# 3. 在 Markdown 文件中使用图片 URL
# 4. 发布文章
python3 {baseDir}/scripts/publish_post.py --file article.md
```

### 示例 4：直接发布短内容

```bash
python3 {baseDir}/scripts/publish_post.py "AI 搞钱指南" "这是正文内容..." "AI，创业"
```

## 日志

所有发布记录会保存到 `{baseDir}/publish_log.txt`，包含时间戳和详细信息。

## 安全说明

- 密码存储在 `.env` 文件中，权限为 600（仅所有者可读写）
- 脚本自动读取 `.env` 文件中的配置
- 不要在代码中硬编码密码

## 相关文件

- `{baseDir}/scripts/publish_post.py` - 主发布脚本（支持 Markdown→HTML 转换）
- `{baseDir}/scripts/manage.py` - 博客管理工具（统计、列表、删除）
- `{baseDir}/scripts/upload_image.py` - 图片上传工具（Typecho 媒体库）
- `{baseDir}/scripts/smart_image.py` - 智能配图（Unsplash 主题匹配）
- `{baseDir}/scripts/batch_publish.py` - 批量发布工具
- `{baseDir}/publish_log.txt` - 发布日志
