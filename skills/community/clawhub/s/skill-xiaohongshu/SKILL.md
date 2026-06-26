---
name: skill-xhs-mcp-service
description: |
  小红书（XHS/RED）自动化助手。完整的小红书操作能力，包含 MCP 服务端。
  当用户提到小红书、红书、XHS、RED、发笔记、搜笔记、小红书运营等任何与小红书相关的操作时使用此技能。
---

# 小红书 MCP 技能

完整的小红书自动化技能，包含独立服务端，开箱即用。

## 快速开始

**首次使用：**

```bash
cd <技能目录>
npm install
npm run login  # 扫码登录
```

**日常使用：** 技能会自动启动服务，无需手动操作。

## 功能列表（13个工具）

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
| `reply_comment_in_feed` | 回复评论 | `feed_id`, `xsec_token`, `content`, `comment_id?` |
| `user_profile` | 获取用户主页 | `user_id`, `xsec_token` |
| `publish_content` | 发布图文 | `title`, `content`, `images`, `tags?` |
| `publish_with_video` | 发布视频 | `title`, `content`, `video`, `tags?` |

## 使用方式

### 方式1：Node.js 直接调用（推荐）

```javascript
import { searchFeeds, likeFeed, publishContent } from './scripts/xhs-tools.js';

// 搜索笔记
const results = await searchFeeds('咖啡');

// 点赞
if (results.feeds[0]) {
  await likeFeed(results.feeds[0].id, results.feeds[0].xsec_token);
}

// 发布图文
await publishContent({
  title: '我的笔记',
  content: '正文内容',
  images: ['./photo1.jpg'],
  tags: ['美食']
});
```

### 方式2：MCP 服务调用

服务默认运行在 http://localhost:18060/mcp

```bash
# 启动服务（通常自动启动）
npm start

# 通过 MCP Inspector 调试
npx @modelcontextprotocol/inspector http://localhost:18060/mcp
```

### 方式3：命令行快速操作

```bash
# 检查登录
node -e "import('./scripts/xhs-tools.js').then(m => m.checkLoginStatus()).then(console.log)"

# 搜索
node -e "import('./scripts/xhs-tools.js').then(m => m.searchFeeds('美食')).then(r => console.log(r.feeds.length))"
```

## 服务管理

**检查服务状态：**
```bash
node scripts/ensure-service.js status
```

**启动服务：**
```bash
node scripts/ensure-service.js start
```

**停止服务：**
```bash
node scripts/ensure-service.js stop
```

## 详细文档

- [API 文档](references/api.md) - 完整的 API 参考和示例

## 注意事项

1. **账号安全**：同一账号不能在多个网页端登录
2. **发布限制**：每天最多 50 篇笔记
3. **标题限制**：最多 20 字
4. **正文限制**：最多 1000 字
5. **Cookie 有效期**：建议每周重新登录一次

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `XHS_PORT` | 服务端口 | `18060` |
| `XHS_HOST` | 绑定地址 | `0.0.0.0` |
| `XHS_PROXY` | 代理地址 | - |

使用代理：
```bash
XHS_PROXY=http://proxy:port npm start
```
