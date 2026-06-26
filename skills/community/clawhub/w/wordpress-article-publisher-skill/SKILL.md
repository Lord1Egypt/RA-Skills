---
name: wordpress-article-publisher
description: WordPress文章发布助手 - 根据关键词生成文章并发布到WordPress网站。
  触发场景：(1) 用户要求"发布文章"、"发布到WordPress"、"wordpress发布"
  (2) 用户提供了WordPress用户名、密码和API地址
  (3) 用户提供了文章关键词，要求生成并发布文章
  (4) 用户要求"创建WordPress技能"、"wordpress发布助手"
  注意：从不保存密码到文件，每次会话需要用户提供。
---

# WordPress 文章发布助手

## 功能概述

根据用户提供的关键词自动生成文章（约1000字）并发布到WordPress网站。

## 工作流程

### 第一步：收集认证信息

**必须收集以下信息（不保存到文件）：**
- WordPress用户名
- 应用程序密码（Application Password）
- 发布API地址（格式：`https://你的域名/wp-json/wp/v2/posts`）

**示例：**

```
用户名：liuxc
应用程序密码：xxxx xxxx xxxx xxxx
发布API：https://3dkee.com/wp-json/wp/v2/posts
```

### 第二步：生成文章

根据关键词生成约1000字的文章结构：
```
引言（100-150字）
优势分析（300-400字）
劣势分析（300-400字）
如何平衡使用（150-200字）
结论（100-150字）
```

### 第三步：发布文章

使用 `scripts/publish_article.ps1` 脚本发布。

## 脚本使用

### publish_article.ps1

**参数：**
- `-SiteUrl` - WordPress站点URL（不含wp-json部分）
- `-Username` - WordPress用户名
- `-AppPassword` - 应用程序密码
- `-Title` - 文章标题
- `-Content` - 文章内容（HTML格式）
- `-Status` - 发布状态（默认：publish）

**使用示例：**
```powershell
.\publish_article.ps1 -SiteUrl "https://3dkee.com" -Username "liuxucai" -AppPassword "xxxx xxxx" -Title "文章标题" -Content "<p>文章内容</p>"
```

**注意：**
- 内容必须为HTML格式
- 使用UTF-8编码确保中文正常显示
- 脚本使用curl.exe发送请求，避免PowerShell中文编码问题

## 编码处理

**问题：** PowerShell的`Invoke-RestMethod`处理中文UTF-8时存在编码bug

**解决方案：**
- JSON文件保存为UTF-8无BOM格式
- HTTP请求头设置`charset=utf-8`
- 使用`curl.exe`发送请求

详见 `references/encoding-fix.md`

## 错误处理

### 中文显示问号

**原因：** PowerShell编码问题

**解决方案：** 重新发布，脚本已使用curl.exe处理

### 发布失败

**可能原因：**
1. 认证信息错误
2. API地址不正确
3. 网络连接问题

**排查步骤：**
1. 检查认证信息是否正确
2. 验证API地址是否可访问
3. 检查应用程序密码是否有效

## 高级功能

### 分类和标签

提供关键词时可同时指定：
```
关键词：AI文章的利弊
分类：科技
标签：人工智能,内容创作
```

### 调整字数

```
关键词：xxx
字数：2000字
```

### 修改已发布文章

```
修改文章 ID 3159 的标题为"新标题"
```

脚本会自动删除原文章并重新发布。

## 安全注意事项

- ✅ 不将密码保存到文件
- ✅ 不将密码写入日志
- ✅ 每次会话需要重新提供密码
- ✅ 临时JSON文件使用后删除

## 参考文档

- `references/wordpress-setup.md` - WordPress应用程序密码设置教程
- `references/encoding-fix.md` - 中文编码问题解决方案
- `references/api-reference.md` - WordPress REST API参考
