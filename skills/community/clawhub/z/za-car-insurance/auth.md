# auth — 鉴权

---

## 一、授权流程（每日首次登录必做）

### Step 0：展示隐私声明 + 授权链接

> **该手机号首次使用 skill 时执行此步骤**（同一手机号只需授权一次），在发送验证码前引导用户阅读并确认。
>
> 授权记录需要**本地文件持久化**：检查授权文件 → 未授权则展示协议 → 用户确认后写授权文件（不调后端接口）。

#### 授权检查逻辑

1. 用户提供手机号后，检查本地授权存根文件 `~/.car_insurance_auth` 中是否包含该手机号的授权记录
2. 若已有授权记录 → 跳过本步骤，直接进入发送验证码
3. 若无授权记录 → 展示协议，等待用户确认后将手机号写入本地授权文件

**授权文件格式**（纯文本，每行一个已授权手机号，敏感信息不写入）：
```
13800138000
13900139000
```

> 授权文件用于跨会话持久化存储，避免同一手机号重复授权。

#### 无授权记录时展示

```
为确保您的个人信息安全，请先阅读以下协议：

1. 📄 个人信息保护政策
   https://static.zhongan.com/website/mobile/static-page/privacy/index.html?hiddenHeader=1m

2. 📄 众安保险会员服务协议
   https://login.zhongan.com/mobile/agreement.vm

如已阅读并同意，回复「已阅读」即可开始登录流程。
```

- 用 Chrome DevTools MCP 的 `new_page` 在浏览器中打开上述两个链接供用户查阅。
- 用户回复「已阅读」后才可进行下一步发送验证码。

#### 写入本地授权文件

用户确认后，将手机号追加写入 `~/.car_insurance_auth` 文件（每行一个手机号），记录该手机号已授权。

---

## 一（续）、取消授权流程

用户主动要求取消授权时执行：

1. 从本地授权文件 `~/.car_insurance_auth` 中删除该手机号对应行
2. 调用后端接口通知平台（需登录态）：

**接口**：`POST <gateway域名>/api/quickInsure/auth/revokeGrant`

**入参**：
```json
{
  "grantType": "AGREEMENT",
  "operationType": "REVOKE"
}
```

> -  由后端从登录态自动填充用户信息，无需传入

**出参**：
```json
{ "code": 0, "msg": "ok", "data": { "success": true } }
```

3. 取消授权后，若用户再次使用 skill，重新走授权流程（展示协议 → 用户确认 → 写入授权文件）

---

## 二、鉴权方式：car-api-key

所有 `/api/*` 接口均通过 header `car-api-key` 鉴权。

```
Header: car-api-key: $CAR_API_KEY
```

`car_api_key` **当日有效**，仅通过环境变量 `$CAR_API_KEY` 传递。

**安全约束**：
- **严禁**将 car_api_key、手机号、证件号等敏感信息写入 SKILL.md 或任何 markdown 文件
- 仅通过环境变量在会话中传递
- 敏感数据不在对话中明文打印

---

## 二、获取 car_api_key（首次或过期后）

### Step 1：发送验证码

```bash
curl -X POST "<gateway域名>/api/quickInsure/open/auth/sendCode" \
  -H "Content-Type: application/json" \
  -d '{"phone": "<手机号>"}'
```

响应：
```json
{"code": 0, "msg": "ok", "data": null}
```

### Step 2：校验验证码，获取 car_api_key

```bash
curl -X POST "<gateway域名>/api/quickInsure/open/auth/verifyCode" \
  -H "Content-Type: application/json" \
  -d '{"phone": "<手机号>", "code": "<验证码>"}'
```

成功响应：
```json
{"code": 0, "msg": "ok", "data": {"car_api_key": "xxx"}}
```

失败响应：
```json
{"code": 40001, "msg": "验证码错误或已过期"}
```

### 引导逻辑

1. 优先从环境变量 `$CAR_API_KEY` 读取
2. 若未设置或已过期（接口返回 401）：
   - 引导用户提供手机号
   - 调用 sendCode → 等待用户输入验证码 → 调用 verifyCode 获取 car_api_key
