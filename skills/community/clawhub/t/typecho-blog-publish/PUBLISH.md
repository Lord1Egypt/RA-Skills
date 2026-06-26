# Typecho Blog Publish Skill

通过 XML-RPC 自动发布文章到 Typecho 博客。支持 Markdown、文件读取、草稿模式、标签管理。

## 特性

- ✅ **Markdown 自动转换**：自动将 Markdown 转换为 HTML 发布
- ✅ **文件读取**：从 Markdown 文件读取内容和元信息
- ✅ **草稿模式**：支持保存为草稿或立即发布
- ✅ **标签管理**：自动解析和设置分类、标签
- ✅ **批量操作**：支持批量发布多篇文章
- ✅ **博客管理**：查看、删除、统计等管理功能
- ✅ **日志记录**：完整的操作日志
- ✅ **错误处理**：友好的错误提示

## 快速开始

### 1. 安装

```bash
clawhub install typecho-blog-publish
```

### 2. 配置

在 `.env` 文件中配置：

```bash
BLOG_URL=http://your-blog.com
BLOG_USERNAME=admin
BLOG_PASSWORD=your_password
```

### 3. 发布文章

```bash
python3 scripts/publish_post.py --file article.md
```

## 文档

- [安装指南](INSTALL.md) - 详细安装步骤
- [使用示例](references/examples.md) - 完整使用示例
- [故障排查](references/troubleshooting.md) - 问题解决
- [Markdown 指南](references/markdown-guide.md) - Markdown 语法支持

## 命令

### 发布文章

```bash
# 从文件发布
python3 scripts/publish_post.py --file article.md

# 保存草稿
python3 scripts/publish_post.py --file article.md --draft

# 直接发布
python3 scripts/publish_post.py "标题" "内容" "分类"
```

### 管理博客

```bash
# 查看统计
python3 scripts/manage.py stats

# 列出文章
python3 scripts/manage.py list 10

# 删除文章
python3 scripts/manage.py delete 123
```

### 批量操作

```bash
# 批量发布
python3 scripts/batch_publish.py articles/

# 批量保存草稿
python3 scripts/batch_publish.py articles/ --draft
```

## 文章格式

```markdown
---
title: 文章标题
categories: 分类 1, 分类 2
tags: 标签 1, 标签 2
---

# 正文

内容...
```

## 系统要求

- Python 3.6+
- Typecho 博客（支持 XML-RPC）
- 博客管理员账号

## 许可证

MIT License

## 作者

团子
