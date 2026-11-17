# 临时体验 Key 申请流程（tempkey V2 完整指南）

当用户未配置 Key 时，按本文件完整流程引导用户申请 AI 场景临时体验 Key（有效期 1 年，PV=5000/天，QPS=5/秒）。

通过四个封装脚本（`scripts/` 目录）完成「发送验证码 → 创建/获取 Key →（可选）补额选择 → 持久化」全流程。
AI 负责：调用脚本 → 解析 JSON 输出 → 按错误码表查找话术展示给用户。
AI **不需要**自行拼接 HTTP 请求、生成 Header、写文件。

接口细节见 `references/api_reference.md`。

---

## 脚本说明

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/send_code.py` | 校验手机号格式 + 发送短信验证码 | `python3 scripts/send_code.py <phone>` |
| `scripts/create_key.py` | 校验验证码 + 创建/获取 Key（返回 created/reused/select 三种分支） | `python3 scripts/create_key.py <phone> <verify_code> <session_token>` |
| `scripts/supplement_key.py` | 补额/新建 Key（仅 create 返回 select 时调用） | `python3 scripts/supplement_key.py <supplement_token> reuse <mkey>` 或 `python3 scripts/supplement_key.py <supplement_token> create` |
| `scripts/save_config.py` | 持久化写入本地配置 / 标记过期 | `python3 scripts/save_config.py <phone> <key> <expire_time> [is_existing]` |

**本地配置文件路径：**
- macOS / Linux：`~/.tencentmap/tempkey.json`
- Windows：`%USERPROFILE%\.tencentmap\tempkey.json`

---

## 执行流程

### 第一步：展示协议，引导输入手机号

向用户展示以下内容，**不得跳过**：

```
根据腾讯位置服务的流程，我需要先向您展示相关协议，然后协助您创建 Key 并分配 AI 场景临时额度（有效期 1 年）。

📋 申请 Key 前，请阅读并同意以下协议：
《腾讯位置服务开放 API 服务协议》：https://rule.tencent.com/rule/0c5ee022-04cf-4614-a116-32d9f362552a
《腾讯位置服务隐私协议》：https://privacy.qq.com/document/preview/4cf61fd47f584dae83758bb0f11c1533

提供手机号即视为已阅读并同意以上协议。

请输入您的手机号：
```

### 第二步：调用 `send_code.py`

收到手机号后立即调用，无需二次确认：

```bash
python3 scripts/send_code.py <phone>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败（值即错误码） |
| `session_token` | string | 成功时返回，5 分钟有效 |
| `msg` | string | 失败时返回错误码字符串 |

**成功处理：**保存 `session_token`，向用户展示：
```
✅ 验证码已发送至 <手机号掩码，如 138****0000>，请注意查收。
验证码有效期为 5 分钟，请输入收到的 6 位验证码：
```

**失败处理（查下表）：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 500081 | "手机号格式不正确，请输入正确的 11 位中国大陆手机号：" | 等待重新输入 |
| 500072 | "发送过于频繁，请稍后重试。" | 结束 |
| 500073 | "该手机号今日发送验证码次数已达上限，请明日再试。" | 结束 |
| 500074 | "今日请求次数已达上限，请明日再试。" | 结束 |
| 500080 | "短信发送失败，请稍后重试。" | 结束 |
| 500070 | "请求异常，请重试。"（若用户要求重试，再次调用 `send_code.py`） | 等待用户操作 |
| 500071 | "请求已过期，请重试。"（若用户要求重试，再次调用 `send_code.py`） | 等待用户操作 |
| 2000 / 2999 | "系统请求参数异常，请重试；若反复出现请联系腾讯位置服务支持：lbs.qq.com" | 结束 |
| 3001 | "系统繁忙，请稍后重试。" | 结束 |
| -1 | "网络连接异常，请检查网络后重试。" | 结束 |

### 第三步：等待用户输入验证码

用户在对话框中回复 6 位验证码。

### 第四步：调用 `create_key.py`

```bash
python3 scripts/create_key.py <phone> <verify_code> <session_token>
```

> 使用第二步保存的 `session_token`；若用户重新发过验证码，必须用**最新一次** `send_code.py` 返回的 `session_token`，旧 token 作废。

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败（值即错误码） |
| `type` | string | 成功时返回：`created` / `reused` / `select` |
| `key` | string | type=created/reused 时返回，Key 值 |
| `expire_time` | string | type=created/reused 时返回，格式 `YYYY-MM-DD HH:MM:SS` |
| `is_existing` | bool | type=created/reused 时可能返回，true=幂等返回已有 Key |
| `key_list` | array | type=select 时返回，合适 Key 列表 |
| `supplement_token` | string | type=select 时返回，用于 supplement 接口 |
| `supplement_token_expire` | int | type=select 时返回，token 过期剩余秒数 |
| `msg` | string | 失败时返回错误码字符串 |

