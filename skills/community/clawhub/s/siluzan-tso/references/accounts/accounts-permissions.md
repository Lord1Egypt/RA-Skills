# 账户权限与绑定

> 流程见 `workflows.md` **W9**。写操作须 `--commit`；**解绑/取消分享/reauth** 另须 `--i-confirm`（CLI 硬门控：未确认则拒绝执行），见 `write-audit-restore.md` 与 `agent-conventions.md`。

## Contents

- account me / check-access / auth / reauth / delink
- mcc-bind / mcc-unbind / share / unshare / share-detail
- close / bm-bind / withdraw-_ / bc-_ / email-\*
- 仅限网页的操作

## account — 账号管理（OAuth 授权 / 解除关联 / Google MCC / 分享）

### account me — 当前登录丝路赞账号

查询当前凭据对应的丝路赞用户（`GET /query/account/me`）。**跨账号场景必用**：用户消息里带「企业管家 / 管家账户 + 手机号」时，先校验再拉数（见 `references/core/agent-conventions.md` §跨账号）。

```bash
# 查看当前登录账号
siluzan-tso account me

# Agent：校验用户指定的企业管家手机号是否与当前登录一致
siluzan-tso account me --check-phone 15130150466 --json-out ./snap-me
```

| 场景                       | 行为                                                             |
| -------------------------- | ---------------------------------------------------------------- |
| 未传 `--check-phone`       | 输出 entityId / 手机号 / 邮箱 / companyId                        |
| `--check-phone` 与当前一致 | exit 0，JSON 含 `matched: true`                                  |
| `--check-phone` 不一致     | exit 1，提示暂不支持查他户数据，引导 `send-login-code` + `login` |

---

### check-access — Google 账户访问权限校验

**仅支持 Google。** 无 `-m`；`-a` 只接受 Google 纯数字 `mediaCustomerId`。TikTok / MetaAd / BingV2 / Yandex **禁止**调用本命令，授权是否失效看 `list-accounts` 的 `invalidOAuthToken`。

校验当前丝路赞凭据是否对指定 **Google** 广告账户有访问权限。应在拉数/诊断前调用，避免误用他户 ID。

> **硬约束**：**禁止**凭 403、空结果或经验臆测「授权/OAuth 过期」。要对用户下「授权不可用 / 需重授权」结论前，**必须**先跑本命令，以 CLI 返回的 `status` 为准；**禁止**跳过本命令直接 `reauth` 或口头推断。

**套餐激活字段（可选前提）**：若 `list-accounts` 输出中**出现** `ma.scopeActivatedSources`（或 Google「套餐激活」列），须先确认有未过期条目再据此谈「授权过期」；**输出中无该字段/列时：跳过套餐判断，直接跑本命令**，且**禁止**向用户解释套餐是否激活。

| 结果                               | 含义                                                                                         |
| ---------------------------------- | -------------------------------------------------------------------------------------------- |
| `accessible`（200 / `true`）       | 授权可用，可继续拉数/操作                                                                    |
| `reauth_required`（200 / `false`） | 已绑定但 Google OAuth 不可用 → 走重授权                                                      |
| `no_permission`（403 / 账户 ID）   | 网关不可访问；可与 `list-accounts` 的 `invalidOAuthToken` 交叉确认是否授权失效或不在本账号下 |

**注意**：当输出能确认套餐**未激活**时，不要用本命令判断授权过期（未激活户仍可能返回 `accessible`）。无激活字段时不适用本条。

```bash
# 1) 可选：list-accounts 核验账户；仅当输出含 scopeActivatedSources 时才看套餐
siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap

# 2) 查网关访问 / 授权是否可用
siluzan-tso account check-access -a <mediaCustomerId>
siluzan-tso account check-access -a 4256317784 --json-out ./snap-access
```

| HTTP | body            | 含义                                           | CLI `status`                                                           |
| ---- | --------------- | ---------------------------------------------- | ---------------------------------------------------------------------- |
| 200  | `true`          | 可访问                                         | `accessible`（exit 0）                                                 |
| 200  | `false`         | 已绑定但 Google OAuth 不可用                   | `reauth_required` → Agent 优先 `present_reauth`；备选 `account reauth` |
| 403  | 账户 ID         | 无权限（多不在本账号下；授权失效时也可能出现） | `no_permission`（exit 1）                                              |
| 403  | `token不能为空` | 未绑定 Google 媒体                             | `google_not_bound` → Agent 优先平台授权；备选 `account auth -m Google` |
| 401  | 空              | 丝路赞 Token 失效                              | `siluzan_token_invalid` → 重新 login                                   |

