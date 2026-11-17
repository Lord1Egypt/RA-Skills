# 402 全流程

> 本文件只在**进入支付流程前读一次**。付款动作全部交给官方 `alipay-payment-skill` 的 `alipay-bot`，本文件不定义任何付款实现。

## 0. 前置确认（缺一项就停）

| 项 | 要求 |
|---|---|
| `query` | 非空，含天数/同行人/预算/偏好等要素 |
| `email` | 非空且格式合法（交付 PDF 依赖它） |
| 单价认知 | 用户已知 **0.99 元/次**，且**同一次咨询只应付款一次** |
| 官方 CLI | `alipay-bot` 可执行（`alipay-bot --help` 有 `402-buyer-pay`） |

## 1. 本地校验请求体（不发请求）

```bash
node "$SKILL_DIR/scripts/travel_aipay.mjs" body \
  --query '杭州三日亲子游，2 大 1 小，预算 5000 元以内，想少走路' \
  --email 'buyer@example.com' \
  --country-code CN --topic-type 7 --is-family-suitable 1 --is-leisure 1
```

输出即最终 `POST` body。字段范围写错（如 `topic_type=99`）会以退出码 `2` 拒绝，**不会发起请求**。

## 2. 取 402 账单

```bash
node "$SKILL_DIR/scripts/travel_aipay.mjs" probe \
  --query '杭州三日亲子游，2 大 1 小，预算 5000 元以内，想少走路' \
  --email 'buyer@example.com' \
  --country-code CN --topic-type 7 --is-family-suitable 1 --is-leisure 1
```

产出（位于 `.xianzong-travel-aipay/`，权限 `0700` / 文件 `0600`，已 gitignore）：

| 文件 | 内容 |
|---|---|
| `payment-needed.txt` | 原样保存的 `Payment-Needed` 响应头（不解码、不改写） |
| `body.json` | **这一单的原始请求体**，后续取货/查询必须复用它 |
| `state.json` | `resourceUrl` / `outTradeNo` / `amount` / `currency` / 文件名 |

对客只需说清：服务名、单价、订单号（`out_trade_no`）、资源地址，以及"付款后再回来取方案"。

## 3. 发起支付（官方 CLI，需用户明确确认）

```bash
node "$SKILL_DIR/scripts/travel_aipay.mjs" pay --confirm --session-id '<当前会话标识>'
```

该子命令内部等价于下面的官方命令（`--intent-summary` 概括**用户的原始业务目的**，不是 URL 或支付材料）：

```bash
alipay-bot 402-buyer-pay \
  --session-id '<当前会话标识>' \
  --file '.xianzong-travel-aipay/payment-needed.txt' \
  --resource-url 'https://api.riyuexinzhu.com/aipay/travel_consultant' \
  --method 'POST' \
  --data "$(cat '.xianzong-travel-aipay/body.json')" \
  --header 'Content-Type: application/json' \
  --intent-summary '原始请求：用户请求仙踪问道旅行咨询，需要一份含行程与 PDF 的亲子游方案'
```

规则（继承 alipay-payment-skill）：

- `--confirm` 只在**用户本次对话明确同意付款**后才能加；未确认时脚本直接以退出码 `2` 拒绝，不调用 CLI。
- `--resource-url` 永远是**原资源地址**，不是支付链接。
- 命令待确认时：保存对客标签（订单号 / 交易号 / 支付方式链接），把支付入口原样展示一次后 **STOP**。
- 首卡异常/超时/未知输出：**不自动重试**；只有用户明确要求重发时才再调用一次，且**订单号、金额、收款对象不变**。
- 已支付成功 / 订单关闭 / 身份错误 → 禁止重发。

## 4. 支付后取货（首选，凭同一订单）

### 路径 A：官方查询（推荐，会自动发履约回执）

```bash
# 推荐：自动轮询到交付（409 / 瞬时失败都会重试，不会重复扣费）
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '<32 位订单号>' --wait

# 只查一次
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '<32 位订单号>'
```

轮询参数：`--poll-interval-ms`（默认 40000）、`--max-wait-ms`（默认 900000，超时返回 `3`）。

内部等价于：

