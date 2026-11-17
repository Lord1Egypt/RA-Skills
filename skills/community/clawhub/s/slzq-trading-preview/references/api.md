# 三立智期 OpenClaw · 接口说明（索引）

根地址：`SLZQ_OPENCLAW_DOMAIN`（**不要**末尾斜杠，**不要**包含 `/mobile-api`）。

```text
API_BASE="${SLZQ_OPENCLAW_DOMAIN}/mobile-api"
```

**默认值**：`SLZQ_OPENCLAW_DOMAIN` 使用生产域名 `https://slzqapi.sxslqhsh.com`；`SLZQ_OPENCLAW_ENV` 使用 `sim`。

---

## 契约与工具定义

| 文件 | 说明 |
|------|------|
| [openapi.yaml](./openapi.yaml) | OpenAPI 3.1 根文件：`components` + `paths` 对各端点的 `$ref` 索引 |
| [openapi/paths-auth.yaml](./openapi/paths-auth.yaml) | 路径分片：首次安装登录领钥（对应 api-auth.md） |
| [openapi/paths-skill.yaml](./openapi/paths-skill.yaml) | 路径分片：健康检查、skill 版本/升级（对应 api-skill.md） |
| [openapi/paths-account.yaml](./openapi/paths-account.yaml) | 路径分片：`/me`、账户摘要（api-account.md） |
| [openapi/paths-positions-orders.yaml](./openapi/paths-positions-orders.yaml) | 路径分片：持仓、委托、成交、下单、撤单（api-positions.md、api-orders.md） |
| [openapi/paths-market.yaml](./openapi/paths-market.yaml) | 路径分片：行情快照、分时、K 线（api-market.md） |
| [openapi/paths-catalog.yaml](./openapi/paths-catalog.yaml) | 路径分片：品种/合约目录等（api-catalog.md） |
| [tools/index.json](./tools/index.json) | 声明 `mergeOrder`，将 `tools/parts/*.json` 各文件顶层数组合并为完整 tools 列表 |
| [tools/parts/skill.json](./tools/parts/skill.json) 等 | 与 HTTP 能力对应的 function 分片（主题与上表 OpenAPI 分片一致） |

---

## 统一响应结构

所有接口均返回：

```json
{
  "success": true,
  "errorCode": null,
  "errorInfo": null,
  "data": { ... }
}
```

失败时 `success=false`，`errorCode` / `errorInfo` 有值，`data` 为 `null`。

---

## Open API（`/open/v1`）鉴权

| 场景 | 请求头 |
|------|--------|
| 推荐 | `Authorization: Bearer ${SLZQ_OPENCLAW_API_KEY}` |
| 可选 | `X-Api-Key: ${SLZQ_OPENCLAW_API_KEY}` |
| 必填 | `X-Trading-Env: sim` 或 `live`（小写） |

> **无需鉴权**的接口：`GET /open/v1/health`、`GET /open/v1/skill/version`、`GET /open/v1/skill/upgrade`，以及 `/open/v1/auth/*`（首次安装登录领钥）。  
> 其余所有 `/open/v1/*` 均需通过拦截器校验密钥与交易环境。

**密钥权限档位**：`SIM`=模拟盘（仅 `sim`）、`SIM_LIVE`=模拟盘+实盘（`sim` 与 `live` 均可）。档位不匹配返回 `10412`。详见 [api-auth.md](./api-auth.md)。

---

## 按主题阅读（拆分文档）

| 文档 | 内容 |
|------|------|
| [api-auth.md](./api-auth.md) | **首次安装**：风险告知、发验证码、登录注册领取密钥；权限档位说明 |
| [api-skill.md](./api-skill.md) | 健康检查、skill 版本、升级指引 |
| [api-account.md](./api-account.md) | `/me`、账户摘要、账户历史盈亏 |
| [api-positions.md](./api-positions.md) | 持仓列表（sim / live 字段说明） |
| [api-orders.md](./api-orders.md) | 当前委托、成交、下单、撤单、`RtnOrderModel` |
| [api-market.md](./api-market.md) | 行情快照、批量快照、分时、K 线 |
| [api-catalog.md](./api-catalog.md) | 品种/合约目录、F10、热门、交易所、夜盘日历 |
| [api-examples-errors.md](./api-examples-errors.md) | curl 快速示例、常见错误码 |
| [api-app-cn.md](./api-app-cn.md) | App 登录态 `/cn/openclaw/*`（**非** Api-Key Open API） |

---

## Open API 能力索引（前缀 `/open/v1`）

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/auth/agreement` | 风险告知（无需鉴权） |
| POST | `/auth/sms/send` | 发送登录验证码（无需鉴权） |
| POST | `/auth/login` | 登录/注册并领取模拟盘密钥（无需鉴权） |
| GET | `/health` | 健康检查（无需鉴权） |
| GET | `/skill/version` | skill 版本（无需鉴权） |
| GET | `/skill/upgrade` | 升级指引（无需鉴权） |
| GET | `/me` | 当前密钥上下文与权限档位 |
| GET | `/account/summary` | 账户摘要 |
| GET | `/account/pnl/history` | 账户历史盈亏 |
| GET | `/positions` | 持仓列表 |
| GET | `/orders/open` | 当前委托 |
| GET | `/trades` | 成交列表 |
| POST | `/orders` | 下单 |
| POST | `/orders/cancel` | 撤单 |
| GET | `/market/snapshot` | 单合约行情快照 |
| GET | `/market/snapshots` | 批量行情快照 |
| GET | `/market/tick` | 分时 |
| GET | `/market/kline` | K 线 |
| GET | `/catalog/goods` | 品种与主力分页 |
| GET | `/catalog/goods/detail` | 品种详情 |
| GET | `/catalog/contract` | 合约详情 |
| GET | `/catalog/contract/f10` | 合约 F10 |
| GET | `/catalog/hot` | 热门合约 TOP10 |
| GET | `/catalog/exchanges` | 交易所列表 |
| GET | `/catalog/session/night-today` | 当晚是否有夜盘 |

**详细字段、示例与 curl** 见上表对应分文档。