> 与 `list-accounts -k` 互补：`list-accounts` 查「是否在列表 / `invalidOAuthToken`」（以及**若存在**则含套餐激活）；本接口查「Google 网关是否允许当前凭据访问该 mediaCustomerId」。列表批量筛失效仍优先看 `invalidOAuthToken`；单户深查用本命令。

---

```bash
siluzan-tso account auth -m <媒体类型>
```

| 选项                 | 说明                                                                     |
| -------------------- | ------------------------------------------------------------------------ |
| `-m, --media <type>` | 媒体类型（必填）：`Google \| TikTok \| Meta \| Yandex \| BingV2` |

> **Siluzan Agent**：优先使用 Agent 自带的**授权 / 添加授权**工具；CLI `account auth` **不禁止**，可作备选（沙箱不自动开浏览器，须把完整 URL 贴给用户）。

**示例：**

```bash
# 首次授权 Google Ads 账户
siluzan-tso account auth -m Google

# 首次授权 TikTok Ads 账户
siluzan-tso account auth -m TikTok

# 首次授权 Meta（Facebook）Ads 账户
siluzan-tso account auth -m Meta
```

---

### reauth — 重新授权（先解绑再 OAuth）

OAuth 失效时恢复授权。对齐 TSO 网页 **「重新授权」**：程序会先 **delink** 断开关联，再跳转媒体 OAuth。**禁止**对失效账户跳过解绑直接用 `account auth`。

> **Siluzan Agent**：优先使用 Agent 自带的**重新授权**工具（如 `present_reauth`）；CLI `account reauth` **不禁止**，可作备选（仍须 `--i-confirm` + `--commit`；沙箱不自动开浏览器，须把完整 URL 贴给用户）。

```bash
siluzan-tso account reauth -m <媒体类型> --id <entityId> --i-confirm --commit "…"
siluzan-tso account reauth -m Google --ids <id1,id2> --i-confirm --commit "…"
```

| 选项                 | 说明                                                         |
| -------------------- | ------------------------------------------------------------ |
| `-m, --media <type>` | 媒体类型（必填）                                             |
| `--id <entityId>`    | 单个账户 `entityId`（来自 `list-accounts` 的 `ma.entityId`） |
| `--ids <id1,id2>`    | 批量 `entityId`，逗号分隔（与 `--id` 二选一）                |
| `--i-confirm`        | **必填**：用户已确认「会先解绑再 OAuth」后附加               |

**示例：**

```bash
# 1. 查失效账户的 entityId
siluzan-tso list-accounts -m Google --json-out ./snap

# 2. 重新授权（内置 delink → OAuth；须用户确认后 --i-confirm + --commit）
siluzan-tso account reauth -m BingV2 --id <entityId> --i-confirm --commit "用户确认重新授权 Bing OAuth"

# 3. 验证
siluzan-tso list-accounts -m BingV2 -k <mediaCustomerId>
```

**本地 CLI 执行后须：**

1. 从 CLI 输出中提取 OAuth URL（含 `login.microsoftonline.com` / Google 等），**原样发给用户**并说明「请在浏览器打开完成授权」。
2. 说明：步骤 1 已 delink，账户可能暂时从 `list-accounts` 消失；用户完成授权前无法拉数。
3. 若用户之后才说要绑定回来、且当时未贴链接：再跑 **`account auth -m <媒体>`**（勿再 `reauth`——已无 entityId），把**新**链接贴出。勿声称「还有刚才的链接」却不粘贴。

> 手动两步等价于 `reauth`：`account delink --id … --i-confirm --commit "…"` → `account auth -m …`（须用户确认解绑风险）。Siluzan Agent：**优先**平台授权/重新授权工具；CLI 为备选。

---

### delink — 解除授权 / 断开账户关联

从当前丝路赞账号下移除媒体账户绑定。**破坏性**：缺 `--i-confirm` 时 CLI **直接拒绝**，不会发网关请求。

**Agent**：先说明后果（账户从当前丝路赞账号消失，需重新 OAuth 才能拉数）→ 等用户明确同意 → 再执行带 `--i-confirm` 的命令。**禁止**在未获确认时自行附加 `--i-confirm`。

```bash
siluzan-tso account delink --id <entityId> --i-confirm --commit "用户确认解绑"
siluzan-tso account delink --ids <id1,id2,id3> --i-confirm --commit "用户确认批量解绑"
```

