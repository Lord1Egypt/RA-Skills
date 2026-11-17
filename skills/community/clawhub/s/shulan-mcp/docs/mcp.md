# MCP Server 接入 / MCP Integration

数懒 MCP Server 把数据中台 REST API 包装为 MCP 工具，供 Claude Code、Cursor、ChatGPT Actions 等客户端调用。

## 环境变量 / Environment

| 变量 | 必填 | 说明 |
|---|---|---|
| `SHULAN_API_KEY` | 是 | 在 https://shulan.io 登录后于「开放平台」生成（`sl_` 前缀） |
| `SHULAN_BASE_URL` | 否 | 默认 `http://127.0.0.1:8790`；使用托管服务填 `https://shulan.io` |

## 工具列表 / Tools

- `shulan_health` — 服务状态检查
- `shulan_create_task` — 创建数据调研任务（自动扣费，多退少不补）
- `shulan_get_task` — 查询任务状态与报告
- `shulan_market` — 查询报告市集
- `shulan_get_report` — 获取报告详情

## Claude Code 配置示例

`~/.claude/mcp.json`：

```json
{
  "mcpServers": {
    "shulan": {
      "command": "node",
      "args": ["/path/to/mcp-server/server.js"],
      "env": {
        "SHULAN_API_KEY": "sl_你的密钥",
        "SHULAN_BASE_URL": "https://shulan.io"
      }
    }
  }
}
```

## 直接启动

```bash
cd mcp-server
npm install
SHULAN_API_KEY=sl_你的密钥 SHULAN_BASE_URL=https://shulan.io node server.js
```

也可以直接从 npm 安装（已发布为 `shulan-mcp`）：

```bash
npm install -g shulan-mcp
SHULAN_API_KEY=sl_你的密钥 SHULAN_BASE_URL=https://shulan.io shulan-mcp
```
