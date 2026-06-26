---
name: wordpress-auto-publish
description: 自动将Markdown文章发布到WordPress博客。支持REST API发布、批量处理、草稿管理、分类标签管理等功能。
version: 1.0.0
date: 2026-04-04
compatibility: OpenClaw >= 2026.3.0
status: 开发中 🚧
---

# WordPress Auto-Publish Skill

## 🎯 技能描述

自动将Markdown文章发布到WordPress博客。支持：
- 通过REST API发布文章
- 批量发布文章
- 定时发布
- 草稿管理
- Markdown到HTML转换
- 分类和标签管理
- 特色图片上传

## 📋 功能特性

### 核心功能
- ✅ 自动发布Markdown文章到WordPress
- ✅ 支持草稿和已发布状态
- ✅ 批量处理多个文章
- ✅ 自动HTML转换
- ✅ 分类和标签管理
- ✅ 特色图片支持

### 管理功能
- ✅ 列出所有文章
- ✅ 更新/删除文章
- ✅ 管理媒体库
- ✅ 分类和标签管理

### 工具功能
- ✅ 配置管理
- ✅ 错误处理和日志
- ✅ 环境变量支持
- ✅ 批量处理队列

## 🚀 快速开始

### 步骤1：安装依赖
```bash
npm install axios marked
```

### 步骤2：配置WordPress
1. 在WordPress中启用REST API
2. 创建应用程序密码
3. 设置WordPress站点URL

### 步骤3：配置技能
1. 复制`config.example.js`为`config.js`
2. 填写WordPress配置信息
3. 设置文章目录

### 步骤4：使用示例
```bash
# 发布单篇文章
node publish.js --file posts/my-article.md

# 发布为草稿
node publish.js --file posts/draft.md --draft

# 批量发布
node batch-publish.js --dir posts/
```

## 📁 项目结构

```
wordpress-auto-publish/
├── SKILL.md                    # 技能文档
├── package.json               # 项目配置
├── config.js                  # 配置文件
├── wordpress-api.js           # WordPress API客户端
├── publish.js                 # 发布文章主脚本
├── batch-publish.js           # 批量发布脚本
├── list-posts.js              # 列出文章
├── delete-post.js             # 删除文章
├── upload-media.js            # 上传媒体文件
├── manage-categories.js       # 管理分类
├── manage-tags.js             # 管理标签
├── posts/                     # 文章目录
│   └── example-post.md       # 示例文章
└── scripts/                  # 工具脚本
    └── setup-wordpress.sh    # 安装脚本
```

## 🔧 详细使用指南

### 1. WordPress REST API配置
1. 登录WordPress后台
2. 进入 **用户 → 个人资料**
3. 在底部找到 **应用程序密码**
4. 创建新密码（如：`your-app-password`）
5. 保存生成的密码

### 2. 获取WordPress配置信息
- **WordPress URL**: 你的WordPress站点URL（如：`https://your-site.com`）
- **用户名**: WordPress用户名
- **应用程序密码**: 上一步生成的密码

### 3. 配置文件设置
创建 `config.js`：
```javascript
module.exports = {
  // WordPress配置
  wordpress: {
    url: process.env.WORDPRESS_URL || 'https://your-site.com',
    username: process.env.WORDPRESS_USERNAME || 'admin',
    password: process.env.WORDPRESS_PASSWORD || 'your-app-password',
    
    // API端点
    apiBase: '/wp-json/wp/v2',
    
    // 默认设置
    defaultStatus: 'draft', // draft, publish, pending, private
    defaultAuthor: 1,
    
    // 媒体设置
    mediaPath: './media',
    supportedFormats: ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx']
  },
  
  // 文章配置
  posts: {
    directory: process.env.POSTS_DIR || './posts',
    defaultCategory: 1,
    defaultTags: [],
    
    // Markdown转换设置
    markdownOptions: {
      gfm: true,
      breaks: true,
      sanitize: false
    }
  },
  
  // 发布设置
  publish: {
    batchSize: 5,
    delayBetweenPosts: 2000, // 毫秒
    maxRetries: 3,
    retryDelay: 1000
  },
  
  // 日志设置
  logging: {
    level: 'info',
    file: './logs/wordpress-publish.log',
    console: true
  }
};
```

### 4. 文章格式要求

#### Markdown文件结构
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

![示例图片](./images/example.jpg)
```

#### 元数据字段
- `title`: 文章标题（必需）
- `slug`: URL别名（可选）
- `status`: 状态 - draft/publish/pending/private（可选，默认draft）
- `categories`: 分类数组（可选）
- `tags`: 标签数组（可选）
- `featured_image`: 特色图片路径（可选）
- `excerpt`: 文章摘要（可选）
- `date`: 发布日期（可选）
- `author`: 作者名（可选）

## ⚙️ 环境变量

```bash
# WordPress配置
export WORDPRESS_URL="https://your-site.com"
export WORDPRESS_USERNAME="admin"
export WORDPRESS_PASSWORD="your-app-password"

# 文章配置
export POSTS_DIR="./posts"
export DEFAULT_STATUS="draft"
export DEFAULT_CATEGORY=1

# 发布设置
export BATCH_SIZE=5
export DELAY_BETWEEN_POSTS=2000
```

## 📝 使用示例

### 发布单篇文章
```bash
node publish.js --file posts/my-article.md --status publish
```

### 批量发布
```bash
node batch-publish.js --dir posts/ --status draft
```

### 列出所有文章
```bash
node list-posts.js --status any --per-page 20
```

### 上传特色图片
```bash
node upload-media.js --file images/featured.jpg --post-id 123
```

### 管理分类
```bash
# 列出分类
node manage-categories.js --list

# 创建分类
node manage-categories.js --create --name "技术" --slug "tech"
```

## 🔍 故障排除

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

### 错误代码
- `401`: 认证失败，检查凭据
- `403`: 权限不足，检查用户角色
- `404`: 资源不存在，检查URL
- `500`: 服务器错误，检查WordPress日志

## 📊 性能优化

### 批量处理建议
- 一次处理不超过10篇文章
- 添加延迟避免服务器压力
- 使用草稿模式先验证

### 资源管理
- 定期清理日志文件
- 备份配置文件
- 使用环境变量管理敏感信息

## 🎯 技能触发条件

当OpenClaw检测到以下需求时自动触发：
- 自动发布文章到WordPress
- 批量或定时发布
- WordPress API集成需求
- Markdown到WordPress转换

## 🔄 更新计划

### v1.1.0 (计划中)
- [ ] 定时发布功能
- [ ] 文章导入/导出
- [ ] 多站点支持
- [ ] 高级媒体管理

### v1.2.0 (计划中)
- [ ] 主题模板支持
- [ ] SEO优化
- [ ] 社交媒体分享
- [ ] 分析集成

## 📞 支持与反馈

如有问题或建议：
1. 查看详细文档
2. 运行 `node publish.js --help` 查看帮助
3. 检查错误日志获取详细信息
4. 提交问题到GitHub仓库

---

**注意**: 此技能需要WordPress 5.0+ 版本，并已启用REST API功能。