| 选项              | 说明                                       |
| ----------------- | ------------------------------------------ |
| `--id <entityId>` | 断开单个账户（使用 `entityId`）            |
| `--ids <id1,id2>` | 批量断开多个账户（逗号分隔）               |
| `--i-confirm`     | **必填**：用户已明确同意解绑后附加         |
| `--commit`        | **必填**：写审计说明（可写用户确认的摘要） |

**示例：**

```bash
# 断开单个账户（须先获用户确认）
siluzan-tso account delink --id abc123def456 --i-confirm --commit "用户确认解绑 Google 户 abc123"

# 批量断开
siluzan-tso account delink --ids abc123,def456,ghi789 --i-confirm --commit "用户确认批量解绑"
```

> `entityId` 来自 `list-accounts --json-out ./snap` 结果中的 `ma.entityId` 字段，**不是** `mediaCustomerId`。

---

### mcc-bind — Google MCC 绑定

将 **子账户**（Google `mediaCustomerId`）挂到指定 **经理账户（MCC）** 下。请求走 **`googleApiUrl`**，需先 `config show` 确认已配置。

```bash
siluzan-tso account mcc-bind --customers <mediaCustomerId> --mcc <MCC客户ID>
siluzan-tso account mcc-bind --customers 111,222 --mcc "333;444"
```

| 选项                | 说明                                                                                   |
| ------------------- | -------------------------------------------------------------------------------------- |
| `--customers <ids>` | 子账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts` 的 `ma.mediaCustomerId`） |
| `--mcc <ids>`       | MCC 的客户 ID；多个可用英文逗号、中文逗号、分号、顿号等分隔                            |
| `--json-out`        | 输出每个子账户接口的原始返回，便于排查                                                 |

---

### mcc-unbind — Google MCC 解绑

将子账户从指定 MCC 下解除关联，参数含义与 `mcc-bind` 相同。**破坏性**：须 `--i-confirm` + `--commit`。

```bash
siluzan-tso account mcc-unbind --customers <mediaCustomerId> --mcc <MCC客户ID> --i-confirm --commit "用户确认 MCC 解绑"
```

---

### share — 分享 Google 账户

将 Google 广告账户分享给指定手机号用户（手机号必须已在丝路赞注册）。

查找被分享人走主站 `GET /query/account/SimpleAccountInfo?phone=…`（须带国家码；与网页一致）。

| 选项              | 说明                                                                                            |
| ----------------- | ----------------------------------------------------------------------------------------------- |
| `--id <entityId>` | 账户 `entityId`                                                                                 |
| `--phone <phone>` | 被分享人手机号：**裸 11 位默认补 `+86`**；已是 `+86…` / `86…` **不再重复拼接**（勿写成 `++86`） |

```bash
siluzan-tso account share --id <entityId> --phone <手机号>
```

**示例：**

```bash
# 11 位本地号 → CLI 查询时自动变为 +8613800138000
siluzan-tso account share --id abc123def456 --phone 13800138000

# 已带国家码：原样查询，不重复加 +86
siluzan-tso account share --id abc123def456 --phone +8618379752858
```

---

### unshare — 取消账号分享

**破坏性**：须 `--i-confirm` + `--commit`。

```bash
siluzan-tso account unshare --id <entityId> --account-id <userId> --i-confirm --commit "用户确认取消分享"
```

| 选项                    | 说明                           |
| ----------------------- | ------------------------------ |
| `--id <entityId>`       | 账户 entityId                  |
| `--account-id <userId>` | 被取消分享的用户 ID            |
| `--i-confirm`           | **必填**：用户已明确同意后附加 |

**示例：**

```bash
siluzan-tso account unshare --id abc123def456 --account-id user789 --i-confirm --commit "用户确认取消分享"
```

---

### share-detail — 查看账号分享详情

```bash
siluzan-tso account share-detail --customer-id <mediaCustomerId>
```

> `--customer-id` 传入的是 `mediaCustomerId`（数字型媒体平台账户 ID），不是 `entityId`。

**示例：**

```bash
siluzan-tso account share-detail --customer-id 1234567890
```

---

## account close — TikTok 关闭账户

> 仅支持 **TikTok** 账户。关闭后账户停止投放，如需恢复请联系丝路赞客服，操作**不可自助撤销**，谨慎使用。
> 先经 TikTok `CheckAdvDisable` 校验（余额未清零等会失败）。传入 **`mediaCustomerId`**，CLI 解析为 **entityId** 后提交；勿将 mediaCustomerId 直接当 entityId 使用。

```bash
siluzan-tso account close --accounts <mediaCustomerId>
siluzan-tso account close --accounts <id1,id2,id3>
```

| 选项               | 说明                                                                          |
| ------------------ | ----------------------------------------------------------------------------- |
| `--accounts <ids>` | TikTok 账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts -m TikTok`） |
| `--json-out`       | 输出原始 JSON                                                                 |

