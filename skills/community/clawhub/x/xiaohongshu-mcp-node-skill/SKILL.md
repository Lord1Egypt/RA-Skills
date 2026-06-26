---
name: xiaohongshu-mcp-node
description: 通过 MCP 协议操作小红书平台，支持内容发布、搜索、互动等完整功能
version: 1.0.0
author: Ping Si <sipingme@gmail.com>
type: mcp-server
requires:
  - mcpServer: xiaohongshu-mcp-node
  - node: ">=20.0.0"
  - browser: chromium
tags:
  - xiaohongshu
  - mcp
  - social-media
  - automation
repository: https://github.com/sipingme/xiaohongshu-mcp-node-skill
mcpServer: https://github.com/sipingme/xiaohongshu-mcp-node
---

# 小红书 MCP Skill

通过 Model Context Protocol 让 AI 能够操作小红书平台。

## 🏗️ 架构说明

本 Skill 是一个 MCP Server 集成配置，实际功能由 [xiaohongshu-mcp-node](https://github.com/sipingme/xiaohongshu-mcp-node) MCP Server 提供。

```
OpenClaw/AI Agent
    ↓ (读取 Skill 配置)
xiaohongshu-mcp-node-skill
    ↓ (启动 MCP Server)
xiaohongshu-mcp-node
    ↓ (MCP Protocol - 13 Tools)
小红书平台
```

## 🎯 何时使用此 Skill

当用户需要操作小红书平台时，AI 会自动调用相应的 MCP 工具：

### 账号管理
- 登录小红书账号
- 检查登录状态

### 内容发布
- 发布图文笔记（标题、正文、图片、标签）
- 发布视频内容

### 内容搜索
- 搜索小红书内容
- 获取推荐列表
- 查看内容详情

### 互动功能
- 发表评论
- 点赞/取消点赞
- 收藏/取消收藏
- 获取评论列表

**触发关键词**：
- "发布到小红书"、"小红书发布"
- "搜索小红书"、"在小红书上搜索"
- "小红书评论"、"评论这条小红书"
- "点赞小红书"、"收藏小红书内容"

## 📋 前置要求

### 1. 安装 xiaohongshu-mcp-node MCP Server

```bash
# 克隆并构建 MCP Server
git clone https://github.com/sipingme/xiaohongshu-mcp-node.git
cd xiaohongshu-mcp-node

# 安装依赖
npm install

# 安装浏览器
npx playwright install chromium

# 构建项目
npm run build

# 首次登录（获取 Cookie）
npm run login
```

### 2. 配置 OpenClaw

在 OpenClaw 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "xiaohongshu": {
      "command": "node",
      "args": ["/path/to/xiaohongshu-mcp-node/dist/index.js"],
      "env": {
        "HEADLESS": "true",
        "COOKIES_PATH": "/path/to/cookies.json"
      }
    }
  }
}
```

### 3. 安装 Skill 文档

```bash
# 克隆 Skill 配置和文档
git clone https://github.com/sipingme/xiaohongshu-mcp-node-skill.git
cp -r xiaohongshu-mcp-node-skill ~/.openclaw/skills/xiaohongshu/
```

## 🚀 标准操作流程 (SOP)

### 操作 1：检查登录状态

**场景**：在执行任何操作前，先确认登录状态

**MCP 工具**：`xhs_check_login`

**步骤**：

1. AI 调用 `xhs_check_login` 工具
2. 解析返回结果
3. 如果未登录，引导用户登录

**输出示例**：
```json
{
  "isLoggedIn": true,
  "username": "用户名"
}
```

**异常处理**：
- 如果 `isLoggedIn: false`，执行操作 2（登录流程）
- 如果 Cookie 过期，提示用户重新登录

---

### 操作 2：登录小红书

**场景**：首次使用或 Cookie 过期

**MCP 工具**：`xhs_get_qrcode`

**步骤**：

1. AI 调用 `xhs_get_qrcode` 工具获取二维码
2. 向用户展示二维码（Base64 图片）
3. 提示用户使用小红书 App 扫码
4. 扫码成功后，Cookie 自动保存

**输出示例**：
```json
{
  "image": "data:image/png;base64,iVBORw0KG...",
  "timeout": "4m"
}
```

**异常处理**：
- 二维码过期：重新调用工具
- 扫码失败：检查网络连接

---

### 操作 3：发布图文内容

**场景**：用户提供标题、正文和图片，发布到小红书

**MCP 工具**：`xhs_publish_note`

**步骤**：

1. 验证用户已登录（调用 `xhs_check_login`）
2. 收集发布信息：
   - 标题（必需，最多20字）
   - 正文内容（必需）
   - 图片路径列表（必需，至少1张，最多9张）
   - 标签（可选，最多10个）
   - 是否原创（可选）
   - 可见范围（可选：public/private/friends）

3. 调用 `xhs_publish_note` 工具：

```json
{
  "title": "文章标题",
  "content": "文章正文内容...",
  "imagePaths": ["/path/to/image1.jpg", "/path/to/image2.jpg"],
  "tags": ["标签1", "标签2"],
  "isOriginal": true,
  "visibility": "public"
}
```

4. 等待发布完成（可能需要30-60秒）

5. 向用户报告结果

**输出示例**：
```json
{
  "success": true,
  "noteId": "abc123",
  "message": "发布成功"
}
```

**异常处理**：
- 标题超过20字：提示用户修改
- 图片不存在：提示用户检查路径
- 未登录：先执行登录流程
- 网络错误：重试或提示用户

---

### 操作 3：发布视频内容

**场景**：用户提供标题、正文和视频文件

**步骤**：

```bash
xhs-cli publish-video \
  --title-file /tmp/title.txt \
  --content-file /tmp/content.txt \
  --video /path/to/video.mp4 \
  --tags "视频" "教程"
