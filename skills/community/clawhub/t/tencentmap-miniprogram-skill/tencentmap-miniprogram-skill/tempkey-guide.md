# 临时体验 Key 申请流程（tempkey 完整指南）

当用户未配置 Key 时，按本文件完整流程引导用户申请临时体验 Key。

## 脚本说明

三个封装脚本位于本 skill 的 `scripts/` 目录：

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `send_code.py` | 校验手机号格式 + 发送短信验证码 | `python scripts/send_code.py <phone>` |
| `create_key.py` | 校验验证码格式 + 创建 Key | `python scripts/create_key.py <phone> <verify_code> <session_token>` |
| `save_config.py` | 持久化写入本地配置 / 标记过期 | `python scripts/save_config.py <phone> <key> <expire_time>` |

**本地配置文件路径：**
- macOS / Linux：`~/.tencentmap/tempkey.json`
- Windows：`%USERPROFILE%\.tencentmap\tempkey.json`

---

## 执行流程

### 第一步：展示协议，引导输入手机号

向用户展示以下内容，**不得跳过**：

```
根据腾讯位置服务的流程，我需要先向您展示相关协议，然后协助您创建 Key 并分配体验额度。

📋 申请 Key 前，请阅读并同意以下协议：
《腾讯位置服务开放 API 服务协议》：https://rule.tencent.com/rule/0c5ee022-04cf-4614-a116-32d9f362552a
《腾讯位置服务隐私协议》：https://privacy.qq.com/document/preview/4cf61fd47f584dae83758bb0f11c1533

提供手机号即视为已阅读并同意以上协议。

请输入您的手机号：
```

### 第二步：调用 `send_code.py`

收到手机号后立即调用，无需二次确认：

```bash
python scripts/send_code.py <phone>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败 |
| `session_token` | string | 成功时返回，5 分钟有效 |
| `msg` | string | 失败时返回错误描述 |

**成功处理：**保存 `session_token`，向用户展示：
```
✅ 验证码已发送至 <手机号掩码，如 138****0000>，请注意查收。
验证码有效期为 5 分钟，请输入收到的 6 位验证码：
```

**失败处理（查下表）：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 500081 | "手机号格式不正确，请输入正确的 11 位中国大陆手机号：" | 等待重新输入 |
| 500082 | "您已注册过腾讯位置服务，请您前往 https://lbs.qq.com/dev/console/application/mine 使用正式 Key 进行相关操作。" | 结束（直接展示，不再继续申请流程） |
| 500072 | "发送过于频繁，请稍后重试。"（接口渐进冷却：60s/120s/300s，Agent 无法得知次数，统一提示） | 结束 |
| 500073 | "该手机号今日发送验证码次数已达上限，请明日再试。" | 结束 |
| 500074 | "今日请求次数已达上限，请明日再试。" | 结束 |
| 500080 | "短信发送失败，请稍后重试。" | 结束 |
| 500070 | "请求异常，请重试。"（若用户要求重试，再次调用 `send_code.py`） | 等待用户操作 |
| 500071 | "请求已过期，请重试。"（若用户要求重试，再次调用 `send_code.py`） | 等待用户操作 |
| 2000 | "系统请求参数异常，请重试；若反复出现请联系腾讯位置服务支持：lbs.qq.com" | 结束 |
| -1 | "网络连接异常，请检查网络后重试。" | 结束 |

### 第三步：等待用户输入验证码

用户在对话框中回复 6 位验证码。

### 第四步：调用 `create_key.py`

```bash
python scripts/create_key.py <phone> <verify_code> <session_token>
```

> 使用第二步保存的 `session_token`；若用户重新发过验证码，必须用**最新一次** `send_code.py` 返回的 `session_token`，旧 token 作废。

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `error` | int | 0=成功，其他=失败 |
| `key` | string | 成功时返回 Key |
| `expire_time` | string | 成功时返回，格式 `YYYY-MM-DD HH:MM:SS` |
| `msg` | string | 失败时返回错误描述 |

**失败处理：**

| error | 向用户说的话 | 后续动作 |
|-------|-------------|----------|
| 2003 | "验证码错误，请重新输入（还可尝试 X 次）："（X = 3 - verify_error_count，见下方计数规则） | AI 上下文计数；达到上限后停止调脚本，提示"验证码已连续错误 3 次，session 已失效，请重新发送验证码"，清除 session_token 和计数器，引导回第二步 |
| 500075 | "验证码错误次数过多，session 已失效，请重新发送验证码。" | 清除 session_token 和 verify_error_count，引导回第二步；重发后**必须用新 session_token** |
| 2002 | "验证码已失效（超过 5 分钟），请重新发送验证码。" | 清除 session_token 和 verify_error_count，引导回第二步；重发后**必须用新 session_token** |
| 500078 | 使用「体验额度已过期」模板（见下方） | 结束 |
| 500076 | "该手机号今日创建 Key 次数已达上限，请明日再试。" | 结束 |
| 500077 | "今日请求次数已达上限，请明日再试。" | 结束 |
| 500079 | "注册异常，请稍后重试。" | 结束 |
| 500070 | "请求异常，请重新输入验证码或重新发送验证码。" | 等待用户下一步输入，**不自动重试** |
| 500071 | "请求已过期，请重新输入验证码或重新发送验证码。" | 等待用户下一步输入，**不自动重试** |
| 2000 | "系统请求参数异常，请重试；若反复出现请联系腾讯位置服务支持：lbs.qq.com" | 结束 |
| -1 | "网络连接异常，请检查网络后重试。" | 结束 |

> **模型不对任何错误码做自动重试，所有失败均将控制权交还用户。**

**`verify_error_count` 计数规则（AI 在对话上下文中维护）：**

```
初始值：0（流程开始时或重新发送验证码后重置）

