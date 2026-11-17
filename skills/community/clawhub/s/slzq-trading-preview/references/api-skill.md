# Open API · 健康检查与 skill 版本

> 根地址、`API_BASE`、统一响应与鉴权见 [api.md](./api.md)。

### 1. 健康检查 + 能力探测

```
GET /open/v1/health
```

无需鉴权，**新老版本服务端都可调用**，是判断服务端能力的唯一权威入口。

**响应 `data`：**

```json
{
  "status": "ok",
  "authLoginSupported": true,
  "skillName": "slzq-trading",
  "skillVersion": "1.1.0",
  "apiBase": "/mobile-api"
}
```

| 字段 | 说明 |
|------|------|
| `authLoginSupported` | `true` 才表示服务端支持「免 API Key 手机号验证码登录领钥」。**字段缺失 = 服务端版本过旧**，此时 `/open/v1/auth/*` 会返回 `10411`，那是旧版拦截器拦下不存在路由的假象，不要据此去补密钥 |
| `skillName` | 服务端配置 `openclaw.config.skill-name`。与本地包名不一致说明该实例跑的是另一套品牌配置，其版本号不能用来判断本地包是否要升级 |
| `skillVersion` | 服务端部署的技能包版本 |
| `apiBase` | 服务端实际生效的路径前缀（生产为 `/mobile-api`），用来核对基址是否拼对 |

---

### 2. skill 版本检查

```
GET /open/v1/skill/version?clientVersion=1.1.0
```

无需鉴权。`clientVersion` 可选（如 `1.1.0`），传入后与最新版做 semver 比较。

**响应 `data`：**

```json
{
  "latestVersion": "1.2.0",
  "updateAvailable": true,
  "zipPath": "/mobile-api/static/openclaw/slzq-trading.zip",
  "clawhubSuggestedCommand": "clawhub install slzq-trading",
  "upgradeSteps": [
    "1. 运行：clawhub install slzq-trading",
    "2. 重启 Claude Desktop / 你的 MCP 客户端",
    "3. 确认 skill 版本已更新"
  ]
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `latestVersion` | string | 最新版本号 |
| `updateAvailable` | boolean | 是否有新版本（clientVersion < latestVersion 时为 true；未传 clientVersion 时始终为 false） |
| `zipPath` | string | 自托管 zip 下载路径（相对于 API_BASE） |
| `clawhubSuggestedCommand` | string | ClawHub 一键安装命令 |
| `upgradeSteps` | string[] | 升级步骤描述 |

---

### 3. skill 升级指引

```
GET /open/v1/skill/upgrade
```

无需鉴权。返回 ClawHub 与自托管 zip 的分步升级说明。

**响应 `data`：**

```json
{
  "latestVersion": "1.2.0",
  "clawhubSteps": [
    "1. 运行：clawhub install slzq-trading",
    "2. 重启 Claude Desktop / 你的 MCP 客户端"
  ],
  "selfHostedSteps": [
    "1. 下载 zip：${API_BASE}/static/openclaw/slzq-trading.zip",
    "2. 解压覆盖原 skill 目录",
    "3. 重启 Claude Desktop / 你的 MCP 客户端"
  ]
}
```

