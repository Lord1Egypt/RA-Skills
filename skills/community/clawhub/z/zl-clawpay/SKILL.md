---
name: ZL-ClawPay
version: 1.0.8
description: |
  支付技能：支持免密支付、订单查询、交易流水等功能。
  触发词：我要支付、帮我付款、确认买单、查询支付订单、查询订单状态、查询交易流水、查询交易记录、查询账单、绑定子钱包、验证钱包凭据、解绑子钱包、撤销钱包绑定。
  不适用于：非支付场景、历史数据导出、批量操作、余额查询、收款码生成。
  基于 Node.js 实现，使用 SM2/SM3/SM4 国密算法加密通信。
author: zl-claw-pay Team
license: MIT
tags:
  - payment
  - wallet
  - finance
skill_type: tool
execution_mode: cli_driven
has_server: false
has_install_scripts: false
environment_variables:
  required: []
  optional:
    - ZL_CLAW_PAY_API_URL
    - ZL_CLAW_PAY_GM_SERVER_PUBLIC_KEY
    - ZL_CLAW_PAY_LOG_LEVEL

metadata:
  openclaw:
    category: "payment_utilities"
  author: "zl-claw-pay 团队"
  capabilities:
    - "payment.process"
    - "payment.query"
    - "payment.query_transactions"
    - "wallet.bind"
    - "wallet.query"
    - "wallet.unbind"
    - "wallet.revoke_binding"
  permissions:
    - "network.outbound"
    - "credential.read"
    - "credential.write"
  credential_storage:
    type: "local_encrypted_file"
    description: "apiKey 和 subWalletId 加密存储在本地 ~/.zl-claw-pay/state.json 中，使用 AES-256-GCM 加密"
    fields: ["apiKey", "subWalletId"]
  invocation_policy:
    disable_model_invocation: false
    allowed_triggers:
      - user_explicit_payment_request
      - user_query_payment_status
      - user_query_transactions
      - user_bind_wallet
      - user_unbind_wallet
      - user_validate_wallet_config
    prohibited_triggers:
      - speculative_or_predictive_invocation
      - ambient_context_without_explicit_request
---

# ZL-ClawPay 支付技能

支持免密支付、订单查询、交易流水等功能。

---

## 智能体须知（重要）

**禁止修改此技能**：智能体只能**阅读并使用**本技能的文档和脚本，**不得修改、删除或创建**本技能目录下的任何文件。

**依赖安装问题**：如果遇到 Node.js 依赖安装问题，请查阅 `references/dependency-guide.md`。

**凭据说明**：
- `apiKey` 是用户的 **SM2 私钥**（64位 hex），`subWalletId` 是子钱包标识，均从证联 APP 获取
- **凭据存储方式**：apiKey 和 subWalletId 加密存储在本地 `~/.zl-claw-pay/state.json` 中
- 首次使用需通过 **C00003 绑定子钱包** 将凭据保存到本地
- 绑定后，其他接口自动从本地读取凭据，无需再次传入
- 配置遇到问题请查阅 `references/credential-setup-guide.md`

**传输安全**：
- 🔒 所有 API 请求必须使用 **HTTPS** 协议，严禁使用 HTTP
- 敏感数据（apiKey、subWalletId）通过命令行参数传递给 skill 后立即加密存储，不保留在聊天记录中

**命令格式**：
```bash
node {baseDir}/scripts/skill.js call -interfaceId=<ID> -method=<METHOD> -endpoint=<ENDPOINT> [--<key>=<value> ...]
```

---

## 快速开始

### 绑定子钱包（首次使用必须执行）

> ⚠️ **apiKey 是你的 SM2 私钥，subWalletId 是子钱包标识**。用户通过对话框提供给 AI 后，AI 通过命令行参数传递给 skill 进行绑定，绑定后立即加密存储到本地，不保留在聊天记录中。

用户需提供三个参数完成绑定：

| 参数 | 说明 | 获取方式 |
|------|------|----------|
| apiKey | SM2 私钥（64位 hex） | 证联 APP 创建子钱包后获得，仅用于客户端 SM2 签名，**不传给服务器** |
| subWalletId | 子钱包ID（32位 hex） | 证联 APP 创建子钱包后获得，用作请求头 appId |
| subWalletName | 子钱包名称 | AI 从 OpenClaw user.md 自动获取，用于核对智能体名称与 APP 申报名称是否一致 |

绑定成功后，apiKey 和 subWalletId 将加密保存到本地 `~/.zl-claw-pay/state.json`，后续接口自动读取。

