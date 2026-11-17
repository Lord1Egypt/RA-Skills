# Open API · 首次安装登录领钥与权限档位

> 根地址、`API_BASE`、统一响应结构见 [api.md](./api.md)。
> 本页三个接口 **均无需 Api Key**——它们正是给「还没有密钥」的用户用的。

## 什么时候走这套流程

- 任何需要鉴权的接口返回 `errorCode=10411`（密钥无效或未配置）；
- 或本地根本没有配置 `SLZQ_OPENCLAW_API_KEY`。

本页描述的是**方式 A（会话内登录领取）**。还有一条并列的**方式 B**：让用户在 App「我的 → 期货辅助交易」的有效密钥列表里一键复制已有密钥粘贴过来——**要用实盘（`SIM_LIVE`）密钥时只能走方式 B**。两种方式都要摆给用户选，不要只给其中一种。

顺序固定为：**取风险告知 → 展示并取得同意 → 发验证码 → 登录领钥**。中间不要跳步。

**方式 A 不会顶掉已有密钥**：登录时服务端先查该账号有没有可用的模拟盘密钥，**有就原样返回那把**（`keyCreated=false`），没有才自动签发（`keyCreated=true`）。因此两种方式拿到的通常是同一把钥匙。

**全程只需要用户提供两样东西：手机号、验证码。** `codeKey` 由服务端按手机号暂存，登录时自动取回，你不需要保存或回传；`agreementVersion` 取自第一步的响应。

## 开工前：先确认服务端支持（必读）

```
GET /open/v1/health        # 免鉴权，新老版本都可调
```

返回 `data.authLoginSupported === true` 才说明本服务端**已上线**本页接口。同时会返回 `skillName`、`skillVersion`、`apiBase`（服务端实际生效的路径前缀，用来核对基址）。

**没有 `authLoginSupported` 字段 ⇒ 该地址上的服务端尚未上线本页接口**。此时直接打 `/open/v1/auth/*` 会得到 `10411「缺少 API Key」`——那是**旧版鉴权拦截器拦下了不存在的路由**（拦截器排在路由匹配之前，对任何 `/open/v1/*` 未知路径都会先报缺 Key），**不是**真的要你补密钥。

遇到这种情况的正确处理：本包只对接生产 `https://slzqapi.sxslqhsh.com`。没有 `authLoginSupported` 时方式 A 不可用，改走方式 B：请用户在 App「我的 → 期货辅助交易」复制已有密钥，或在该页面新建一把。**不要改域名，不要自己枚举地址。**

> 使用 MCP 时无需自己判断：`slzq_open_v1_auth_status` 已经把上述探测封装好，直接读它返回的 `verdict`（`READY` / `NEED_LOGIN` / `SERVER_TOO_OLD` / `KEY_REJECTED` / `NETWORK_ERROR`）。
> **没有注册 MCP 也照样能走完本页流程**：这三个接口全部免鉴权，直接发 HTTP 即可，不要因为缺工具就把方式 A 从选项里划掉、只剩方式 B。

> 本页所有 JSON 都是**契约示例**，不是实测数据。判断服务端行为只能依据工具/接口的真实返回。

---

### 1. 风险告知

```
GET /open/v1/auth/agreement
```

**响应 `data`：**

```json
{
  "version": "sim-risk-1",
  "title": "模拟盘小龙虾风险告知",
  "highlights": [
    "本 skill 领取的密钥仅可用于模拟盘（sim）：行情真实、资金与撮合为模拟，盈亏不代表实盘结果。",
    "智能体可代为下单、撤单，请在每次交易指令前自行确认合约、方向、手数与价格。",
    "API Key 等同于账号的交易凭证，请勿粘贴到公开渠道、日志或代码仓库；泄露后请在 App 内立即吊销。",
    "实盘（live）权限不通过本流程开通，须在 App 内签署实盘风险告知并校验 CTP 交易密码。"
  ],
  "agreementUrl": "https://slzqapi.sxslqhsh.com/mobile-api/static/page/openclaw-agreement",
  "acceptField": "agreementVersion",
  "nextStep": "请把以上要点原文展示给用户……"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 风险告知版本号，登录时作为 `agreementVersion` 原样回传 |
| `highlights` | string[] | **必须原文展示给用户**的要点，不要压缩或改写 |
| `agreementUrl` | string | 协议全文地址，用户要求细读时给出 |

用户已在 App 内同意过协议或模拟盘风险告知时，登录接口不再强制 `agreementVersion`；但首次使用仍应展示要点。

---

### 2. 发送验证码

```
POST /open/v1/auth/sms/send
Content-Type: application/json

{ "mobileNum": "13800000000" }
```

**响应 `data`：**

```json
{
  "codeKey": "9f3c...",
  "maskedMobileNum": "138****0000",
  "expireMinutes": 15,
  "codeLength": 4,
  "nextStep": "请让用户查收短信并读出验证码……"
}
```

| 字段 | 说明 |
|------|------|
| `codeKey` | 验证码句柄。**服务端已按手机号暂存，登录时不用回传**，也不必自己保存；返回它只为排查问题 |
| `maskedMobileNum` | 脱敏手机号，用来跟用户确认发送对象 |
| `expireMinutes` | 验证码有效期（分钟），暂存的 codeKey 与它同寿 |
| `codeLength` | **验证码位数（纯数字）**。按这个长度向用户索取，**不要自己猜**。该值由服务端按调用来源动态决定（Open API 通道当前为 **4 位**），所以**以每次响应为准，不要硬编码**；字段缺失时才退回按 4 位提示用户 |

**发送频率限制**（触发后返回失败，按 `errorInfo` 提示等待，**不要循环重试**）：

| 维度 | 限制 | 说明 |
|------|------|------|
| 手机号 | **1 分钟 1 条** | 刚发过就换号码试也没用，同号必须等满 1 分钟 |
| 手机号 | **单日 10 条** | 与 App 共享同一份配额 |
| IP | **单日 30 条** | 本通道专属；只统计真正发出去的短信，网关故障不扣配额 |
| IP | 每小时 10 条 | 与 App 共享 |

验证码错误另有独立限制：单个 `codeKey` 累计错 10 次即作废；同一手机号 1 小时内累计错 10 次会被锁 1 小时。

---

### 3. 登录/注册并领取密钥

```
POST /open/v1/auth/login
Content-Type: application/json

