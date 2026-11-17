# 代购 MCP — 接入指南

服务名：**代购服务**（客户端中建议命名为 `purchasing-mcp`）。

**免责声明：**代购服务仅供学习测试使用，请勿使用本服务及提供的信息从事违法活动，否则一经发现，后果自负，本站将配合相关部门打击。

## 连接信息

| 项 | 值 |
|---|---|
| MCP URL | `https://mcp.137449244.xyz/mcp` |
| 健康检查 | `https://mcp.137449244.xyz/health` |

连接成功后，在对话中说「逛逛商店」即可开始；未登录时会提示提供手机号或邮箱与密码。

## Cursor

`~/.cursor/mcp.json` 或项目 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "purchasing-mcp": {
      "url": "https://mcp.137449244.xyz/mcp"
    }
  }
}
```

保存后重启 Cursor，或在 Settings → MCP 中刷新。

## Claude Desktop / Claude Code

macOS 配置文件：`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "purchasing-mcp": {
      "url": "https://mcp.137449244.xyz/mcp"
    }
  }
}
```

## 其他 MCP 客户端

Cline、Roo Code、Continue、Windsurf、Codex 等：添加 **HTTP / Streamable HTTP** 类型 MCP，URL 填：

```
https://mcp.137449244.xyz/mcp
```

## 验证

1. 访问健康检查地址，应返回 `"status":"ok"`。
2. AI 客户端中 MCP 显示已连接。
3. 对话中输入「逛逛商店」，应出现店铺列表或登录提示。

## 常见问题

| 问题 | 处理 |
|------|------|
| 连接失败 / 502 | 稍后重试；确认 URL 以 `/mcp` 结尾且网络可访问 HTTPS |
| 工具列表为空 | 重启 AI 客户端；检查 JSON 语法 |
| 登录后无商品 | 换一家店铺或分类再试 |
| 能连上但无法下单 | 确认已按提示完成「我同意不退款协议」打字确认与 USDT 网络选择 |

## 不提供的内容

本接入指南**不包含**也请勿向终端用户索取：管理后台、服务器凭证、货源信息、环境配置或源码部署方式。购物问题请直接在已连接 MCP 的对话中完成。
