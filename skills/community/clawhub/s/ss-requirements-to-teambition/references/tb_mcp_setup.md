# TB MCP 配置指南

## 1. 获取 User Token

打开 https://open.teambition.com/user-mcp ，登录后页面会显示你的 User Token，格式类似：

```
u-W8ASWDui25gI8KqHFKpo8VMzfxnkIVh3Tsyx7aE3UYTzzt8y
```

复制这个 Token。

## 2. 安装 CLI 工具

```bash
npm install -g teambition-openapi-mcp
```

## 3. 配置 OpenClaw MCP

在 `~/.openclaw/openclaw.json` 的 `mcp.servers` 中添加：

```json
{
  "mcp": {
    "servers": {
      "teambition-mcp": {
        "command": "teambition-openapi-mcp",
        "args": ["user-mcp", "-u", "你的UserToken"]
      }
    }
  }
}
```

> 如果 npm global bin 不在 PATH 中，用完整路径：`/home/你的用户名/.npm-global/bin/teambition-openapi-mcp`

## 4. 重启 Gateway

```bash
openclaw gateway restart
```

## 5. 验证

重启后对 AI 说「帮我查一下 TB 项目列表」，如果 AI 能调用 `teambition-mcp__listUserProjectsV3` 就说明配置成功。

## 可用的 MCP 工具

配置完成后，AI 可以调用以下工具（skill 主要用到 `createTaskV3`）：

| 工具 | 用途 |
|------|------|
| `createTaskV3` | 创建任务 |
| `searchProjectTasksV3` | 搜索项目任务 |
| `queryTaskV3` | 查询任务详情 |
| `updateTaskStatusV3` | 更新任务状态 |
| `updateTaskNoteV3` | 更新任务备注 |
| `updateTaskCusomFieldV3` | 更新自定义字段 |
| `listUserProjectsV3` | 列出用户参与的项目 |