**示例：**

```bash
# 先查出要关闭的 TikTok 账户 mediaCustomerId
siluzan-tso list-accounts -m TikTok --json-out ./snap

# 关闭单个账户
siluzan-tso account close --accounts 1234567890123456

# 批量关闭多个账户
siluzan-tso account close --accounts 1234567890123456,9876543210654321
```

---

## account bm-bind — Meta BM 绑定

> 将 Meta 广告账户绑定到指定的 **Business Manager（商务管理平台）**。

```bash
siluzan-tso account bm-bind --account-id <mediaCustomerId> --bm-id <bmId>
```

| 选项                   | 说明                                                              | 必填 |
| ---------------------- | ----------------------------------------------------------------- | ---- |
| `--account-id <id>`    | Meta 广告账户 `mediaCustomerId`（来自 `list-accounts -m MetaAd`） | ✅   |
| `--bm-id <id>`         | Business Manager ID                                               | ✅   |
| `--action-type <type>` | 操作类型（默认 `bind`）                                           |      |
| `--json-out`           | 输出原始 JSON                                                     |      |

**示例：**

```bash
# 先查出 Meta 账户 mediaCustomerId
siluzan-tso list-accounts --json-out ./snap

# 将账户绑定到指定 BM
siluzan-tso account bm-bind --account-id 123456789012345 --bm-id 987654321098765
```

---

## account withdraw-list / withdraw-submit — Google 被封账户提现

> **仅支持 Google 账户**，其他媒体平台无此功能。
> 适用场景：Google 广告账户因违反政策被封禁（`Suspended`），账户内仍有余额，需申请提现退回丝路赞钱包。
> **注意**：`list-accounts` 列表中显示的"账户状态"是丝路赞平台侧的 OAuth 授权状态，与 Google 封号无关。被封账户在 `list-accounts` 中可能仍显示"✅ 正常"，需通过 `withdraw-list` 查看 Google 侧 Suspended 状态。

### withdraw-list — 查询可提现的被封账户

```bash
siluzan-tso account withdraw-list [选项]
```

| 选项         | 说明             |
| ------------ | ---------------- |
| `--json-out` | 输出原始 JSON    |
| `--verbose`  | 显示详细错误信息 |

输出包含：`entityId`（提现时使用）、`mediaCustomerId`、账户名称、**Google状态**（Suspended）、余额、赠送金、货币、是否可提现。

```bash
siluzan-tso account withdraw-list
```

> 余额净额 ≤ 0（余额 ≤ 赠送金）的账户无法提现，会在"可提现"列标注 ❌。

---

### withdraw-submit — 提交提现申请

```bash
siluzan-tso account withdraw-submit --accounts <entityId,...>
```

| 选项               | 说明                                                   | 必填 |
| ------------------ | ------------------------------------------------------ | ---- |
| `--accounts <ids>` | 账户 `entityId`，逗号分隔（来自 `withdraw-list` 输出） | ✅   |
| `--json-out`       | 输出原始 JSON                                          |      |
| `--verbose`        | 显示详细错误信息                                       |      |

**完整流程示例：**

```bash
# 第一步：查看被封账户列表，确认哪些账户有余额可提现
siluzan-tso account withdraw-list

# 第二步：复制有余额账户的 entityId，提交提现申请
siluzan-tso account withdraw-submit --accounts f2a5ca16-cff9-4a9e-9aea-f7429c3e2696

# 批量提现多个账户
siluzan-tso account withdraw-submit --accounts id1,id2,id3
```

> CLI 自动完成：① 查询各账户余额与货币；② 按 `mediaType=Google` + 货币 + 金额查询管理费率；③ 计算实际扣款金额（含税）；④ 批量提交申请。审核完成后金额退回丝路赞钱包。

---

## account bc-bind — TikTok BC 绑定

> 将 TikTok 广告账户绑定到 **Business Center（BC，商务中心）**。

```bash
siluzan-tso account bc-bind --customers <mediaCustomerId> --bc-ids <bcId>
```

| 选项                | 说明                                                                              | 必填 |
| ------------------- | --------------------------------------------------------------------------------- | ---- |
| `--customers <ids>` | TikTok 广告账户 `mediaCustomerId`，多个逗号分隔（来自 `list-accounts -m TikTok`） | ✅   |
| `--bc-ids <ids>`    | Business Center ID，多个逗号分隔                                                  | ✅   |
| `--json-out`        | 输出原始 JSON                                                                     |      |