```

**参数说明**：
- `--title` 或 `--title-file`：标题（必需）
- `--content` 或 `--content-file`：正文内容（必需）
- `--video`：视频文件路径（必需）
- `--tags`：标签列表（可选）
- `--visibility`：可见范围（可选）

**注意事项**：
- 视频上传时间较长（5-10分钟）
- 视频大小限制：通常不超过 1GB
- 支持格式：MP4, MOV 等

---

### 操作 4：搜索内容

**场景**：用户想搜索小红书上的内容

**步骤**：

```bash
xhs-cli search \
  --keyword "Node.js" \
  --sort-by "综合" \
  --note-type "图文"
```

**参数说明**：
- `--keyword`：搜索关键词（必需）
- `--sort-by`：排序方式（可选）
- `--note-type`：笔记类型（可选）
- `--publish-time`：发布时间（可选）

**输出示例**：
```json
{
  "success": true,
  "count": 20,
  "feeds": [
    {
      "id": "abc123",
      "xsecToken": "xyz789",
      "title": "Node.js 开发技巧",
      "user": {
        "userId": "user123",
        "nickname": "技术博主",
        "avatar": "https://..."
      },
      "cover": "https://...",
      "likeCount": "1.2k",
      "commentCount": "89"
    }
  ],
  "message": "找到 20 条结果"
}
```

---

### 操作 5：获取内容详情

**场景**：用户想查看某条内容的详细信息

**步骤**：

```bash
xhs-cli get-detail \
  --feed-id "abc123" \
  --xsec-token "xyz789" \
  --load-all-comments
```

**参数说明**：
- `--feed-id`：内容ID（必需，从搜索结果中获取）
- `--xsec-token`：安全令牌（必需，从搜索结果中获取）
- `--load-all-comments`：加载所有评论（可选）

**输出包含**：
- 完整标题和正文
- 所有图片URL
- 用户信息
- 点赞数、评论数
- 评论列表

---

### 操作 6：发表评论

**场景**：用户想对某条内容发表评论

**步骤**：

```bash
cat > /tmp/comment.txt << 'EOF'
很棒的分享！学到了很多。
EOF

xhs-cli comment \
  --feed-id "abc123" \
  --xsec-token "xyz789" \
  --content-file /tmp/comment.txt
```

**参数说明**：
- `--feed-id`：内容ID（必需）
- `--xsec-token`：安全令牌（必需）
- `--content` 或 `--content-file`：评论内容（必需）

---

### 操作 7：点赞内容

**场景**：用户想点赞某条内容

**步骤**：

```bash
# 点赞
xhs-cli like \
  --feed-id "abc123" \
  --xsec-token "xyz789"

# 取消点赞
xhs-cli like \
  --feed-id "abc123" \
  --xsec-token "xyz789" \
  --unlike
```

---

### 操作 8：收藏内容

**场景**：用户想收藏某条内容

**步骤**：

```bash
# 收藏
xhs-cli favorite \
  --feed-id "abc123" \
  --xsec-token "xyz789"

# 取消收藏
xhs-cli favorite \
  --feed-id "abc123" \
  --xsec-token "xyz789" \
  --unfavorite
```

---

### 操作 9：获取推荐列表

**场景**：用户想查看推荐内容

**步骤**：

```bash
xhs-cli list-feeds
```

**输出**：返回20条推荐内容，格式同搜索结果

---

## 📊 输入输出规范

### 命令行输出格式

所有命令统一使用 JSON 格式输出：

**成功响应**：
```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

