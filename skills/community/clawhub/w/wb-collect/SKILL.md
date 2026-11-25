---
name: wb-collect
slug: wb-hudongshu
displayName: 微博主帖采集
version: 1.0.0
description: 微博主帖采集工具。当用户需要采集/查询某条微博的正文、作者、发布时间、转发数、评论数、点赞数，提交一批微博主帖链接一键批量采集、导出采集结果 CSV（Excel 直开），或提到"微博采集/主帖采集/微博正文/转发数/评论数/点赞数/社媒指数"时使用本 skill。适合微博投放结案、内容数据盘点、活动效果监测、爆款内容分析、达人微博分析等场景。支持 weibo.com/<用户ID>/<微博ID>、/detail/<mid> 直链与 t.cn 短链。收费服务（1 条微博 = 1 点数，注册送 10 点）。
---

# 微博主帖采集 Skill（wb-collect）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交微博主帖链接 → 平台调度内网浏览器节点调用 `/ajax/statuses/show?isGetLongText=true` → 拿到该条微博的**正文、作者、发布时间、转发 / 评论 / 点赞**三项计数。批量采集，结果直接导出 CSV（BOM 头，Excel 直开不乱码）。

- **能采什么**：正文（`title`/`text`，长文直接拿全文，无需点「展开」）、作者昵称与 ID、发布时间（`create_time`）、转发数（`share_count`）、评论数（`comment_count`）、点赞数（`like_count`）、微博 ID（`post_id`）与 bid、原帖链接。
- **适用场景**：微博投放结案、内容数据盘点、活动效果监测、爆款内容分析、达人微博分析等。
- **省心机制**：批量采（单次 1~50 条）、无效链接不扣费、服务侧失败按条自动返还点数（详见「计费规则提示」）、Agent 友好（stdout 纯 JSON + 统一退出码）。
- **不采集评论正文**。需要评论内容请改用评论采集 skill `wb-comments`（会话制，按步计费）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **每条有效微博 0.1 元**（每 1 点数抵扣 1 条微博的采集；无效链接不扣费）。
- 注册即送 **10 免费点数**（可采集 10 条微博）；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 链接要求（重要，提交前必读）

**本 skill 只接受微博主帖链接**，这是硬性要求（客户端提交前会做本地预检——域名白名单与路径格式检查，不通过直接报错、不扣费；服务端还会做更严格校验，未通过的条目判 `invalid` 不计费）：

1. **支持的链接形态**：
   - `https://weibo.com/2153789604/RoCNr3H8I`（`<用户ID>/<微博ID>`，最常见）
   - `https://weibo.com/detail/5358690090880816`（`/detail/<mid>`，mid 为纯数字微博 ID）
   - `https://weibo.com/status/5358690090880816`（`/status/<mid>`）
   - `https://t.cn/<短码>`（**短链直接提交即可**，采集节点浏览器打开后自动跳转还原，无需人工转换）

2. **用户主页链接（`weibo.com/u/<用户ID>`）不要提交本 skill**：主页微博列表采集请用 `wb-profile` skill；评论采集请用 `wb-comments` skill。传了主页链接会被识别并提示改用什么 skill，不会误扣费。

3. 提交前逐条检查链接；批量场景中只要有一条不合规，本 skill 会拒绝整批提交并列出问题条目（不会部分扣费）。

> agent 工作流提示：拿到用户给的链接后先判断形态；`t.cn` 短链直接提交即可，不要反复试错浪费轮次。带 `?xxx=` 查询串的直链同样支持。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
- 首次使用需先 `register --link`（注册即送 10 点数；用户手机微信扫码/点链接在网页完成，页面自带图形+短信验证码）或 `login --link`（已有账号）。成功后 token 自动保存，后续调用免输。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（升级/重装 skill 不丢配置；与小红书/抖音/快手/B站系列 skill 共用同一账号体系）。可用环境变量 `XHS_CONFIG_PATH` 覆盖（测试隔离用）。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示，所以一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次加 `--base-url <url>` 覆盖。
- **⚠️ 安全提示（重要）**：默认服务地址是**明文 http**，token 会在公网明文传输。客户端每次请求都会在 stderr 提示。请知悉该风险；如环境允许，建议通过 `config set base-url https://...` 切换到 https 服务地址（需服务端已配好证书）。
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

```json
{"ok":true,"data":{"name":"wb-collect","version":"1.0.0","capability":"wb_collect"}}
```

### register — 注册（注册即送 10 点数）

**方式一：扫码/链接注册（唯一方式，用户在手机上完成）**

```bash
node cli.js register --link        # 生成注册二维码/链接
node cli.js register --check --access-token "<上一步下发的串>"   # 用户完成后确认并保存 token
```

`register --link` 的 stdout 返回 `qr_url` / `register_url` / `access_token`。**agent 必须把注册引导原样发给用户**（stderr 里也给出了同样话术，可直接复制）：

```text
需要先注册账号（注册即送 10 免费点数；不注册不登录没有点数，无法采集）。请用手机微信扫码或打开链接注册：

注册方式（二选一）
二维码图片：<qr_url>
注册链接：<register_url>
access_token（注册后校验用）：<access_token>
微信扫码/注册完成后告诉我一声，我会执行校验并保存凭证，然后继续之前的操作：
（注册/使用中如遇问题，请拨打客服电话 18722121663）
```

