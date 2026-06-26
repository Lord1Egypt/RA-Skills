# WordPress API访问设置指南

## 问题诊断
当前WordPress站点 (`https://openow.ai`) 的REST API基本可用，但认证失败。错误信息显示：
- `rest_not_logged_in` - 用户未登录
- `rest_cannot_create` - 没有创建文章的权限

## 解决方案

### 方案1: 使用WordPress内置的应用程序密码（推荐）

WordPress 5.6+ 版本内置了应用程序密码功能，无需安装额外插件。

#### 设置步骤:
1. **登录WordPress后台**
   - 访问 `https://openow.ai/wp-admin`
   - 使用管理员账号登录

2. **创建应用程序密码**
   - 进入 **用户 → 个人资料**
   - 滚动到页面底部的 **"应用程序密码"** 部分
   - 输入应用程序名称（如：`OpenClaw API`）
   - 点击 **"添加新应用程序密码"**
   - **重要**: 立即复制生成的密码（格式如：`xxxx xxxx xxxx xxxx xxxx xxxx`）
   - 这个密码只显示一次，请妥善保存

3. **验证用户权限**
   - 确保用户有发布文章的权限
   - 管理员账号通常有所有权限

#### 配置示例:
```javascript
const config = {
  url: 'https://openow.ai',
  username: 'inkmind',  // WordPress用户名
  appPassword: 'xxxx xxxx xxxx xxxx xxxx xxxx'  // 应用程序密码
};
```

### 方案2: 安装JWT认证插件

如果需要更灵活的认证方式（如token-based认证），可以安装JWT插件。

#### 安装步骤:
1. **安装插件**
   - 在WordPress后台，进入 **插件 → 安装插件**
   - 搜索 **"JWT Authentication for WP REST API"**
   - 安装并激活插件

2. **配置wp-config.php**
   - 编辑WordPress根目录下的 `wp-config.php` 文件
   - 在 `/* That's all, stop editing! Happy publishing. */` 之前添加：
   ```php
   define('JWT_AUTH_SECRET_KEY', 'your-top-secret-key');
   define('JWT_AUTH_CORS_ENABLE', true);
   ```
   - 将 `your-top-secret-key` 替换为强密码

3. **获取JWT令牌**
   ```javascript
   // 获取令牌
   const response = await axios.post('https://openow.ai/wp-json/jwt-auth/v1/token', {
     username: 'inkmind',
     password: 'your-password'
   });
   
   const jwtToken = response.data.token;
   
   // 使用令牌访问API
   const api = axios.create({
     baseURL: 'https://openow.ai/wp-json/wp/v2',
     headers: {
       'Authorization': `Bearer ${jwtToken}`,
       'Content-Type': 'application/json'
     }
   });
   ```

### 方案3: 安装Basic Auth插件

如果WordPress版本较旧，可以安装Basic Auth插件。

#### 推荐插件:
1. **Application Passwords** (WordPress官方)
2. **Basic Authentication** (第三方)

#### 安装步骤:
1. 安装并激活插件
2. 按照插件说明配置
3. 使用Basic Auth访问API

## 测试脚本

### 测试应用程序密码:
```bash
cd /root/.openclaw/workspace/skills/wordpress-auto-publish
node test-app-password.js
```

### 测试JWT认证:
```bash
cd /root/.openclaw/workspace/skills/wordpress-auto-publish
node test-jwt.js
```

## 自动发布配置

### 1. 更新配置文件
编辑 `config.js`:
```javascript
module.exports = {
  wordpress: {
    url: 'https://openow.ai',
    username: 'inkmind',
    password: 'your-app-password',  // 应用程序密码
    // ... 其他配置
  }
};
```

### 2. 创建测试文章
在 `posts/` 目录下创建Markdown文件:
```markdown
---
title: 测试文章
slug: test-article
status: draft
categories: [测试]
tags: [API, 自动化]
excerpt: 这是一个测试文章
date: 2026-04-06
---

# 测试文章标题

这是通过API自动发布的测试文章内容。
```

### 3. 发布文章
```bash
node publish.js --file posts/test-article.md --status draft
```

## 故障排除

### 常见错误及解决方案:

1. **401 Unauthorized**
   - 检查用户名和密码是否正确
   - 确认使用的是应用程序密码而不是登录密码
   - 验证用户是否有API访问权限

2. **403 Forbidden**
   - 检查用户角色和权限
   - 确保用户有发布文章的权限
   - 验证API端点是否受限制

3. **404 Not Found**
   - 检查WordPress URL是否正确
   - 确认REST API已启用
   - 验证插件是否已安装并激活

4. **500 Internal Server Error**
   - 检查WordPress错误日志
   - 验证插件配置
   - 检查服务器权限设置

### 调试建议:
1. 先测试公开API端点是否可用
2. 逐步测试认证流程
3. 检查网络连接和防火墙设置
4. 查看WordPress调试日志

## 安全建议

1. **使用强密码**: 应用程序密码应足够复杂
2. **限制权限**: 为API用户分配最小必要权限
3. **定期轮换**: 定期更新应用程序密码
4. **HTTPS**: 确保使用HTTPS连接
5. **IP限制**: 如果可能，限制API访问的IP地址

## 下一步

1. 在WordPress中设置应用程序密码
2. 使用新的应用程序密码测试API访问
3. 配置自动发布脚本
4. 设置定时任务或webhook触发发布

如需进一步帮助，请提供具体的错误信息和WordPress版本信息。