**错误响应**：
```json
{
  "success": false,
  "error": "错误信息"
}
```

### 标题长度限制

小红书标题最多 **20个字**，计算规则：
- 中文字符、全角字符：每个计 1 个字
- 英文字母、数字、半角字符：每个计 0.5 个字

如果超长，需要提示用户修改或自动截断。

### 图片要求

- **格式**：JPG, PNG, GIF, WEBP
- **数量**：图文发布至少 1 张，最多 9 张
- **大小**：单张不超过 10MB
- **来源**：支持本地路径和 URL（自动下载）

### 视频要求

- **格式**：MP4, MOV
- **大小**：不超过 1GB
- **时长**：建议 15秒 - 5分钟

---

## ⚠️ 常见问题和解决方案

### 问题 1：未登录或 Cookie 过期

**症状**：提示"未登录"或操作失败

**解决**：
```bash
xhs-cli login
```
扫码重新登录

### 问题 2：标题超过长度限制

**症状**：提示"标题验证失败"

**解决**：
- 检查标题长度（中文20字，英文40字符）
- 修改标题或使用更简洁的表达

### 问题 3：图片上传失败

**症状**：提示"图片上传失败"

**原因**：
- 图片路径错误
- 图片格式不支持
- 图片大小超限
- 网络问题

**解决**：
- 检查图片路径是否正确
- 确认图片格式（JPG/PNG/GIF）
- 压缩图片到 10MB 以下
- 检查网络连接

### 问题 4：浏览器自动化失败

**症状**：提示"页面元素未找到"

**原因**：小红书页面结构变化

**解决**：
- 更新 xiaohongshu-mcp-node 到最新版本
- 报告问题到 GitHub Issues

### 问题 5：找不到命令

**症状**：`xhs-cli: command not found`

**解决**：
```bash
# 确认安装
npm list -g xiaohongshu-mcp-node-skill

# 重新安装
npm install -g xiaohongshu-mcp-node-skill

# 检查 PATH
which xhs-cli
```

---

## 🔒 安全性说明

### 敏感信息处理

- Cookie 存储在本地文件中（默认 `./cookies.json`）
- 不会上传任何数据到第三方服务器
- 所有通信仅限于小红书官方网站

### 权限要求

- 读取本地文件（图片、视频、文本）
- 网络访问（小红书网站）
- 写入 Cookie 文件
- 浏览器控制（Playwright）

### 数据隐私

- ❌ 不会收集用户信息
- ❌ 不会上传到第三方服务器
- ✅ 所有操作仅在本地执行
- ✅ Cookie 仅存储在本地

---

## 🎓 示例对话

**用户**：帮我把这篇文章发布到小红书

**AI**：好的，我来帮你发布。请提供以下信息：
1. 文章标题（最多20字）
2. 文章正文
3. 配图（至少1张）
4. 标签（可选）

**用户**：[提供内容和图片]

**AI**：收到！我将为你发布到小红书。

[执行命令]

```bash
xhs-cli publish \
  --title "Node.js 开发技巧分享" \
  --content "..." \
  --images /tmp/img1.jpg /tmp/img2.jpg \
  --tags "Node.js" "编程" "技术分享" \
  --original
```

**AI**：✅ 文章已成功发布到小红书！
- 标题：Node.js 开发技巧分享
- 图片：2 张
- 状态：发布完成

---

## 📚 参考资料

- [项目 GitHub](https://github.com/sipingme/xiaohongshu-mcp-node-skill)
- [xiaohongshu-mcp-node 核心库](https://github.com/sipingme/xiaohongshu-mcp-node)
- [快速开始指南](./references/quick-start.md)
- [常见问题 FAQ](./references/faq.md)

---

## 📝 维护说明

- **版本**: 1.0.0
- **最后更新**: 2026-03-20
- **维护者**: Ping Si <sipingme@gmail.com>
- **许可证**: Apache-2.0

---

## ✅ 首次成功检查清单

新用户应该能在 5 分钟内完成：

- [ ] 安装工具：`npm install -g xiaohongshu-mcp-node xiaohongshu-mcp-node-skill`
- [ ] 检查安装：`xhs-cli --version`
- [ ] 登录账号：`xhs-cli login`（扫码）
- [ ] 检查登录：`xhs-cli check-login`
- [ ] 测试发布：准备图片和内容，执行发布命令
- [ ] 在小红书 App 中看到发布的内容

如果以上步骤都能顺利完成，说明 Skill 已正确配置！
