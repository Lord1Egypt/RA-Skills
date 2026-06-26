# WordPress Auto-Publish Skill

一个OpenClaw技能，用于自动将Markdown文章发布到WordPress博客。

## 🚀 快速开始

### 1. 安装
```bash
# 进入技能目录
cd /root/.openclaw/workspace/skills/wordpress-auto-publish

# 运行安装脚本
bash scripts/setup-wordpress.sh
```

### 2. 配置WordPress
1. 登录WordPress后台
2. 进入 **用户 → 个人资料**
3. 在底部找到 **应用程序密码**
4. 创建新密码（如：`xxxx xxxx xxxx xxxx`）
5. 保存生成的密码

### 3. 编辑配置文件
编辑 `config.js` 文件：
```javascript
wordpress: {
  url: 'https://your-wordpress-site.com',  // 你的WordPress站点
  username: 'your-username',               // WordPress用户名
  password: 'xxxx xxxx xxxx xxxx'          // 应用程序密码
}
```

### 4. 测试连接
```bash
npm test
# 或
node test-connection.js
```

## 📝 使用指南

### 发布单篇文章
```bash
node publish.js --file posts/my-article.md --status publish
```

### 批量发布文章
```bash
node batch-publish.js --dir posts/ --status draft
```

### 列出WordPress文章
```bash
node list-posts.js --status any --per-page 20
```

### 查看帮助
```bash
node publish.js --help
node batch-publish.js --help
node list-posts.js --help
```

## 📁 文章格式

### Markdown文件示例
```markdown
---
title: 文章标题
slug: article-slug
status: draft
categories:
  - 技术
  - 编程
tags:
  - WordPress
  - API
  - 自动化
featured_image: ./images/featured.jpg
excerpt: 文章摘要
date: 2026-04-04
author: 作者名
---

# 文章内容

这里是文章的Markdown内容...

## 二级标题

- 支持标准Markdown语法
- 支持代码块
- 支持图片链接
```

### 支持的元数据字段
- `title`: 文章标题（必需）
- `slug`: URL别名（可选）
- `status`: 状态 - draft/publish/pending/private（默认draft）
- `categories`: 分类数组（可选）
- `tags`: 标签数组（可选）
- `featured_image`: 特色图片路径（可选）
- `excerpt`: 文章摘要（可选）
- `date`: 发布日期（可选）
- `author`: 作者名（可选）

## 🔧 故障排除

### 常见问题

1. **API连接失败**
   - 检查WordPress URL是否正确
   - 验证应用程序密码
   - 确保REST API已启用

2. **认证失败**
   - 检查用户名和密码
   - 重新生成应用程序密码
   - 验证用户权限

3. **文章发布失败**
   - 检查网络连接
   - 验证文章格式
   - 查看错误日志

### 查看日志
```bash
cat logs/wordpress-publish.log
```

## 📊 功能特性

- ✅ **Markdown支持** - 完整Markdown语法支持
- ✅ **批量处理** - 一次发布多篇文章
- ✅ **分类标签** - 自动创建和管理
- ✅ **特色图片** - 支持上传特色图片
- ✅ **错误重试** - 自动重试失败的操作
- ✅ **详细日志** - 完整的操作日志

## 🎯 技能触发

当OpenClaw检测到以下需求时自动触发：
- 发布文章到WordPress
- 批量发布文章
- WordPress博客管理
- Markdown到WordPress转换

## 📞 支持

如有问题，请：
1. 查看详细文档 `SKILL.md`
2. 检查错误日志
3. 运行测试脚本 `npm test`

---

**版本**: 1.0.0  
**更新日期**: 2026-04-04  
**兼容性**: WordPress 5.0+，Node.js 14+