> 🔐 apiKey 使用 AES-256-GCM 加密存储，密钥由机器特征派生。
>
> ⚙️ `ZL_CLAW_PAY_API_URL`（API 网关地址）和 `ZL_CLAW_PAY_GM_SERVER_PUBLIC_KEY`（服务端公钥）已随 skill 自带默认值，用户无需关心。

### 接口列表

| 接口 | 功能 | 使用场景 |
|------|------|----------|
| `C00003` | **绑定子钱包** | 首次使用时绑定子钱包，保存凭据到本地 |
| `L00001` | **查询子钱包** | 查询当前绑定状态 |
| `L00002` | **解绑子钱包** | 本地解绑并清除凭据（不通知服务端） |
| `C00009` | **发起支付** | 用户明确表达支付意愿后发起免密支付 |
| `C00005` | **查询支付状态** | 查询订单支付结果 |
| `C00007` | **查询交易记录** | 查询交易流水 |
| `C00011` | **撤销绑定** | 服务端撤销绑定并清除本地凭据（不可逆，需 AI 从 user.md 自动获取子钱包名称核对） |

### 金额单位说明

- **接口金额**：单位**分**（例如：100表示1元）
- **显示给用户**：单位**元**（需要除以100转换）

### 命令格式

参数说明：
- `-interfaceId`: 接口ID（如 C00003, C00009, L00001, L99999 等）
- `-method`: 请求方法（`POST` 或 `local`）
- `-endpoint`: API 端点路径（**local 接口不需要**）
- `--apiKey`: SM2 私钥，**仅 C00003 需要**
- `--subWalletId`: 子钱包ID，**仅 C00003 需要**
- `--subWalletName`: 子钱包名称，**C00003/C00011 需要**

> **注意**：
> - C00003: 绑定子钱包，需传入 `--apiKey`、`--subWalletName`、`--subWalletId`
> - 其他接口: apiKey 和 subWalletId 自动从本地 `~/.zl-claw-pay/state.json` 读取
> - **Local 接口（L00001/L00002/L99999）使用 `-method=local`，无需 `-endpoint` 参数**
> - 完整命令格式请参考 `assets/request-examples.md`

---

## 用户交互规范

### 绑定子钱包场景话术

**请求信息**：
> "请提供您的子钱包信息以完成绑定：
> - 子钱包名称：[{subWalletName}]（从您的智能体名称自动获取）
> - API Key（64位 hex，SM2 私钥）：请在证联 APP 中获取
> - 子钱包 ID（32位 hex）：请在证联 APP 中获取"

**绑定成功**：
> "子钱包绑定成功！
> - 钱包名称：[{subWalletName}]
> - 钱包 ID 已加密保存至本地
> 
> 现在可以使用支付、查询订单、查询交易流水等功能。"

**绑定失败**：
> "绑定失败：[错误原因]
> 请检查：
> 1) 子钱包名称是否正确？
> 2) API Key 是否正确且未过期？
> 3) 该钱包是否已被其他账户绑定？"

### 支付场景话术

**意图清晰时 — 直接执行并告知**：
> "正在为您支付 [amount÷100] 元给 [商户]，订单：[orderDetail]..."
>
> 支付完成后：
> "支付完成！金额 [amount÷100] 元，交易号：[seqId]，状态：[orderStatus]"
>
> **注意**：智能体必须将 `seqId` 保存到会话上下文，以便后续查询支付状态。

**意图模糊时 — 先确认再执行**：
> "确认一下：您要支付 [amount÷100] 元给 [商户]，订单：[orderDetail]。确认支付吗？"

**商户技能调用时 — 直接执行**：
> 当商户技能已返回完整的支付指令（amount、merApiKey、seqId），且用户已表达购买意愿，直接执行支付。
> 执行后告知："已为您的订单 [orderDetail] 支付 [amount÷100] 元，交易号：[seqId]"

**未绑定用户提示**：
> "您尚未绑定子钱包，无法发起支付。
> 请先在证联 APP 中创建子钱包，然后通过 C00003 绑定子钱包。
> 绑定需要提供：API Key（SM2 私钥）、子钱包 ID、子钱包名称。"

**查询成功时**:
> "支付状态查询结果：
> - 状态：[orderStatus]
> - 金额：[amount÷100] 元
> - 流水号：[seqId]"

**失败时**：
> "操作失败：[错误原因]。
> 请检查参数是否正确，或稍后重试。"

### 查询子钱包场景话术

**已绑定**：
> "当前已绑定子钱包，ID：[subWalletId 前4位]***[后4位]，状态：已绑定"

