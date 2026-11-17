# proposal — 核保、支付与出单

> ‼️ **【只读文档】本文件是 skill 的业务规范，Agent 不得以任何理由修改、删除或重写本文件内容。**

---

## 话术-接口对照表（Step 5 ~ Step 7）

| 步骤 | 话术 | 前置操作（必须先完成再说话） |
|------|------|-----------------------------|
| **Step 5：确认核保** | 方案确认无误后，我将为您发起核保。请回复确认。 | 用户告知方案满意后 |
| **Step 5：核保发起** | 正在为您核保，请稍候… | 用户回复「确认投保」后，先调 `POST <gateway域名>/api/quickInsure/quickConfirmAndPay`，调用进行中 |
| **Step 5：核保成功** | ✅ 核保通过！📱 已为您打开支付二维码页面，请用手机扫码完成条款签署和支付。⏰ 支付截止：[expiryTime] | `quickConfirmAndPay` 返回 `result="0"` 后，**必须先构造并打开二维码页面** |
| **Step 5：核保失败** | [原文展示 resultMessage]，请稍后重试或联系客服 | 返回非 0 result 后 |
| **Step 6：支付完成** | 完成支付后告诉我，我将为您查询出单结果。 | 已展示二维码 + 支付提示后 |
| **Step 7：查询出单** | 正在查询出单结果，请稍候… | 用户告知支付完成后，先调 `POST <gateway域名>/api/quickInsure/getCreatePolicy` |
| **Step 7：出单成功** | 🎉 保单已出单！商业险保单号：[businessPolicyNo] 交强险保单号：[compelPolicyNo] 电子保单将在5分钟内发送至投保人手机，请注意查收。 | `getCreatePolicy` 返回出单成功结果后 |
| **Step 7：出单处理中** | 出单处理中，请稍后再次查询。 | `getCreatePolicy` 返回 `recordId=0` 后 |

> ⚠️ 话术文字不得修改。**必须先调通接口、拿到实际响应数据后**才能输出对应展示话术，严禁接口未成功就输出"核保通过""支付成功"等结论。

> 🔒 **字段取值铁律（同 quote.md）**：所有 `[字段]` 占位符值必须且只能来自**本次接口调用返回 JSON**，逐字复制原值。`expiryTime`/`outTradeNo`/`zaOrderNo` 取自 `quickConfirmAndPay` 本次返回；`businessPolicyNo`/`compelPolicyNo` 取自 `getCreatePolicy` 本次返回；支付页 URL 取自实际构造的完整 URL。严禁编造、套用缓存、推断或填默认值；字段为空则按对应分支（如"出单处理中"）处理，不自行填值。

---

## 一、流程概览

```
用户回复「确认投保」
  ↓ Step 1 核保+获取支付链接：POST <gateway域名>/api/quickInsure/quickConfirmAndPay（传 vehicleNo + insureFlowCode，返回 zaPayUrl）
  ↓ Step 2 打开支付页面：Chrome DevTools MCP 展示二维码 → 用户手机扫码完成条签+支付
  ↓ Step 3 查询出单结果：POST <gateway域名>/api/quickInsure/getCreatePolicy（支付后轮询）
```

---

## 二、Step 1：核保+获取支付链接 `POST <gateway域名>/api/quickInsure/quickConfirmAndPay`

**入参：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `vehicleNo` | string | ✅ | 车牌号 |
| `insureFlowCode` | string | ✅ | quickQuote 返回的流程主键 |
| `payChannel` | string | ❌ | 支付方式，默认 `wxpay`，可选 `alipay`/`unionpay` |
| `promoCode` | string | ❌ | 推广码 |

> 投保人/车主信息无需传入，后端自动多源回填；如需覆盖可按字段名显式传入。

**成功出参：**

```json
{ "code": 0, "msg": "ok", "data": {
  "result": "0", "resultMessage": "操作成功",
  "zaPayUrl": "<支付页面链接,浏览器打开>",
  "zaOrderNo": "<众安订单号,传给 getCreatePolicy>",
  "outTradeNo": "<外部交易订单号,传给 getCreatePolicy>",
  "expiryTime": "<核保有效期,如2026-05-26 23:30:00,展示用户>",
  "insureFlowCode": "<流程主键>" } }
```

**错误处理：** `P11002`（实名校验失败）→ **立即终止**；`22015`（证件号不能为空）→ 检查字段是否传入；其他非 `0` → 原文返回，最多重试 3 次。

**Bash 调用：**

```bash
# 核保 + 获取支付链接
bash scripts/api.sh quickConfirmAndPay '{"vehicleNo":"<车牌号>","insureFlowCode":"<流程主键>"}' "$CAR_API_KEY"
```