收到 error == 2003 时：
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

### 第五步：调用 `save_config.py` 并输出结果

```bash
python scripts/save_config.py <phone> <key> <expire_time>
```

**脚本返回字段：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `is_new` | bool | `true`=新建，`false`=复用已有 Key |
| `write_success` | bool | 文件是否写入成功 |
| `msg` | string | `write_success=false` 时返回失败原因 |

- `is_new=true` → 使用「申请成功」模板
- `is_new=false` → 使用「复用已有 Key」模板
- `write_success=false` → 正常展示结果，在输出末尾附加：
  `⚠️ 本地记录保存失败，请检查文件权限：~/.tencentmap/tempkey.json`

---

## 输出模板

### 申请成功（`is_new=true`）

```
🎉 您的腾讯位置服务 Key 已创建成功！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 您的 Key
<key>

📅 体验额度有效期至
<expire_time 日期部分，格式 YYYY-MM-DD>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 本 Key 已开通以下 24 个 WebService API（PV=5000/天，QPS=5/秒）：

| # | 接口名称 | # | 接口名称 |
|---|----------|---|----------|
| 1 | 坐标转换 | 2 | 行政区划列表 |
| 3 | 行政区划子级查询 | 4 | 逆地址解析 |
| 5 | IP 定位 | 6 | 地点搜索 |
| 7 | 关键词输入提示 | 10 | 静态图 |
| 38 | 行政区划搜索 | 78 | 驾车路线规划 |
| 79 | 步行路线规划 | 80 | 公交路线规划 |
| 83 | 地址解析 | 93 | POI 详情 |
| 96 | 距离矩阵驾车 | 100 | 骑行路线规划 |
| 118 | 距离矩阵骑行 | 124 | 周边 POI 推荐 |
| 132 | 步行距离矩阵 | 204 | 电动车路线规划 |
| 238 | 智能硬件定位 | 275 | 多边形区域搜索 |
| 303 | 天气 | 323 | 直线距离矩阵 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 使用方式
在腾讯位置服务 WebService API 请求中添加参数：
key=<您的 Key>

示例：https://apis.map.qq.com/ws/geocoder/v1/?address=北京市海淀区&key=<您的 Key>

📌 官方文档：https://lbs.qq.com/service/webService/webServiceGuide/webServiceOverview
🚀 控制台：https://lbs.qq.com/dev/console/application/mine

⚠️ 重要提示
   已为您分配体验额度，请在 <expire_time 日期部分> 前完成测试。
   测试完成后，请前往 https://lbs.qq.com 分配正式额度以供正式上线使用。
```

### 复用已有 Key（`is_new=false`）

```
ℹ️ 您已有一个有效的 Key，无需重复申请。

🔑 您的 Key
<key>

📅 体验额度有效期至
<expire_time 日期部分>
```

随后展示配额列表和使用方式（同申请成功模板的「配额+使用方式」部分）。

### 体验额度已过期（error: 500078）

收到 500078 后，调用：
```bash
python scripts/save_config.py <phone> --mark-expired
```

脚本返回：`{"found": true/false, "expire_time": "..."}` 或 `{"found": false}`

- `found=true` → 展示本地记录中的过期时间
- `found=false` → 省略过期时间行

```
⏰ 您的 Key 体验额度已过期。
[found=true 时显示] 过期时间：<expire_time 日期部分>

体验额度到期后已自动停用。

如需继续使用腾讯位置服务，请前往官网分配正式额度：
👉 https://lbs.qq.com/dev/console/application/mine
```

---

## 注意事项

1. **协议展示不可跳过**：无论何种触发场景，必须先展示协议后再收集手机号。
2. **禁止自动重试**：所有脚本调用失败（任何 error 码）均立即告知用户，将控制权交还用户，不做任何静默重试。
3. **session_token 即时更新**：每次重新发送验证码后，必须用新 `session_token` 覆盖旧值，同时 `verify_error_count` 重置为 0，严禁复用旧 token。
4. **验证码错误次数由 AI 维护**：`create_key.py` 不计数，AI 在对话上下文中用 `verify_error_count` 追踪；达到 3 次后停止调用脚本，引导用户重新发送验证码。
5. **手机号掩码展示**：对话中展示手机号时使用 `138****0000` 格式；本地文件中以明文手机号为 key（用于查询匹配）。
6. **持久化失败不阻断主流程**：`write_success=false` 时静默追加提示，Key 正常展示。
