# XHS MCP Server - 使用说明

## 📦 安装

```bash
cd D:\work\xiaohongshu\xiaohongshu-mcp-node
npm install
```

## 🔐 登录

首次使用需要登录小红书：

```bash
npm run login
```

在弹出的浏览器中扫码登录，登录成功后 cookies 会自动保存到 `data/cookies.json`。

## 🚀 启动服务

```bash
npm start
```

服务地址：
- MCP 端点: `http://localhost:18060/mcp`
- 健康检查: `http://localhost:18060/health`

## 🔧 客户端接入

### MCP Inspector 测试

```bash
npx @modelcontextprotocol/inspector
# 连接到 http://localhost:18060/mcp
```

### Claude Code

```bash
claude mcp add --transport http xhs-mcp http://localhost:18060/mcp
```

### Cursor

创建 `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "xhs-mcp": {
      "url": "http://localhost:18060/mcp"
    }
  }
}
```

### VSCode

创建 `.vscode/mcp.json`:

```json
{
  "servers": {
    "xhs-mcp": {
      "url": "http://localhost:18060/mcp",
      "type": "http"
    }
  }
}
```

### OpenClaw (MCPorter)

```bash
# 添加服务
mcporter config add xhs-mcp http://localhost:18060/mcp

# 检查登录
mcporter call xhs-mcp.check_login_status

# 搜索
mcporter call xhs-mcp.search_feeds keyword="美食"

# 首页推荐
mcporter call xhs-mcp.list_feeds
```

## 📋 支持的工具

| 工具 | 说明 | MCPorter 支持 |
|------|------|---------------|
| check_login_status | 检查登录状态 | ✅ |
| get_login_qrcode | 获取登录二维码 | ✅ |
| delete_cookies | 删除登录状态 | ✅ |
| list_feeds | 获取首页推荐 | ✅ |
| search_feeds | 搜索笔记 | ✅ |
| get_feed_detail | 获取笔记详情 | ✅ |
| like_feed | 点赞/取消点赞 | ✅ |
| favorite_feed | 收藏/取消收藏 | ✅ |
| post_comment_to_feed | 发表评论 | ✅ |
| reply_comment_in_feed | 回复评论 | ✅ |
| user_profile | 获取用户主页 | ✅ |
| publish_content | 发布图文 | ❌ 需用脚本 |
| publish_with_video | 发布视频 | ❌ 需用脚本 |

## 📝 发布图文示例

由于 MCPorter 不支持数组参数，发布功能需要用 Node.js 脚本：

```javascript
// publish.js
import { publishContent } from './src/xhs-tools.js';

await publishContent({
  title: "今日美食分享",
  content: "今天做了一道超好吃的红烧肉，分享给大家～",
  images: [
    "D:/photos/food1.jpg",
    "D:/photos/food2.jpg"
  ],
  tags: ["美食", "红烧肉", "家常菜"]
});

console.log("发布成功！");
```

运行：
```bash
node publish.js
```

## ⚙️ 环境变量

```bash
# 自定义端口
XHS_PORT=8080 npm start

# 使用代理
XHS_PROXY=http://127.0.0.1:7890 npm start
```

## ⚠️ 注意事项

1. **登录限制**：同一账号不能在多个网页端登录
2. **发布限制**：每天最多 50 篇笔记
3. **标题限制**：最多 20 字
4. **正文限制**：最多 1000 字
5. **Cookie 有效期**：需要定期重新登录

## 🛠️ 故障排除

### 服务启动失败

```bash
# 检查端口是否被占用
netstat -ano | findstr 18060

# 杀掉占用进程
taskkill /PID <进程ID> /F
```

### 登录失败

```bash
# 删除旧 cookies 重新登录
rm data/cookies.json
npm run login
```

### Puppeteer 启动慢

首次运行会下载 Chromium（约 150MB），后续运行会很快。

## 📁 项目结构

```
xiaohongshu-mcp-node/
├── package.json        # 项目配置
├── README.md           # 说明文档
├── USAGE.md            # 使用说明（本文件）
├── SKILL.md            # OpenClaw 技能配置
├── src/
│   ├── index.js        # MCP 服务入口
│   ├── login.js        # 登录工具
│   ├── browser.js      # 浏览器管理
│   ├── xhs-tools.js    # 工具实现
│   └── utils.js        # 工具函数
└── data/
    └── cookies.json    # 登录状态
```

## 📄 License

MIT License
