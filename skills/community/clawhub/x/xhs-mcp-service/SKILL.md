---
name: xhs-mcp-server
description: |
  小红书（XHS/RED）MCP 服务。通过本地 xhs-mcp-server 服务提供完整的小红书操作能力。
  当用户提到小红书、红书、XHS、RED、发笔记、搜笔记、小红书运营等任何与小红书相关的操作时使用此技能。

  ⚠️ 前置条件：需要先启动 xhs-mcp-server 服务（默认 http://localhost:18060/mcp）
---

你是小红书操作助手，帮助用户通过 MCP 协议操作小红书。

## 🔧 部署要求

**必须先完成以下步骤：**

1. **进入项目目录**
   ```bash
   cd D:\work\xiaohongshu\xiaohongshu-mcp-node
   ```

2. **安装依赖**
   ```bash
   npm install
   ```

3. **首次登录小红书**
   ```bash
   npm run login
   ```
   在弹出的浏览器中扫码登录，登录成功后 cookies 会自动保存。

4. **启动 MCP 服务**
   ```bash
   npm start
   ```
   服务将运行在 http://localhost:18060/mcp

## 📋 功能列表（13个工具）

| 工具 | 说明 | 参数 |
|------|------|------|
| `check_login_status` | 检查登录状态 | 无 |
| `get_login_qrcode` | 获取登录二维码 | 无 |
| `delete_cookies` | 删除登录状态 | 无 |
| `list_feeds` | 获取首页推荐 | 无 |
| `search_feeds` | 搜索笔记 | `keyword`, `filters?` |
| `get_feed_detail` | 获取笔记详情 | `feed_id`, `xsec_token` |
| `like_feed` | 点赞/取消点赞 | `feed_id`, `xsec_token`, `unlike?` |
| `favorite_feed` | 收藏/取消收藏 | `feed_id`, `xsec_token`, `unfavorite?` |
| `post_comment_to_feed` | 发表评论 | `feed_id`, `xsec_token`, `content` |
| `reply_comment_in_feed` | 回复评论 | `feed_id`, `xsec_token`, `content`, `comment_id?`, `user_id?` |
| `user_profile` | 获取用户主页 | `user_id`, `xsec_token` |
| `publish_content` | 发布图文 | `title`, `content`, `images`, `tags?` |
| `publish_with_video` | 发布视频 | `title`, `content`, `video`, `tags?` |

## 🔧 通过 MCPorter 调用

如果 OpenClaw 已配置 MCPorter，可以这样调用：

```bash
# 添加 MCP 服务
mcporter config add xhs-mcp http://localhost:18060/mcp

# 检查登录状态
mcporter call xhs-mcp.check_login_status

# 搜索笔记
mcporter call xhs-mcp.search_feeds keyword="美食"

# 获取首页推荐
mcporter call xhs-mcp.list_feeds

# 点赞（需要 feed_id 和 xsec_token）
mcporter call xhs-mcp.like_feed feed_id="xxx" xsec_token="xxx"
```

## ⚠️ MCPorter 限制

MCPorter 在 Windows 命令行下**无法传递数组参数**，因此：

- ✅ **简单参数功能**：可用 MCPorter（搜索、点赞、收藏、评论等）
- ❌ **数组参数功能**：需要用 Node.js 脚本（发布图文、发布视频）

## 📝 发布图文/视频

由于 MCPorter 不支持数组参数，发布功能需要用 Node.js 脚本：

```javascript
// 创建发布脚本 publish.js
import { publishContent } from './src/xhs-tools.js';

await publishContent({
  title: "标题（最多20字）",
  content: "正文内容（最多1000字）",
  images: ["图片1.jpg", "图片2.jpg"],
  tags: ["标签1", "标签2"]
});
```

运行：
```bash
node publish.js
```

## 🎯 使用场景

### 场景1：检查登录状态

```
用户：帮我检查小红书登录状态
→ mcporter call xhs-mcp.check_login_status
```

### 场景2：搜索笔记

```
用户：搜索小红书上关于咖啡的内容
→ mcporter call xhs-mcp.search_feeds keyword="咖啡"
```

### 场景3：点赞收藏

```
用户：帮我点赞搜索结果的第一篇
→ 1. 搜索获取 feed_id 和 xsec_token
→ 2. mcporter call xhs-mcp.like_feed feed_id=xxx xsec_token=xxx
```

### 场景4：发布笔记

```
用户：帮我发布一篇小红书笔记
→ 需要用 Node.js 脚本（MCPorter 不支持数组参数）
→ node publish.js
```

## 📁 项目文件位置

- **项目目录**: `D:\work\xiaohongshu\xiaohongshu-mcp-node\`
- **主程序**: `src/index.js`
- **登录工具**: `src/login.js`
- **工具实现**: `src/xhs-tools.js`
- **浏览器管理**: `src/browser.js`
- **Cookies 存储**: `data/cookies.json`

## 🔧 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `XHS_PORT` | 服务端口 | `18060` |
| `XHS_HOST` | 绑定地址 | `0.0.0.0` |
| `XHS_PROXY` | 代理地址 | - |

使用代理启动：
```bash
XHS_PROXY=http://proxy:port npm start
```

## ⚠️ 重要注意事项

1. **账号安全**：同一账号不能在多个网页端登录，会互相踢出
2. **发布限制**：每天最多 50 篇笔记
3. **标题限制**：最多 20 字
4. **正文限制**：最多 1000 字
5. **Cookie 有效期**：Cookie 可能过期，需要定期重新登录

## 💡 最佳实践

1. **简单操作用 MCPorter**：搜索、点赞、收藏、评论
2. **复杂操作用 Node.js**：发布图文、发布视频、批量操作
3. **定时发布**：结合 cron 技能定时调用发布脚本
4. **错误处理**：如果操作失败，先检查登录状态

## 🔗 相关资源

- MCP 协议: https://modelcontextprotocol.io/
- MCP Inspector: `npx @modelcontextprotocol/inspector`
