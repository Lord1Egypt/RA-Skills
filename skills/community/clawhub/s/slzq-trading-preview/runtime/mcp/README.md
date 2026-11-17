# slzq-trading-mcp

将三立智期 **Open API**（`SLZQ_OPENCLAW_DOMAIN` + `/mobile-api/open/v1`）以 **MCP（stdio）** 暴露给 Claude Desktop、Cursor、OpenClaw 等客户端。工具名前缀 `slzq_open_v1_*`，与 HTTP 路径一一对应。

本包仅识别 **`SLZQ_OPENCLAW_*`** 环境变量；配置名须与随包根目录 `SKILL.md` 一致。本目录就是 skill 包内的 `runtime/mcp/`，**不是**独立的 `slzq-trading-mcp/` zip。

## 前置条件

- **Node.js** ≥ 18（macOS / Linux / Windows 官方安装包均可）
- 与 slzq-trading skill 相同的三个环境变量（见下）

## 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| `SLZQ_OPENCLAW_DOMAIN` | 否 | 仅 `https://` + 主机名，**不要**带 `/mobile-api`；默认生产域名 |
| `SLZQ_OPENCLAW_API_KEY` | 否 | Api Key；**留空也能启动**，可在会话中用登录工具现场领取（见下） |
| `SLZQ_OPENCLAW_ENV` | 否 | `sim` 或 `live`（小写），默认 `sim` |

除 `GET /open/v1/health`、`/skill/version`、`/skill/upgrade`、`/auth/*` 对应的工具外，其余工具在调用时会自动带 `Authorization: Bearer …` 与 `X-Trading-Env`。

## 首次安装：没有 API Key 时怎么办

不必先去 App 生成密钥。直接让智能体按顺序调用这 4 个工具即可：

| 工具 | 作用 |
|------|------|
| `slzq_open_v1_auth_status` | 查看本机是否已配置密钥、密钥来源与权限档位 |
| `slzq_open_v1_auth_agreement` | 取回风险告知，**必须原文展示给用户**并取得同意 |
| `slzq_open_v1_auth_send_code` | 向用户手机号发送验证码（同号 1 分钟 1 条） |
| `slzq_open_v1_auth_login` | 手机号 + 验证码登录/注册，领取**模拟盘**密钥 |

登录成功后：

- 密钥写入 `~/.slzq-trading/credentials.json`（权限 `0600`），本机装了 OpenClaw 时同时合并进 `~/.openclaw/openclaw.json` 的 `skills.entries.slzq-trading`；
- **当前会话立即生效**，无需重启客户端；
- 工具返回内容只含脱敏密钥，不会把明文回给模型。

若已显式设置了 `SLZQ_OPENCLAW_API_KEY` 环境变量，它的优先级高于凭据文件——重新登录后请一并更新该环境变量，否则重启会退回旧密钥（工具返回里会提示这一点）。

## 密钥权限档位

| 档位 | 含义 | 可用 `X-Trading-Env` |
|------|------|----------------------|
| `SIM` | 模拟盘 | `sim` |
| `SIM_LIVE` | 模拟盘 + 实盘 | `sim`、`live` |

`slzq_open_v1_me` / `slzq_open_v1_auth_status` 会返回 `scope`、`canTradeLive` 与 `liveUpgradeSteps`。**实盘档位只能在 App 内开通**（签署实盘风险告知 + 校验 CTP 交易密码），本 MCP 的登录工具只签发模拟盘密钥。

## 本地构建

```bash
cd runtime/mcp
npm ci
```

`dist/index.js` 已随包预编译；改源码后才需要 `npm run build`。入口：`dist/index.js`（`package.json` 的 `bin` 为 `slzq-trading-mcp`）。

## 多平台 MCP 注入示例

以下将 `COMMAND` 设为 **`node`**，`ARGS` 设为 **skill 安装目录下的 `runtime/mcp/dist/index.js` 绝对路径**。

### macOS · Claude Desktop

配置文件：

`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "slzq-trading": {
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/slzq-trading/runtime/mcp/dist/index.js"],
      "env": {
        "SLZQ_OPENCLAW_DOMAIN": "https://slzqapi.sxslqhsh.com",
        "SLZQ_OPENCLAW_API_KEY": "oc.your.key.here",
        "SLZQ_OPENCLAW_ENV": "sim"
      }
    }
  }
}
```

修改后**完全退出并重启** Claude Desktop。

### Linux · Claude Desktop

配置文件常见路径：

`~/.config/Claude/claude_desktop_config.json`

（JSON 结构同上。）

### Windows · Claude Desktop

配置文件：

`%APPDATA%\Claude\claude_desktop_config.json`

注意 JSON 中对反斜杠转义：`C:\\Users\\you\\...\\dist\\index.js`，或使用正斜杠 `C:/Users/you/.../dist/index.js`。

### Cursor

在用户级 MCP 配置中加入与上相同的 `mcpServers.slzq-trading` 块（具体文件名依 Cursor 版本可能为 `.cursor/mcp.json` 或设置 UI 中的 MCP 项）。

### OpenClaw

若网关支持注册外部 MCP（stdio），将 `command` / `args` / `env` 与上表一致即可；**键名以 OpenClaw 官方文档为准**。环境变量可与 skill 条目中的 `SLZQ_OPENCLAW_*` 保持一致。

## 接口文档

HTTP 字段与示例见 skill 包内拆分文档（与仓库 `references/` 同步）：

- 索引：[references/api.md](../../references/api.md)
- 下单/撤单：[references/api-orders.md](../../references/api-orders.md)

## 冒烟检查（可选）

不启动 MCP，仅验证域名可达：

```bash
npm run verify:http
```

（使用 `SLZQ_OPENCLAW_DOMAIN`，默认生产域名请求 `/open/v1/health`。）

验证 MCP 工具是否注册成功：

```bash
npm run test:mcp-tools
```

通过时应看到核心工具：`slzq_open_v1_auth_status`、`slzq_open_v1_auth_login`、`slzq_open_v1_health`、`slzq_open_v1_me`、`slzq_open_v1_catalog_hot`、`slzq_open_v1_market_snapshot`、`slzq_open_v1_positions`、`slzq_open_v1_orders_place`、`slzq_open_v1_orders_cancel`。

验证首次安装引导链路（离线，使用临时 HOME 与本地假后端，不触碰真实配置、不发外网请求）：

```bash
npm run test:auth-flow
```

## 安全

- 勿将 Api Key 提交到仓库或公开配置；`~/.slzq-trading/credentials.json` 权限为 `0600`，请勿放宽。
- 勿在会话、日志中复述密钥明文；所有工具返回的均为脱敏值。
- **未经用户明确要求**，勿对 `live` 自动下单/撤单（工具 `slzq_open_v1_orders_place` / `slzq_open_v1_orders_cancel`）。
- 登录工具只签发模拟盘密钥；实盘权限必须由用户本人在 App 内校验 CTP 交易密码后开通。