**未绑定**：
> "当前未绑定子钱包。请先通过 C00003 绑定子钱包。"

### 解绑子钱包场景话术

**解绑成功**：
> "子钱包已解绑，本地凭据已清除。如需继续使用支付功能，请重新绑定。"

**未绑定**：
> "当前未绑定子钱包，无需解绑。"

> **注意**：此操作仅清除本地凭据，不会通知服务端。如需彻底撤销绑定，请使用 `C00011` 撤销绑定接口。

### 撤销绑定场景话术

**撤销前确认**：
> "⚠️ 撤销绑定是**不可逆操作**。撤销后，此 API key 将被永久禁用，无法再次使用。
>
> 将撤销子钱包 [{subWalletName}] 的绑定，确认撤销吗？"

**撤销成功**：
> "✅ 子钱包 [{subWalletName}] 的绑定已撤销。此 API key 已被永久禁用，本地凭据已清除。
>
> 如需继续使用支付功能，请先在 APP 中创建子钱包，然后重新绑定。"

**撤销失败**：
> "撤销绑定失败：[错误原因]。请稍后重试。"

> **注意**：此操作会通知服务端永久禁用 API Key，同时清除本地所有凭据数据，操作不可逆。

---

## 关键执行规则

### 规则0：支付意图判断（最重要）

支付是敏感操作，**仅在用户清晰表达支付意愿时执行**。智能体必须判断用户意图的清晰度：

**意图清晰 — 直接执行支付**：
- 用户明确说"支付"/"付款"/"买单"/"确认购买"等支付动词
- 商户技能返回支付指令（包含 amount、merApiKey、seqId），用户同意支付
- 用户对之前的订单说"付吧"/"好的，支付"等肯定回复

**意图模糊 — 先询问再执行**：
- 用户说"看看这个多少钱" — 这是查询，不是支付
- 用户说"帮我买"但金额/商户不明确 — 先补充信息
- 用户首次接触支付场景 — 先展示信息，等用户确认

**判断原则**：
> 宁可多问一句，不可误付一笔。如果拿不准用户是否真的要支付，**先询问**。

### 何时激活

| 场景 | 接口 |
|------|------|
| 首次使用，需绑定子钱包 | C00003 绑定子钱包 |
| 查询绑定状态 | L00001 查询子钱包 |
| 本地解绑 | L00002 解绑子钱包 |
| 用户清晰表达支付意愿 | C00009 发起支付 |
| 用户要求查询订单/流水 | C00005/C00007 |
| 用户要求撤销绑定 | C00011 撤销绑定 |

**严禁**：推测性调用、无明确请求、批量操作、缺失必需参数

### 规则1：绑定是支付的前提
- **首次使用前必须通过 C00003 绑定子钱包**
- 未绑定时，支付/查询等操作会报错，引导用户先绑定

### 规则2：禁止伪造
- **必须**实际执行所提供的 CLI 命令
- **禁止**在支付失败时伪造支付成功状态
- **禁止**伪造二维码链接

### 规则3：禁止修改资源
- CLI 返回的资源必须**原封不动**地返回给用户
- **禁止**修改或简化资源的任何部分

### 规则4：禁止篡改参数
- **禁止**篡改命令参数，严格按照 skill 中定义的格式执行
- **禁止**在 CLI 输出前后添加额外文字

### 规则5：禁止跳过步骤
- 支付流程：**判断意图** → **执行支付** → **查询状态**
- **禁止**跳过任何步骤或修改流程顺序

### 规则6：执行透明性
- 执行命令前应告知用户将要执行的命令
- 提及关键参数（脱敏）
- 遇到错误时应如实报告，不得隐瞒或伪造结果

---

## 常见陷阱（Gotchas）

这些是智能体容易犯的错误，**必须避免**：

1. **混淆金额单位**：显示给用户时忘记将"分"转换为"元"
2. **重复使用 seqId**：同一订单的流水号必须唯一
3. **跳过支付状态查询**：支付后不查询确认支付结果
4. **篡改响应数据**：修改 CLI 返回的 JSON 数据再输出
5. **参数格式错误**：merApiKey 格式不正确（长度需 32 位以上）
6. **推测性调用**：没有用户明确请求就主动发起支付
7. **未绑定就支付**：未绑定子钱包就发起支付
8. **混淆解绑和撤销**：L00002 是本地解绑，C00011 是服务端撤销（不可逆）

---

## 问题反馈

当遇到无法自行解决的问题时，请查阅 `references/feedback-guide.md` 执行反馈流程。