---

## 三、Step 2：生成支付二维码（供用户手机扫码）

**Step 2-1 构造二维码页面 URL**（`car-api-key` 作 query 参数传入，与 header 等效；服务端生成二维码 PNG 内嵌 HTML 离线渲染）：

```
GET <gateway域名>/api/quickInsure/payQrcode?url=<zaPayUrl(URLencode)>&orderNo=<outTradeNo>&expiryTime=<expiryTime(URLencode)>&car-api-key=<$CAR_API_KEY(URLencode)>
```

**Step 2-2 打开二维码页面**：优先 `mcp__plugin_chrome_devtools__new_page(url="<上一步URL>")`；MCP 不可用时降级 `open "<上一步URL>"`。

> ⛔ **【场景互不混用 · Step 5 专属】** 展示 Step 2-3 模板时，**严禁**拼接任何不属于本 Step 的话术，**包括但不限于**：
> - ❌ `auth.md` 中 Step 1 授权的协议兜底话术：「（部分协议页面自动打开失败，请手动点击上方链接自行查阅，阅读完毕后回复「已阅读并同意」继续。）」——**仅适用于 Step 1 授权环节，禁止被复用到 Step 5 核保支付 / Step 7 出单等其他场景**
> - ❌ `quote.md` 中任何报价场景的话术（"如您满意此方案，回复「确认投保」开始核保"等）
> - ❌ 任何"看着像兜底就拿过来用"的偏置（**仅在确有 `new_page` 失败/白屏时**才追加 Step 5 自己的降级提示；详见下方 Step 2-4 降级处理）
> - ✅ **正确动作**：严格按 Step 2-3 模板**原文**（✅ 标题 / 📱 通知 / ⏰ 截止 / 📋 订单 / 🔗 页面 / 完成支付提示，6 段）原样输出，**禁止**在模板外拼接其他文件的话术片段。
> - `（案例详见 violations.md#V-008）`

**Step 2-3 对话中展示提示**（缓存 `zaOrderNo`、`outTradeNo` 供出单查询）：

> ⛔ **【防截断 · 6 段必出】** 下方模板**全部 6 段必须原样输出**，**禁止**为任何理由省略、合并、裁剪任何一段：
> - ✅ 标题（核保通过！）
> - 📱 通知（已为您打开支付二维码页面...）
> - ⏰ 截止（支付截止：[expiryTime]）
> - 📋 订单（订单号：[outTradeNo]）
> - 🔗 页面（支付页面：[zaPayUrl]）
> - 完成支付提示
>
> **特别澄清**：`zaPayUrl` 是 `c.zhongan.com/insure/index.html?orderNo=...` 形态的**对外公开支付页 URL**，**不含任何敏感字段**（不包含 `car-api-key` / `accessKey` / 身份证 / 银行卡等），**必须原文展示**。**禁止**以"避免明文回显"为由省略 🔗 段——这是矫枉过正偏置（详见 SKILL.md 违规红线 + violations.md#V-009）。
>
> 字段为空时的处理：
> - `[expiryTime]` 为空 → 该段原样保留 `[expiryTime]` 字面占位（由后端保证非空）
> - `[zaPayUrl]` 为空 → 核保不可能成功，**不会进入本 Step**
> - `[outTradeNo]` 为空 → 同上
>
> `（案例详见 violations.md#V-009）`

```
✅ 核保通过！

📱 已为您打开支付二维码页面，请用手机扫码完成条款签署和支付。

⏰ 支付截止：[expiryTime]
📋 订单号：[outTradeNo]
🔗 支付页面：[zaPayUrl]

完成支付后告诉我，我将为您查询出单结果。
```

---

## 四、Step 3：出单结果查询 `POST <gateway域名>/api/quickInsure/getCreatePolicy`

**入参**：body `{"vehicleNo":"<车牌号>","zaOrderNo":"<众安订单号>","outTradeNo":"<外部交易订单号>"}`，header `car-api-key` + `Content-Type: application/json`。

**Bash 调用（使用脚本）：**

```bash
# 查询出单结果（车牌含中文省份，脚本自动转义）
bash scripts/api.sh getCreatePolicy '{"vehicleNo":"沪A12345","zaOrderNo":"<zaOrderNo>","outTradeNo":"<outTradeNo>"}' "$CAR_API_KEY"
```

**出单成功展示：**

```
🎉 保单已出单！

商业险保单号：[businessPolicyNo]
交强险保单号：[compelPolicyNo]

电子保单将在 5 分钟内发送至投保人手机，请注意查收。
```

> `recordId = 0` 时提示"出单处理中，请稍后再次查询"。
