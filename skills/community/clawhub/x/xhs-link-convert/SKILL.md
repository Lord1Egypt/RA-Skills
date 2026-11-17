---
name: xhs-convert-url-pro
version: 2.0.1
description: 小红书笔记链接批量转链工具。当用户提到小红书、转链、链接转换、xhslink，或要求把小红书笔记链接（含短链）转换为携带xsec_token的且浏览器可以直接打开观看的新链接时使用本 skill。转链结果可直接用于「小红书互动数采集」skill（xhs-dpt）。收费服务（1 条 = 1 点数，注册送 10 点）。
---

# 小红书转链 Skill（xhs-convert-url-pro）

封装「小红书转链服务」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交小红书链接 → 轮询任务 → 拿到转链后的 `new_url`（携带 `xsec_token`，浏览器可直接打开）。

与「小红书互动数采集」skill（`xhs-dpt`）同框架、同凭证、同输出规约：两个 skill 共用 `~/.xhs-platform/config.json`，登录一次两边通用，`logout` 会同时使两个 skill 失效。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、结果异常等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **每条有效转链 0.2 元**（每 1 点数抵扣 1 条 URL 的转换；无效链接不扣费）。
- 注册即送 **10 免费点数**；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖，无需 `npm install`）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
- 首次使用需先 `register --link`（注册即送 10 点数；用户手机微信扫码/点链接在网页完成，页面自带图形+短信验证码）或 `login --link`（已有账号）。成功后 token 自动保存到配置文件，后续调用免输。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（与采集 skill `xhs-dpt` 共用）。可用环境变量 `XHS_CONFIG_PATH` 覆盖（测试隔离用）。没有 token 或 token 失效时执行 `login --link` 重新登录即可。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示图形验证码，所以一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次调用加 `--base-url <url>` 覆盖。
- 环境变量：`XHS_CONFIG_PATH`（配置路径）、`XHS_PLATFORM_BASE_URL`（服务地址）、`XHS_PLATFORM_INSECURE=1`（忽略 HTTPS 证书校验）。
- 所有命令支持全局参数 `--token <token>`（临时覆盖配置文件中的 token）。
- `~/.xhs-platform/config.json` 含 token，**不要泄露、不要提交 git**。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。直接解析 stdout 即可。
- 交互提示、轮询进度一律走 **stderr**，不要解析。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

输出 skill 名、版本号、node 版本、配置文件路径。升级 skill 后建议先跑一次，确认版本号与预期一致。输出示例：

```json
{"ok":true,"data":{"name":"xhs-convert-url-pro","version":"2.0.0","node_version":"v22.22.2","config_path":"C:\\Users\\<user>\\.xhs-platform\\config.json"}}
```

### register — 注册（注册即送 10 点数）

```bash
node cli.js register --link        # 生成注册二维码/链接
node cli.js register --check --access-token "<上一步下发的串>"   # 用户完成后确认并保存 token
```

`register --link` 的 stdout 返回 `qr_url` / `register_url` / `access_token`。**agent 必须把注册引导原样发给用户**（stderr 里也给出了同样的话术，可直接复制）：

```text
需要先注册账号（注册即送 10 免费点数；不注册不登录没有点数，无法使用转链）。请用手机微信扫码或打开链接注册：

注册方式（二选一）
二维码图片：<qr_url>
注册链接：<register_url>
access_token（注册后校验用）：<access_token>
微信扫码/注册完成后告诉我一声，我会执行校验并保存凭证，然后继续之前的操作：
（注册/使用中如遇问题，请拨打客服电话 18722121663）
```

二维码/链接打开的页面支持发送短信验证码、设置密码，注册成功自动完成授权。用户说「注册完成」后，执行 `register --check --access-token "<access_token>"`：
- 成功：token 自动保存（与采集 skill 通用），返回 `quota_balance`，继续之前被中断的操作。
- `LOGIN_PENDING`：用户还没完成注册，提醒后再试。
- `LOGIN_EXPIRED`：会话过期（10 分钟）或已使用，重新执行 `register --link`。

`register --check` 成功输出示例：

```json
{"ok":true,"data":{"phone":"13800000000","quota_balance":10}}
```

### login — 登录

```bash
node cli.js login --link        # 生成登录二维码/链接
node cli.js login --check --access-token "<上一步下发的串>"   # 用户完成后确认并保存 token
```

`login --link` 的 stdout 返回 `qr_url` / `login_url` / `access_token`。**agent 必须把登录引导原样发给用户**（stderr 里也给出了同样的话术，可直接复制）：

```text
需要先登录。请用手机微信扫码或打开链接登录账号：

登录方式（二选一）
二维码图片：<qr_url>
登录链接：<login_url>
access_token（登录后校验用）：<access_token>
微信扫码/登录完成后告诉我一声，我会执行校验并保存凭证，然后继续之前的操作：
（注册/使用中如遇问题，请拨打客服电话 18722121663）
```

用户说「登录完成」后，执行 `login --check --access-token "<access_token>"`：
- 成功：token 自动保存（与采集 skill 通用），继续之前被中断的操作（如重新提交任务）。
- `LOGIN_PENDING`：用户还没完成授权，提醒用户完成后再试。
- `LOGIN_EXPIRED`：会话过期（10 分钟）或已使用，重新执行 `login --link`。

### quota — 查询点数

```bash
node cli.js quota
```

输出示例：

```json
{"ok":true,"data":{"id":1,"phone":"13800000000","nickname":"","quota":10,"role":"user","last_login_at":"","created_at":"2026-01-01T00:00:00"}}
```

### logout — 登出（切换账号）

```bash
node cli.js logout
```