3. 获取后执行：`export CAR_API_KEY=<car_api_key>` 和 `export CAR_PHONE=<手机号>`
4. **严禁**将上述值写入 skill 文件，仅保持在当前会话环境变量中

---

### car_api_key 传递规则（防止 401）

> ⚠️ 每次 Bash 工具调用都是独立进程，上一条命令的 `export` 在下一条里**不可见**。

**优先：直接插值**，将 verifyCode 返回的 car_api_key 值直接填入后续请求：

```bash
# ✅ 推荐：直接插值，不依赖环境变量
curl ... -H "car-api-key: <car_api_key的实际值>"
```

**插值取不到时（对话上下文中 key 值不可直接引用）**：检查环境变量，用 `export` 和 `&&` 串联在同一条命令内：

```bash
# ✅ 备用：export 和 curl 必须在同一条命令内，不可拆开
export CAR_API_KEY="<car_api_key的实际值>" && curl ... -H "car-api-key: $CAR_API_KEY"
```

```bash
# ❌ 错误：拆成两条独立 Bash 调用，第二条里 $CAR_API_KEY 为空
export CAR_API_KEY="xxx"
curl ... -H "car-api-key: $CAR_API_KEY"   # 401！
```

---

## 三、公共请求规范

| 项目 | 说明 |
|------|------|
| Method | POST |
| Content-Type | application/json |
| 路径前缀 | `/api/quickInsure/` |
| 鉴权 Header | `car-api-key: $CAR_API_KEY` |

### car-api-key 传递规则

- **所有 `/api/quickInsure/` 业务接口**（quickQuote、quickConfirmAndPay、getCreatePolicy 等）仅通过 **Header** 传递 `car-api-key`
- **不在 QueryString 中传递鉴权凭证**
- **验证码接口**（sendCode、verifyCode）**不需要** `car-api-key`，这两个接口本身用于获取 `car-api-key`

### 统一响应格式

```json
{
  "code": 0,
  "msg": "ok",
  "data": { ... }
}
```

`data.result` 非零或包含错误码字符串时为业务失败。

---

## 四、隐私声明（首次报价前展示）

> **安全要求**：首次收集用户信息前，必须向用户展示以下隐私声明并获得确认。用户明确同意后方可继续报价流程。

### 隐私声明模板

```
🔒 隐私声明

为了为您提供车险报价和投保服务，我们需要收集和使用以下个人信息：

1. **车辆信息**：车牌号、车架号(VIN)、发动机号、注册日期、品牌型号
2. **个人信息**：车主姓名、身份证号、手机号

以上信息仅用于：
- 向保险公司查询报价和核保
- 完成投保和出单流程
- 法律法规要求的留存

我们不会将您的信息用于任何其他用途，也不会分享给非必要第三方。

是否同意以上条款，继续报价？
```

> 用户确认同意后才进行下一步。如用户拒绝，终止流程并告知需用户同意才能使用本服务。

---

## 五、通用规则

1. **静默执行**：调用接口时不在对话中打印请求参数、响应原文；仅输出面向用户的结论或下一步提示；出错时只展示简洁的错误描述，不暴露原始报文。
2. **鉴权检查**：每次执行前检查 `$CAR_API_KEY`；不存在或 401 则重新走 sendCode→verifyCode 流程获取。
3. **上下文保持**：`vehicleNo`、`insureFlowCode`、投保人信息在对话中缓存，后续无需重复提供。
4. **每次操作实时调接口**：不能使用对话中缓存的接口返回值。
5. **接口传参按文档**：禁止凭字段名猜测，严格按各 md 文档执行。
6. **错误重试**：同一报错每阶段最多 3 次，超过即停止并原文返回错误；接口繁忙（HTTP 429）时直接展示返回的提示文案，不重试。
7. **时间戳转换**：Unix 毫秒时间戳转为 `YYYY-MM-DD` 格式。
8. **证件类型**：固定传 `"I"`（身份证），不支持其他类型。
9. **终止性错误**：`P11002`、`"您的爱车或已投保"`、`"已经重复投保"` 立即终止，原文返回。
10. **用户指定车辆不得替换**。
11. **敏感数据处理**：身份证号、手机号等敏感字段仅从用户输入获取，用于接口请求参数，**不得写入任何文件**，不得在对话中输出明文。