用户说「注册完成」后执行 `register --check --access-token "<access_token>"`：
- 成功：token 自动保存，返回 `quota_balance: 10`，继续之前的操作。
- `LOGIN_PENDING`：用户还没完成注册，提醒后再试。
- `LOGIN_EXPIRED`：会话过期（10 分钟）或已使用，重新执行 `register --link`。

### login — 登录

```bash
node cli.js login --link
node cli.js login --check --access-token "<上一步下发的串>"
```

引导话术同 register（把"注册"换成"登录"）。成功后 token 自动保存。

### quota — 查询点数

```bash
node cli.js quota
```

```json
{"ok":true,"data":{"quota":10,...}}
```

### logout — 登出（切换账号）

```bash
node cli.js logout
```

### submit — 提交采集任务

```bash
node cli.js submit --url "https://weibo.com/2153789604/RoCNr3H8I" \
                   --url "https://weibo.com/detail/5358690090880816"
node cli.js submit --file urls.txt            # 每行一条微博链接, 忽略空行与 # 注释行
node cli.js submit --file urls.txt --wait     # 提交后轮询等待终态（推荐）
node cli.js submit --url <链接> --force       # 跳过 24h 内容去重强制重提
```

- `--url` 可重复；`--file` 按行读取；二者可混合；总数 1~50 条。
- 每条自动生成递增 client_id；幂等键按链接内容派生，同批重试不重复扣费；同一用户同一微博 24h 内默认去重（防重复扣费），`--force` 可强制重提。

输出示例（不带 `--wait`）：

```json
{"ok":true,"data":{"task_id":"t_20261029_c6c377b1","total":2,"valid_count":2,"invalid_count":0,"charged":2,"quota_balance":8,"status":"pending"}}
```

带 `--wait` 时最终输出同 `query` 的完整结果。

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id>                          # 查一次
node cli.js query <task_id> --wait                   # 轮询直到终态
node cli.js query <task_id> --wait --interval 3 --timeout 300
```

- `--interval` 轮询间隔秒数（默认 2），`--timeout` 总超时秒数。
- 终态：`done`（全部成功）/ `partial_failed`（部分失败）/ `failed`（全部失败）。

终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261029_08b4caae","status":"done","success_count":1,"fail_count":0,
 "items":[{"id":1,"video_url":"https://weibo.com/2153789604/RoCNr3H8I","status":"success",
   "result":{"post_id":"5358690090880816","bid":"RoCNr3H8I",
             "title":"好不容易追回我老婆！竟然劝我离婚！",
             "share_count":"94","comment_count":"279","like_count":"3450",
             "create_time":"2026-10-27 17:53",
             "url":"https://weibo.com/2153789604/RoCNr3H8I"}}]}}
```

**解读要点（agent 必读）**：
- 三个计数是**字符串**；**空串 = 该指标未采集到**（页面未渲染/被拦截），不是 0——向用户解读时注意区分。
- `comment_count` 是页面显示的评论总数，与实际可采集到的条数常常不一致（微博接口会过滤），这是正常现象。
- 失败条目的 `fail_reason` 会透出具体原因（微博不存在/已删除/无权限查看等）。

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out out.csv
```

生成两段式 CSV（BOM 头，Excel 直开不乱码）：任务汇总 + 微博主帖明细（正文/三项计数/作者/时间）。适合把结果直接交给用户。

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 典型工作流（agent 照此执行）

1. 检查每条链接形态（`<用户ID>/<微博ID>`、`/detail/<mid>` 直链或 `t.cn` 短链均可直接提交；主页链接引导改用 `wb-profile`）。
2. `node cli.js quota` — 确认剩余点数 ≥ 待采集条数。
3. `node cli.js submit --url <链接1> --url <链接2> ... --wait` — 一步拿到终态结果（条数多时用 `--file`）。
4. 解析 stdout JSON：遍历 `data.items`，把 `status==="success"` 条目的 `result` 整理成表格返回给用户；`failed`/`invalid` 条目附 `fail_reason` 说明。
5. 用户要文件时：`node cli.js export <task_id> --wait --out 微博数据.csv`，把 CSV 路径交给用户。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / **链接校验未通过** | 消息里逐条列出问题链接：主页链接改用 `wb-profile`；非官方域名替换正确链接后重提（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 3002 | 超单次批量上限 | 拆分为 ≤50 条/批重新提交 |
| 3003 / 3004 | 任务或导出不存在 | 检查 task_id / export_id 是否属于当前账号 |
| 条目 `invalid` | 链接不合法 / 24h 内重复 | 按 fail_reason 提示；重复提交可 `--force` |
| 任务 `partial_failed` | 部分条目失败 | fail_reason 已透出；服务侧/风控原因失败的条目点数已自动返还，可稍后重提 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| TIMEOUT | 轮询超时 | 任务未结束，稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- 提交时按**有效微博条数预扣**（1 条 = 1 点数）；无效链接（非官方域名/格式错误）不扣费。
- **自动返还**：服务侧故障（无在线微博节点/超时/风控拦截）等未采集到数据的条目，点数按条自动返还（`refunded_quota` 体现），可稍后重提。
- **不返还**：微博不存在、已删除或无权限查看属业务性失败，不返还。
- 同一用户同一微博 24h 内默认去重；`--force` 强制重提会正常扣费。

## 红线

- 仅采集**公开**微博数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出（fail_reason）。