**失败处理：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 1008 | "验证码错误，请重新输入（还可尝试 X 次）："（X = 3 - verify_error_count，见下方计数规则） | AI 上下文计数；达到上限后提示"验证码已连续错误 3 次，session 已失效，请重新发送验证码"，清除 session_token 和计数器，引导回第二步 |
| 500075 | "验证码错误次数过多，session 已失效，请重新发送验证码。" | 清除 session_token 和 verify_error_count，引导回第二步；重发后**必须用新 session_token** |
| 1007 | "验证码已失效（超过 5 分钟），请重新发送验证码。" | 清除 session_token 和 verify_error_count，引导回第二步；重发后**必须用新 session_token** |
| 500084 | 使用「AI 场景临时额度已到期」模板（见下方） | 结束 |
| 500079 | "注册异常，请稍后重试。" | 结束 |
| 500083 | "该手机号正在创建 Key，请稍后重试。" | 结束 |
| 500070 | "请求异常，请重新输入验证码或重新发送验证码。" | 等待用户下一步输入，**不自动重试** |
| 500071 | "请求已过期，请重新输入验证码或重新发送验证码。" | 等待用户下一步输入，**不自动重试** |
| 2000 / 2999 | "系统请求参数异常，请重试；若反复出现请联系腾讯位置服务支持：lbs.qq.com" | 结束 |
| 3001 | "系统繁忙，请稍后重试。" | 结束 |
| -1 | "网络连接异常，请检查网络后重试。" | 结束 |

> **模型不对任何错误码做自动重试，所有失败均将控制权交还用户。**

**`verify_error_count` 计数规则（AI 在对话上下文中维护）：**

```
初始值：0（流程开始时或重新发送验证码后重置）

收到 error == 1008 时：
  verify_error_count += 1
  剩余次数 = 3 - verify_error_count

  if 剩余次数 > 0:
    提示："验证码错误，请重新输入（还可尝试 {剩余次数} 次）："
    等待用户输入新验证码
  else:
    提示："验证码已连续错误 3 次，session 已失效，请重新发送验证码。"
    清除 session_token，verify_error_count = 0
    引导回第二步

重新发送验证码后（无论何种原因触发）：
  verify_error_count = 0（必须重置）
```

### 第五步：根据 `type` 分支处理

#### 分支 A：`type=created`（新建 Key 或幂等返回）

直接进入第六步持久化。
- `is_existing=true` → 使用「幂等返回已有 Key」模板
- `is_existing` 不存在 → 使用「申请成功」模板

#### 分支 B：`type=reused`（幂等返回已补额的老 Key）

直接进入第六步持久化。使用「复用老 Key」模��。
> `is_existing` 固定为 true。

#### 分支 C：`type=select`（老用户有名下满足条件的 Key，需选择）

**保存 `supplement_token` 和 `key_list`。** 向用户展示：

```
检测到您名下有以下可扩容的 Key，请选择扩容方式：

1. 【<key_list[0].key_name>】 <key_list[0].key_value 掩码，如 AB3D-CDEF-****-****-OPQR>
2. 【<key_list[1].key_name>】 <key_list[1].key_value 掩码>
...

回复序号（1/2/...）→ 用对应 Key 扩容
回复「新建」   → 创建全新的 AI 场景专用 Key
```

**Key 值掩码规则：**展示前 8 位 + `****` + 后 4 位，如 `AB3D-CDEF-****-****-OPQR`。
> 注意：调用 `supplement_key.py` 时传**完整 Key 值**（从 `key_list` 取），不要传掩码。

**用户回复序号 N（1 ≤ N ≤ len(key_list)）：**

```bash
python3 scripts/supplement_key.py <supplement_token> reuse <key_list[N-1].key_value>
```

**用户回复「新建」：**

```bash
python3 scripts/supplement_key.py <supplement_token> create
```

**supplement_key.py 返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败（值即错误码） |
| `type` | string | `reused`（action=reuse）/ `created`（action=create） |
| `key` | string | Key 值 |
| `expire_time` | string | 格式 `YYYY-MM-DD HH:MM:SS` |
| `is_existing` | bool | type=reused 时为 true |
| `msg` | string | 失败时返回错误码字符串 |

**supplement 失败处理：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 1007 | "选择已失效（超过 5 分钟），请重新发送验证码开始。" | 清除所有 token，引导回第二步 |
| 500085 | "该 Key 不满足扩容条件，请选择其他 Key 或回复「新建」。" | 引导回选择步骤 |
| 500084 | 使用「AI 场景临时额度已到期」模板 | 结束 |
| 500086 | "额度配置失败，请稍后重试。" | 结束 |
| 500088 | "正在处理中，请稍后重试。" | 结束 |
| 500089 | "系统繁忙，请稍后重试。" | 结束 |
| 500070 | "请求异常，请重试。" | 等待用户操作 |
| 500071 | "请求已过期，请重试。" | 等待用户操作 |
| 2000 / 2999 | "系统请求参数异常，请重试；若反复出现请联系腾讯位置服务支持：lbs.qq.com" | 结束 |
| 3001 | "系统繁忙，请稍后重试。" | 结束 |
| -1 | "网络��接异常，请检查网络后重试。" | 结束 |

