# App 登录态接口（非 Open API）

> 根地址、`API_BASE` 约定见 [api.md](./api.md)。此类接口需 App 登录态，**不是** Api-Key Open API。

## 四、App 登录态接口（`/cn/openclaw/*`）

> 这些接口用于 App 内管理 OpenClaw 密钥与协议，**不是** OpenClaw Agent 调用的 Open API。

| 说明 | 方法 | 路径 |
|------|------|------|
| 是否展示 OpenClaw 入口 | GET | `/cn/openclaw/status` |
| 协议状态 | GET | `/cn/openclaw/agreement/status` |
| 同意协议 | POST | `/cn/openclaw/agreement/accept` |
| 凭据与关联账号 | GET | `/cn/openclaw/ctp-credential/status` |
| 密钥列表 | GET | `/cn/openclaw/api-keys` |
| 创建密钥 | POST | `/cn/openclaw/api-keys` |
| 吊销密钥 | POST | `/cn/openclaw/api-keys/{id}/revoke` |

**创建密钥请求体：**

```json
{
  "name": "我的策略密钥",
  "allowLive": false
}
```

开通实盘时额外加 `"ctpTradingPassword": "交易密码"`。

**密钥列表返回的档位字段：**

| 字段 | 说明 |
|------|------|
| `scope` | `SIM`=模拟盘；`SIM_LIVE`=模拟盘+实盘 |
| `scopeName` | 档位中文名，可直接展示 |
| `allowSim` / `allowLive` | 库表原始开关，保留兼容；展示请优先用 `scope` |

同一用户最多同时持有两条有效密钥：模拟盘一条、实盘一条。实盘密钥同时可用于 `sim` 环境。

> 若用户尚未登录 App，也可以通过 skill 侧的 `/open/v1/auth/*` 流程用手机号验证码注册并领取模拟盘密钥，见 [api-auth.md](./api-auth.md)。
