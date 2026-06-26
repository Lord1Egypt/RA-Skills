# sip-wine-food

面向智能体宿主：**访问门店酒菜数据时，统一只使用网关 `https://mcp.sipsiip.com/api`**，默认 MCP 会话 URL 为 **`https://mcp.sipsiip.com/api/sippai`**。能力与数据由 **单仓后端 `api/sippai`** 提供，经 MCP 对外暴露。**不要**在 skill 或面向用户的配置里再写其它对外业务域名或未走 MCP 的 REST 入口。

## 接入约定

- **唯一对外网关前缀**：`https://mcp.sipsiip.com/api`
- **本 skill MCP 入口**：`https://mcp.sipsiip.com/api/sippai`（与网关常见挂载 `MCP_HTTP_MOUNT_PATH=/api/sippai` 一致）
- **业务能力所在**：后端工程 **`api/sippai`**（门店检索集成接口、门店酒单与菜式等）。
- **禁止**：自选其它业务域名或未经上述 MCP 的 HTTP 去拿同一批数据（详见 `SKILL.md`）。

## 远程宿主（推荐）

在 Cursor / SkillHub / 其它支持 Streamable HTTP MCP 的宿主中，将 MCP 服务端配置为 **`https://mcp.sipsiip.com/api/sippai`**（认证与负载策略以服务交付文档为准）。不要在宿主 UI 里填写第二个「数据来源」URL。

## 本地开发（不作为对外入口）

本机 MCP **stdin/stdout** 子进程仅用于联调：在安装依赖并完成构建的前提下启动网关脚本，并为本机网关进程配置可访问 Sippai 后端的 **`SIPPAI_BASE_URL`**、以及 **`api/sippai`** 中与集成/MCP 一致的 **`SIPPAI_MCP_API_KEY` / `SIPPAI_MCP_API_KEYS`**。启动命令与工作目录 **以单仓实际布局为准**。**勿**将本地地址写入面向用户的「官方数据入口」。

```json
"mcp": {
  "command": "node",
  "args": ["--import", "tsx", "<单仓 MCP 网关入口脚本，以服务仓库为准>"],
  "cwd": "${WORKSPACE}",
  "env": {
    "MCP_TRANSPORT": "stdio",
    "SIPPAI_MCP_API_KEY": "与后端 SIPPAI_MCP_API_KEYS 对齐"
  }
}
```

## 文件说明

| 文件 | 用途 |
|------|------|
| `SKILL.md` | 行为规范、网关说明与 **`api/sippai` 业务能力** |
| `skill.json` | 元数据；含 `public_gateway_base` / `public_mcp_url` |
| `_meta.json` | 扩展元数据 |

## License

沿用单仓顶层仓库策略（若未定，默认 MIT）。

## ClawHub / 其它市场上架备忘

上架前建议你本地跑官方提供的校验命令（若有，例如 OpenClaw 生态中的 `validate`/`publish`，以 ClawHub 当前文档为准）。发布包内请**勿**写入真实密钥、Token、手机号或仅能内网访问的 URL；密钥仅能通过宿主环境变量或用户侧安全配置注入。

以下为常见检查项：

| 项 | 说明 |
|----|------|
| YAML | `SKILL.md` 顶栏含 **`name`、`version`、`description`**；并已附 **≥1 段使用示例**。 |
| 描述 | **中英可读**，便于市集检索与用户理解「何时用 / 怎么用」。 |
| 安全 | 无硬编码密钥；`skill.json` 中 `env` 仅说明变量名语义。 |
| 协议 | **`license`** 与仓库策略一致（本 skill 写明 MIT）。 |
| 唯一名 | **`sip-wine-food`** 在目标平台上未被占用（若占用需更名或加后缀）。 |

更完整的对外说明与人类可读入口：**https://sipsiip.com/ai/getwinefood**，静态可复制文件见同目录 **`skill.json` / `_meta.json`**。