```bash
alipay-bot 402-query-payment-status \
  --out-shake-no '<32 位订单号>' \
  --resource-url 'https://api.riyuexinzhu.com/aipay/travel_consultant' \
  --method 'POST' \
  --data "$(cat '.xianzong-travel-aipay/body.json')" \
  --header 'Content-Type: application/json' \
  --output json
```

命令在资源非空时会**自动发送履约回执**，因此成功路径**不要**再执行任何回执命令。

#### 载荷判读（2026-11-14 实测，**必读**）

官方 `--output json` 只有三种形状。**不要用 `resourceDelivered` 或退出码判成功**：

| 形状 | 关键字段 | 含义 | 动作 |
|---|---|---|---|
| 成功 | `success: true`、`resourceResponse.status: 200`、`resourceResponse.body.content`（业务 JSON 字符串） | 已交付；`body.already_fulfilled=true` 为幂等重放 | 展示结果，结束（不再发回执） |
| 生成中 | `errorMessage` 含 `HTTP 409`、`resourceResponse.status: 409` | 已验付，方案生成中 | 同一订单等一会再查 |
| 瞬时失败 | `errorCode: RESOURCE_REQUEST_FAILED`、`resourceResponse: null` | 服务发布/重启或网络瞬断 | 原样重跑同一命令 |

> ⚠️ 踩坑记录：`resourceDelivered` **不是** 402 协议字段，也不是官方文档化约定——它只是 `alipay-bot --output json` 信封的内部字段（二进制中存在 `json:"resourceDelivered"` 与 `json:"resourceDelivered,omitempty"`，成功路径会被省略，只有失败载荷出现 `false`），只能用作诊断。曾用它（`grep '"resourceDelivered": true'`）当成功判据，导致交付早已成功（服务端 `state=FULFILLED, is_first_delivery=False`）却反复查询、界面一直显示「其他/未交付」。判据只看 `success` / `resourceResponse.status` / `body.content`，且 `complete --wait` 已内置，勿自己再写轮询循环。

### 路径 B：带官方凭证直取

当官方 CLI 已给出可用 `Payment-Proof` 时：

```bash
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --proof '<Payment-Proof>'
```

判读（退出码）：

| 码 | 含义 | 动作 |
|---|---|---|
| `0` | 交付成功 | 展示正文 + PDF；**不再发回执** |
| `3` | 409 资源生成中 | 按 `Retry-After`（默认 30s）用**同一订单**重试或改用路径 A；**绝不重新付款** |
| `4` | 业务层失败 | 原样报告 `resp_message`；不重试、不重复付款 |
| `5` | 凭证无效（新 402） | 报告凭证失效；如需继续，按**新账单**重新走付款确认 |
| `6` | 5xx | 报告服务端错误；仅网络类错误允许重试一次 |
| `2` | 参数错误 | 修参数后再发起 |

## 5. 结果展示

- 正文：Markdown 原样展示（`data.content`）。
- PDF：`data.pdf_oss_file_url` **完整输出**（含 `OSSAccessKeyId` / `Expires` / `Signature`），说明约 90 天有效、并已发送到请求填写的邮箱。
- 目的地、参考资料条数可一并展示；**不要展示任何 cost / pricing / 内部计费字段**。

## 6. 状态不明时的唯一动作

出现下面任一情况，先查单再决定，**都不重新付款**：

- `complete` 超时、进程被中断、输出被截断；
- 用户说"我付了 / 付好了 / 继续 / 好了吗"；
- 拿到 409。

```bash
node "$SKILL_DIR/scripts/travel_aipay.mjs" complete --out-shake-no '<订单号>' --wait
```

原请求体丢失时仍可只查状态，但要说明**可能无法自动恢复资源**。

## 7. 禁止事项

- ❌ 自行构造 `Payment-Proof`、自行签名、直接调用支付宝网关。
- ❌ 402 之后换 `query` 内容或换 `body.json`（履约按订单保存的原始请求执行）。
- ❌ 收到 409 后重新取账单（会产生新订单 → 同一需求重复付款）。
- ❌ 成功后再追加一次履约回执。
- ❌ 把 `Payment-Proof`、`payment-needed.txt` 内容回显到面客文本或写入宽权限文件。