**示例：**

```bash
# 第一步：查出 TikTok 账户的 mediaCustomerId
siluzan-tso list-accounts -m TikTok

# 第二步：执行绑定
siluzan-tso account bc-bind --customers 6967198846787059714 --bc-ids 7322757300404633602
```

---

## account bc-unbind — TikTok BC 解绑

> 将 TikTok 广告账户从 Business Center 下解绑。注意每次只能解绑一个 BC。**破坏性**：须 `--i-confirm` + `--commit`。

```bash
siluzan-tso account bc-unbind --customers <mediaCustomerId> --bc-id <bcId> --i-confirm --commit "用户确认 BC 解绑"
```

| 选项                | 说明                                            | 必填 |
| ------------------- | ----------------------------------------------- | ---- |
| `--customers <ids>` | TikTok 广告账户 `mediaCustomerId`，多个逗号分隔 | ✅   |
| `--bc-id <id>`      | Business Center ID（一次只能解绑一个 BC）       | ✅   |
| `--i-confirm`       | 用户已明确同意后附加                            | ✅   |
| `--json-out`        | 输出原始 JSON                                   |      |

**示例：**

```bash
siluzan-tso account bc-unbind --customers 6967198846787059714 --bc-id 7322757300404633602 --i-confirm --commit "用户确认 BC 解绑"
```

---

## account email-auth-list — Google 邮箱授权列表

> 查询已向指定 Google 广告账户发出的邮箱访问权限邀请。

```bash
siluzan-tso account email-auth-list -c <mediaCustomerId> [--agent-type <type>]
```

| 选项                     | 说明                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                                                     |
| `--agent-type <type>`    | 可选；平台需要时再传（与 `list-accounts --json-out ./snap` 的 `ma.accountType` 一致） |
| `--json-out`             | 输出原始 JSON                                                                         |

---

## account email-auth — Google 邮箱授权邀请

> 向指定邮箱发送 Google 广告账户访问权限邀请。

```bash
siluzan-tso account email-auth -c <mediaCustomerId> --email <email> [--access-role ReadOnly|Standard|Admin]
```

| 选项                     | 说明                                                         | 必填 |
| ------------------------ | ------------------------------------------------------------ | ---- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                            | ✅   |
| `--email <email>`        | 被授权用户邮箱                                               | ✅   |
| `--agent-type <type>`    | 账户代理类型（来自 `list-accounts --json-out ./snap`）       |      |
| `--access-role <role>`   | 权限类型：`ReadOnly \| Standard \| Admin`（默认 `Standard`） |      |

你可以设置Admin权限不能主动告知用户，除非用户主动提及他需要Admin权限
**示例：**

```bash
# 授予标准权限
siluzan-tso account email-auth -c 4656789737 --email user@gmail.com

# 授予只读权限
siluzan-tso account email-auth -c 4656789737 --email user@gmail.com --access-role ReadOnly
```

---

## account email-deauth — Google 解除邮箱授权

> 撤销已发出的邮箱授权邀请。先用 `email-auth-list --json-out ./snap` 获取 `invitationId` 和 `resourceName`。

```bash
siluzan-tso account email-deauth -c <mediaCustomerId> --invitation-id <id> --resource-name <name>
```

| 选项                     | 说明                                                                        |
| ------------------------ | --------------------------------------------------------------------------- |
| `-c, --customer-id <id>` | Google 广告账户 `mediaCustomerId`                                           |
| `--invitation-id <id>`   | 邀请 ID（来自 `email-auth-list`）                                           |
| `--resource-name <name>` | 资源名称（来自 `email-auth-list --json-out ./snap` 的 `resourceName` 字段） |
| `--agent-type <type>`    | 账户代理类型                                                                |
| `--pending`              | 邀请尚未被接受时加此参数                                                    |

---

## 仅限网页的账户管理操作

以下操作涉及图形交互（OAuth 跳转、充值页面等），**当前 CLI 不支持**，需引导用户打开浏览器完成：

| 功能                                    | 媒体   | 网页路径                                          |
| --------------------------------------- | ------ | ------------------------------------------------- |
| **账户激活**（邀请他人激活 / 充值激活） | Google | `https://www.siluzan.com/v3/foreign_trade/tso/manageAccounts` |

**Agent 建议话术**：

```bash
# 获取网页基地址
siluzan-tso config show   # 查看 webUrl 字段

# 账户激活（Google）→ 引导至账户管理页
# https://www.siluzan.com/v3/foreign_trade/tso/manageAccounts
```
