# MCP 接入处理

**核心约束**：
- MCP 配置由 Agent 负责完成：检查凭据，按平台方式配置并测试连接；仅将登录、获取 Token、重启会话等无法代办的动作交给用户。
- Agent 能自动创建、写入或打开配置时，不要求用户自行找路径或重复配置；对用户只说明必要动作和最终结果。

## MCP 配置

初始化时，先检查当前平台已有的 Secret、环境变量和 MCP 配置，优先使用平台原生凭据机制；仅在平台明确支持时使用本地凭据文件 `~/.zz/ZZ_MCP_TOKEN`。
- 已有凭据：Agent 直接完成配置并测试连接。
- 缺少凭据：引导用户打开[转转开放平台](https://open.zhuanzhuan.com/mcp?copymcp=1)登录并获取 Token；获取 Token 后提供给 Agent，由 Agent 按当前平台支持的方式完成配置并测试连接。

1. **通用配置信息**：

- Server：`zz-mcp`
- Transport：Streamable HTTP
- URL：`https://mcp.zhuanzhuan.com/zai/zai-transfer`
- Header: `Authorization: Bearer <ZZ_MCP_TOKEN>`

2. **JSON 配置方式**（如workbuddy平台）

将以下配置追加到当前平台的 MCP 配置文件（不要覆盖已有的其他 `mcpServers`）：

```json
"zz-mcp": {
  "type": "streamableHttp",
  "url": "https://mcp.zhuanzhuan.com/zai/zai-transfer",
  "headers": { "Authorization": "Bearer <ZZ_MCP_TOKEN>" },
  "disabled": false
}
```

`<ZZ_MCP_TOKEN>` 是占位符；使用平台原生的环境变量、Secret引用或替换为用户真实 Token。

## 安全约束

- 不在回复、日志或文档中展示、复述或输出 Token；凭据只写入当前平台支持的安全存储位置。
