---
name: typecho-post-publisher
description: 发布文章到 Typecho 博客。使用场景：(1) 用户要求发布新文章到 Typecho 博客 (2) 帮助用户撰写并发布博客文章 (3) 编辑或更新已有文章。此技能封装了登录凭据和完整的发布流程，包括填写标题、内容、选择分类和发布操作。
---

# Typecho 文章发布

## 快速开始

1. 使用 browser 工具连接用户的 Chrome 浏览器（需要安装 OpenClaw Browser Relay 扩展）
2. 导航到博客后台：`https://你的博客地址/admin/`
3. 登录（用户名和密码需要在技能配置中设置）
4. 点击「撰写」进入文章编辑器
5. 填写标题、内容，选择分类
6. 点击「发布文章」

## 登录凭据

> 注意：以下为占位符，实际使用时需要替换为真实的博客凭据

- **URL**: https://your-blog.com/admin/
- **用户名**: YOUR_USERNAME
- **密码**: YOUR_PASSWORD

## 发布流程

### 新建文章

1. 导航到 `https://你的博客地址/admin/write-post.php`
2. 填写标题（标题输入框）
3. 填写文章内容（内容输入框，支持 Markdown）
4. 在右侧边栏选择分类（勾选对应分类 checkbox）
5. 点击「发布文章」按钮

### 编辑已有文章

1. 导航到 `https://你的博客地址/admin/manage-posts.php`
2. 找到要编辑的文章，点击标题或「编辑」链接
3. 修改内容
4. 点击「发布文章」保存更新

### 选择分类

在右侧边栏的「分类」部分：
- 默认分类
- Docker
- 系统与环境
- 开发工具
- 服务器路由器
- CodeIgniter
- Laravel
- 苹果相关
- Golang
- AI

## 常见问题

**发布失败提示"没有选择分类"**：确保在右侧边栏勾选了至少一个分类

**内容填写失败**：可以尝试分步填写，先填标题，再填内容

## 使用 Chrome 扩展控制

1. 用户需要安装 OpenClaw Browser Relay 扩展
2. 在目标标签页点击扩展图标确保显示 ON
3. 使用 `profile: "chrome"` 调用 browser 工具
