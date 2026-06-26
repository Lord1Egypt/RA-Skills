# 快速开始

本指南帮助你在 5 分钟内开始使用 toutiao-mcp-skill。

## 前置条件

- Node.js >= 18.0.0
- OpenClaw 已安装并配置

## 安装步骤

### 1. 安装 MCP Server

```bash
npm install -g toutiao-mcp
npx playwright install chromium
```

### 2. 配置 OpenClaw

编辑 OpenClaw 的 MCP 配置文件，添加：

```json
{
  "mcpServers": {
    "toutiao": {
      "command": "node",
      "args": ["/usr/local/lib/node_modules/toutiao-mcp/dist/index.js"],
      "env": {
        "PLAYWRIGHT_HEADLESS": "true",
        "COOKIES_FILE": "~/.openclaw/data/toutiao-cookies.json",
        "DATA_DIR": "~/.openclaw/data"
      }
    }
  }
}
```

### 3. 首次登录

在 OpenClaw 对话中：

```
你: 帮我登录今日头条

AI: [调用 login_with_credentials]
    浏览器窗口已打开，请完成登录
```

在打开的浏览器中完成登录（扫码或账号密码）。

### 4. 验证登录

```
你: 检查今日头条登录状态

AI: [调用 check_login_status]
    ✅ 已登录
```

### 5. 发布第一篇文章

```
你: 帮我发布一篇今日头条文章
    标题：我的第一篇文章
    内容：这是我使用 toutiao-mcp 发布的第一篇文章！

AI: [调用 publish_article]
    ✅ 文章发布成功！
    文章ID: 7123456789
```

## 下一步

- 查看 [SKILL.md](../SKILL.md) 了解所有功能
- 查看 [FAQ](./faq.md) 了解常见问题
- 查看 [troubleshooting.md](./troubleshooting.md) 解决问题

## 常用命令

```bash
# 检查登录
你: 检查今日头条登录状态

# 发布文章
你: 发布文章到今日头条，标题是"xxx"，内容是"xxx"

# 发布微头条
你: 发布微头条："今天学习了 TypeScript"

# 批量发布
你: 把这些小红书数据发布到今日头条
```

## 获取帮助

- GitHub Issues: https://github.com/sipingme/toutiao-mcp-skill/issues
- Email: sipingme@gmail.com