服务端吊销当前 token 并清除本地保存的 token（**采集 skill 同步失效**）。之后可执行 `login --link` 登录其他账号。输出示例：

```json
{"ok":true,"data":{"logged_out":true}}
```

### submit — 提交转链任务

```bash
node cli.js submit --url "https://www.xiaohongshu.com/explore/6970ac3c000000000a03d7d5" \
                   --url "http://xhslink.com/o/pl4tP4IXRa"
node cli.js submit --file urls.txt            # 每行一条 URL，忽略空行与 # 注释行
node cli.js submit --file urls.txt --wait     # 提交后轮询等待终态（推荐）
```

- `--url` 可重复；`--file` 按行读取；二者可混合；总数 1~50 条。
- **链接支持**：`xiaohongshu.com/explore/<id>`、`/discovery/item/<id>`、`xhslink.com` 短链（服务端自动还原）。
- 每条自动生成递增 client_id（1, 2, 3...）；幂等键按 URL 内容派生（sha256 截断），同一批 URL 重试/重复提交由服务端幂等返回原任务、不重复扣费，内容变化自动换键。唯一例外：因服务端登录态失效整单失败且已全额返还的任务，重提同批链接会被服务端清理旧任务并**重新受理**，不会被幂等键挡住。

输出示例（不带 `--wait`）：

```json
{"ok":true,"data":{"task_id":"t_20260917_a1b2c3","total":2,"valid_count":2,"invalid_count":0,"charged":2,"quota_balance":8,"status":"pending"}}
```

带 `--wait` 时最终输出同 `query` 的完整结果（见下）。

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id>                          # 查一次
node cli.js query <task_id> --wait                   # 轮询直到终态
node cli.js query <task_id> --wait --interval 3 --timeout 300
```

- `--interval` 轮询间隔秒数（默认 2），`--timeout` 轮询总超时秒数（默认 120）。
- 终态：`done`（全部成功）/ `partial_failed`（部分失败）/ `failed`（全部失败）。轮询进度走 stderr，终态完整结果输出到 stdout。

终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20260917_a1b2c3","status":"done","total":2,"valid_count":2,"invalid_count":0,"success_count":2,"fail_count":0,"charged_quota":2,"refunded_quota":0,"items":[{"id":1,"url":"https://www.xiaohongshu.com/explore/6970ac3c000000000a03d7d5","note_id":"6970ac3c000000000a03d7d5","new_url":"https://www.xiaohongshu.com/explore/6970ac3c000000000a03d7d5?xsec_token=AB...","status":"success","fail_reason":""}]}}
```

**解读要点（agent 必读）**：
- `new_url` 是转换后的最终链接，**已携带 `xsec_token` 参数**，浏览器可直接打开。
- 条目 `status:"invalid"` 表示链接不合法（非笔记链接），不扣费，附 `fail_reason`。

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 与采集 skill 的协同（推荐工作流）

用户要"转链 + 采集"时，两个 skill 配合使用：

1. 用本 skill `submit --url <链接> ... --wait` 拿到带 `xsec_token` 的 `new_url` 列表。
2. 把 `new_url` 作为笔记链接传给采集 skill `xhs-dpt`：`node cli.js submit --url <new_url> --wait`（采集 skill 要求链接必须带 `xsec_token`，转链结果天然满足）。
3. 两个 skill 凭证通用：任一 skill `register --link` / `login --link` 后，另一个无需再登录。

## 典型工作流（agent 照此执行）

1. `node cli.js quota` — 确认剩余点数 ≥ 待提交有效 URL 数。
2. `node cli.js submit --url <url1> --url <url2> ... --wait` — 一步拿到终态结果（URL 较多时用 `--file`）。
3. 解析 stdout JSON：遍历 `data.items`，把 `status==="success"` 的 `new_url` 按原顺序整理返回给用户；对 `failed`/`invalid` 的条目附 `fail_reason` 说明。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 | 检查命令参数（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册过走 `register --link`（送 10 点数），已有账号走 `login --link`；把引导话术发给用户，完成后 `--check`（退出码 2） |
| LOGIN_PENDING | 用户尚未完成注册/登录 | 提醒用户完成微信扫码/链接操作后重试 `--check`（退出码 2） |
| LOGIN_EXPIRED | 会话过期/已使用 | 重新执行 `register --link` 或 `login --link`（退出码 2） |
| 2001 | 短信验证码错误或过期 | 引导用户在扫码打开的网页里重新获取并填写验证码 |
| 2003 | 需要图形验证码 | 登录/发短信每次都强制图形验证码（网页端操作）——终端无法完成，统一走 `register --link` / `login --link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 3002 | 超单次批量上限 | 拆分为 ≤50 条/批重新提交 |
| 3003 | 任务不存在 | 检查 task_id 是否属于当前账号 |
| 条目 fail_reason 含 `cookie_expired` / 登录态失效 | 服务端蒲公英登录态临时失效 | **点数已按条自动返还**（`refunded_quota` 体现）；告知用户属服务端临时故障、稍后**重新提交同一批链接**即可自动重新受理，无需改动 URL |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| TIMEOUT | 轮询超时 | 任务未结束，稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查后端服务与 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- 每条**有效** URL 扣 1 点数（提交时预扣）；无效链接（非笔记链接/格式错误）不扣费。
- 短链（xhslink）还原失败自动返还该条点数（`refunded_quota` 体现）。
- 转链服务登录态失效（服务侧临时故障）同样按条自动返还；由此整单失败且全额返还的任务，重提同一批链接会自动重新受理。
- 已进入转链服务后失败的条目（如笔记已删）**不返还**点数。

## 红线

- 仅处理**公开**小红书笔记链接的转换；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；服务端原因的失败如实透出（fail_reason）。