**supplement 成功后**进入第六步持久化：
- `type=reused` → 使用「复用老 Key」模板
- `type=created` → 使用「申请成功」模板

### 第六步：调用 `save_config.py` 并输出结果

```bash
python3 scripts/save_config.py <phone> <key> <expire_time> <is_existing>
```

> `is_existing` 传 `true` 或 `false`（对应脚本返回的 `is_existing`，无该字段时传 `false`）。

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_new` | bool | `true`=新建，`false`=复用已有 Key |
| `write_success` | bool | 文件是否写入成功 |
| `msg` | string | `write_success=false` 时返回失败原因 |

- `write_success=false` → 正常展示结果，在输出末尾附加：
  `⚠️ 本地记录保存失败，请检查文件权限：~/.tencentmap/tempkey.json`

---

## 输出模板

### 申请成功（type=created 且 is_existing 不存在）

```
🎉 您的腾讯位置服务 Key 已创建成功！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 您的 Key
<key>

📅 AI 场景临时额度有效期至
<expire_time 日��部分，格式 YYYY-MM-DD>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 已为您开通 AI 场景接口临时额度
   • 额度：PV=5000 次/天，QPS=5 次/秒
   • 有效期：1 年
   • 接口范围：WebService API（具体接口以控制台为准）

💡 使用方式
在腾讯位置服务 WebService API 请求中添加参数：
key=<您的 Key>

示例：https://apis.map.qq.com/ws/geocoder/v1/?address=北京市海淀区&key=<您的 Key>

📌 官方文档：https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
🚀 控制台：https://lbs.qq.com/dev/console/application/mine
📊 具体额���可登录控制台查看 Key 列表

⚠️ 重要提示
   AI 场景临时额度有效期为 1 年，请在 <expire_time 日期部分> 前完成测试。
   到期后如需继续使用，请前往 https://lbs.qq.com 分配正式额度或办理商业授权。
```

### 幂等返回已有 Key（type=created + is_existing=true）

```
✅ 检测到您已领取过 AI 场景 Key，无需重复申请。

🔑 您的 Key
<key>

📅 AI 场景临时额度有效期至
<expire_time 日期部分>
```

随后展示「额度+使用方式」部分（同申请成功模板）。

### 复用老 Key（type=reused 或 supplement action=reuse）

```
✅ 已为您的 Key 开通 AI 场景临时额度。

🔑 您的 Key
<key>

📅 AI 场景临时额度有效期至
<expire_time 日期部分>
```

随后展示「额度+使用方式」部分（同申请成功模板）。

### AI 场景临时额度已到期（error: 500084）

收到 500084 后，调用：
```bash
python3 scripts/save_config.py <phone> --mark-expired
```

脚本返回：`{"found": true/false, "expire_time": "..."}` 或 `{"found": false}`

- `found=true` → 展示本地记录中的过期时间
- `found=false` → 省略过期时间行

```
⏰ AI 场景临时额度已到期。

您的账号已使用过 AI 场景扩容机会，该 Key 的临时额度已到期。

如需继续使用腾讯位置服务，请前往官网分配可用额度或认证办理商业授权：
👉 https://lbs.qq.com/dev/console/application/mine
```

---

## 注意事项

1. **协议展示不可跳过**：无论何种触发场景，必须先展示协议后再收集手机号。
2. **禁止自动重试**：所有脚本调用失败（任何 error 码）均立即告知用户，将控制权交还用户，不做任何静默重试。
3. **session_token 即时更新**：每次重新发送验证码后，必须用新 `session_token` 覆盖旧值，同时 `verify_error_count` 重置为 0，严禁复用旧 token。
4. **验证码错误次数由 AI 维护**：`create_key.py` 不计数，AI 在对话上下文中用 `verify_error_count` 追踪；达到 3 次后停止调用脚本，引导用户重新发送验证码。
5. **手机号掩码展示**：对话中展示手机号时使用 `138****0000` 格式；本地文件中以明文手机号为 key（用于查询匹配）。
6. **Key 值掩码展示**：select 分支展示 key_list 时用掩码，但调用 `supplement_key.py` 时传完整 Key 值。
7. **持久化失败不阻断主流程**：`write_success=false` 时静默追加提示，Key 正常展示。
8. **is_existing 透传**：`create_key.py` / `supplement_key.py` 返回的 `is_existing` 需透传给 `save_config.py`，用于本地记录标记。
9. **supplement_token 有效期**：默认 300 秒，超时后需重新走完整流程（从发码开始）。
