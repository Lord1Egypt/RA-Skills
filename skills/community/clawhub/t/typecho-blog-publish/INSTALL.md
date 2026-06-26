# Typecho 博客发布技能 - 安装指南

## 前置要求

1. **Python 3.6+**
2. **Typecho 博客**（支持 XML-RPC）
3. **博客管理员账号**

## 安装步骤

### 1. 安装技能

```bash
# 从 ClawHub 安装
clawhub install typecho-blog-publish

# 或者手动克隆
git clone <repo-url> typecho-blog-publish
cd typecho-blog-publish
```

### 2. 环境检查

```bash
bash scripts/setup_runtime.sh
```

确保输出显示所有检查通过。

### 3. 配置博客信息

在工作区根目录创建或编辑 `.env` 文件：

```bash
# Typecho 博客配置
BLOG_URL=http://your-blog.com
BLOG_USERNAME=admin
BLOG_PASSWORD=your_password
BLOG_XMLRPC=/index.php/action/xmlrpc
```

**安全提示**：
- `.env` 文件权限应设为 600
- 不要将 `.env` 提交到版本控制
- 建议使用应用专用密码

### 4. 测试安装

```bash
# 查看帮助
python3 scripts/publish_post.py --help

# 查看博客统计
python3 scripts/manage.py stats
```

## 使用方法

### 发布文章

```bash
# 从文件发布
python3 scripts/publish_post.py --file article.md

# 保存为草稿
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

使用 Markdown 格式，头部包含元信息：

```markdown
---
title: 文章标题
categories: 分类 1, 分类 2
tags: 标签 1, 标签 2
---

# 正文内容

这里是文章内容...
```

## 常见问题

### Q: 提示"密码错误"
**A**: 检查 `.env` 文件是否存在，`BLOG_PASSWORD` 是否正确。

### Q: Markdown 不渲染
**A**: 技能会自动将 Markdown 转换为 HTML。如果仍有问题，检查 Typecho 后台设置。

### Q: 无法上传图片
**A**: 当前版本不支持自动上传图片。请手动上传后在文章中插入链接。

### Q: 如何批量发布？
**A**: 使用 `batch_publish.py` 脚本，支持设置延迟时间。

## 卸载

```bash
# 删除技能目录
rm -rf typecho-blog-publish
```

## 更新

```bash
# 拉取最新版本
git pull origin main

# 或者重新安装
clawhub update typecho-blog-publish
```

## 支持

- 文档：查看 `README.md` 和 `references/` 目录
- 问题反馈：提交 Issue
- 讨论：加入 Discord 社区

## 许可证

MIT License