{
  "mobileNum": "13800000000",
  "verifyCode": "1234",
  "agreementVersion": "sim-risk-1"
}
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `mobileNum` | 是 | 11 位手机号；未注册会自动注册 |
| `verifyCode` | 是 | 用户收到的短信验证码，位数见上一步的 `codeLength`（当前 **4 位纯数字**）。**按字符串原样传，保留前导零**（`"0123"` 不要传成 `123`） |
| `codeKey` | 否 | **不用传**：服务端按手机号取回上一次发码的句柄。仅并发多端等特殊场景才显式指定 |
| `agreementVersion` | 首次必填 | 取自风险告知的 `version`；用户已同意过则可省略 |
| `name` | 否 | 密钥备注名 |
| `forceRotate` | 否 | 默认 `false` 复用已有模拟盘密钥；`true` 会吊销旧密钥并重新签发，**其它设备上的旧密钥立即失效** |

**响应 `data`：**

```json
{
  "apiKey": "oc.<16位>.<secret>",
  "keyId": 12,
  "keyPrefix": "oc.AbCd",
  "userId": 20001,
  "newUser": false,
  "keyCreated": true,
  "scope": "SIM",
  "scopeName": "模拟盘",
  "allowedTradingEnvs": ["sim"],
  "canTradeLive": false,
  "defaultTradingEnv": "sim",
  "simAccountReady": true,
  "simAccountBalance": 2000000.00,
  "simAccountMessage": "模拟盘账户已就绪，可用资金 2000000.00 元，直接查余额或下模拟单即可。",
  "domain": "https://slzqapi.sxslqhsh.com",
  "apiKeyEnvVar": "SLZQ_OPENCLAW_API_KEY",
  "domainEnvVar": "SLZQ_OPENCLAW_DOMAIN",
  "tradingEnvVar": "SLZQ_OPENCLAW_ENV",
  "setupSteps": ["1. 把返回的 apiKey 写入客户端环境变量 …"],
  "liveUpgradeSteps": ["1. 在 App 完成期货实盘登录 …"]
}
```

| 字段 | 说明 |
|------|------|
| `apiKey` | **完整密钥**，写入配置即可；**禁止**回显给用户、写日志或复述 |
| `keyCreated` | `true`=本次新签发；`false`=**返回的是该账号原有的模拟盘密钥**，与用户在 App 里看到的是同一把，可据此告诉用户「没有生成新密钥，旧配置不受影响」 |
| `newUser` | `true`=本次新注册的账号 |
| `scope` | 权限档位，本接口恒为 `SIM` |
| `simAccountReady` | 模拟盘账户是否已就绪。`true`=可直接查余额、下模拟单；`false`=本次自动开通失败，调 `/open/v1/account/summary` 会再试一次 |
| `simAccountBalance` / `simAccountMessage` | 账户余额与人话说明，可直接转述给用户 |

> **领钥即开户**：登录成功时服务端会自动确保该用户的模拟盘账户已开通（幂等，初始资金取服务端字典配置），
> 因此拿到密钥后可以直接查 `/open/v1/account/summary`、直接下模拟单，**不需要**再去 App 点「开通模拟盘」。
> App 侧的开户接口要 `CnToken`，Open API 用户本来也够不着。
| `setupSteps` / `liveUpgradeSteps` | 可直接转述给用户的操作步骤 |

> 使用 MCP 工具 `slzq_open_v1_auth_login` 时，密钥会自动落盘并在当前会话立即生效，工具返回里只有脱敏值。

**常见错误：**

| errorCode | 含义 | 下一步 |
|-----------|------|--------|
| `10008` | 手机号格式错误 | 让用户重新提供 11 位手机号 |
| `10011` | 验证码错误 | 请用户核对；错误累计超限会锁 1 小时，不要替用户猜 |
| `10012` | 验证码已过期，或该手机号没有有效发码记录 | 重新调用发送验证码接口（同号 1 分钟 1 条） |
| `10415` | 未同意风险告知 | 先调 `GET /open/v1/auth/agreement` 展示要点，再带 `agreementVersion` 重试 |

---

## 权限档位（scope）

| 档位 | 含义 | 可用 `X-Trading-Env` | 获得方式 |
|------|------|----------------------|----------|
| `SIM` | 模拟盘 | `sim` | 本页登录流程，或 App 内生成 |
| `SIM_LIVE` | 模拟盘 + 实盘 | `sim`、`live` | 仅 App：实盘登录 → 签署《实盘小龙虾风险告知》→ 勾选实盘并校验 CTP 交易密码 |

- **实盘档位包含模拟盘**：同一把实盘密钥既能跑 `sim` 也能跑 `live`。
- 模拟盘密钥带 `X-Trading-Env: live` 会返回 `10412`，`errorInfo` 里已给出改法。
- 查询当前档位见 [api-account.md](./api-account.md) 的 `GET /open/v1/me`。
- 服务端**不会**通过任何 Open API 把实盘权限授出去；Agent 不得向用户索要 CTP 交易密码。
