---
name: xhs-profile
slug: xhs-user-profile
displayName: 小红书博主主页采集
version: 2.0.1
description: 小红书博主主页笔记采集工具（博主主页链接）。当用户需要采集某个小红书博主/达人/KOL 主页的全部笔记列表——标题、图文/视频类型、点赞数、发布时间、封面图、带 xsec_token 的笔记直链，做博主内容盘点、达人建联前调研、竞品账号监测、KOL 选号评估、导出笔记清单 CSV（Excel 直开），或提到"博主主页/达人笔记/UP主笔记列表/采集某个博主/主页笔记导出/达人内容盘点"时使用本 skill。**一页（30 条笔记）= 5 点数；整单预扣按页数、结算按实采量退差；会话模式建会话免费、每步一页 5 点、无更多不扣费；零结果/失败/博主被封均全额返还（注册送 10 点）。**
---

# 小红书博主主页笔记采集 Skill（xhs-profile）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用。输入**博主主页链接**，平台调度内网浏览器节点以真人滚动方式打开博主主页，SSR 首屏解析 + 拦截官方列表接口响应，采集该博主的笔记列表。

- **能采什么**：博主主页的笔记明细（`title` 标题、`note_type` 视频/图文、`liked_count` 点赞数、`publish_time` 发布时间、`cover_url` 封面图、`note_url` 带 xsec_token 的笔记直链、`sticky` 是否置顶）。
- **适用场景**：博主内容盘点、达人建联前调研、竞品账号监测、KOL 选号评估、批量取博主笔记链接（后续可接 xhs-dpt 采完整互动数 / xhs-comments 采评论）。
- **采集方式**：内网浏览器节点拟人滚动博主主页 + SSR 首屏解析 + 拦截官方接口（不调签名 API）；**列表接口只带点赞数，不含收藏/评论数**（需要完整互动数时，用采到的笔记直链走 xhs-dpt 逐篇采集）。
- **限制**：每任务 1 个博主；整单 1~10 页（每页 30 条）；会话模式不限页数、一页一页采；节点滚动每页约 5-10 秒。
- 采集由**平台调度内网浏览器节点**完成（节点登录态在浏览器端人工维护，平台不持有账号）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **一页（30 条笔记）= 5 点数**（1 点数 = 1 元以下优惠价请联系客服）。
- **整单模式**（`collect`）：**预扣** `页数 × 5`（如 3 页预扣 15 点）；**结算按实采量**：`ceil(实采条数/30) × 5`，差值自动返还（如 3 页只实采 45 条收 10 点——不满 30 条的零头按一页计）。
- **会话模式**（`session`）：**建会话免费**；每步进一页 = 5 点；已没有更多笔记时步进返回 `no_more` **不扣费**；博主昵称和笔记总数在第一个付费步返回。
- **全额返还**：博主暂无笔记（零结果）、节点离线超时、风控拦截、**博主被封或主页不可见**，点数全额退还。
- 注册即送 **10 免费点数**（可采 2 页 / 60 条）。点数不足时提示用户充值；充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 交互协议（agent 必须严格遵守）

本 skill 支持**两种模式**，按用户需求选择：

### 整单模式（用户明确要采 N 页 / 一次性采完）

1. **查余额**：`node cli.js quota` 确认点数充足（余额 < 预扣点数会被 3001 拒绝）。
2. **报价确认（必须）**：向用户明确以下信息并**等用户确认后**再提交：
   - 博主主页链接、采集页数（1~10 页，每页 30 条）
   - 预估点数：`页数 × 5`（例：3 页 → 15 点）
   - 计费规则：**预扣 页数×5，按实采 ceil(条数/30)×5 结算退差，零头按一页计，零结果/失败/博主被封全退**
   - **未经用户确认不要执行 collect。**
3. **提交并等待**：`node cli.js collect --url "<主页链接>" --pages <N> --wait --timeout 600`。节点滚动每页约 5-10 秒，不要中途重试。
4. **如实汇报结算**：结果里的 `collected_count`（实采条数）、`settle_charged`（实收点数）、`refunded_diff`（退还差值）必须如实告知用户。
5. **需要文件时导出**：`node cli.js export <task_id> --wait --out 博主笔记.csv`，把 CSV 路径交给用户。

### 会话模式（用户想一页一页看结果再决定要不要继续）

1. **建会话（免费）**：`node cli.js session start --url "<主页链接>"` → 拿到 `session_id`。
2. **逐页步进**：每次 `node cli.js session step <session_id>` 采一页（30 条 = 5 点），**步进前向用户确认扣 5 点**；返回本页笔记 + `has_more` + 博主昵称/笔记总数（首步）+ 余额。
3. **到底自动免费**：`no_more: true` 表示已采完，**不扣费**；引导用户 `session finish` 结束会话释放节点。
4. **随时拉取/导出**：`session notes <session_id>` 免费拉已采笔记；`session export <session_id> --out 文件.csv` 导出累计结果。
5. **注意**：会话空闲 20 分钟自动过期（节点释放），之后需重新建会话（已采数据仍在，`session notes/export` 仍可拉取）。

**链接要求**：`--url` 接受 `https://www.xiaohongshu.com/user/profile/<id>` 主页直链（可带 xsec_token 参数）或 xhslink 短链；**不接受笔记链接**（笔记互动数请用 xhs-dpt，评论请用 xhs-comments）。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
- 首次使用需先 `register --link`（注册即送 10 点数；用户手机微信扫码/点链接在网页完成，页面自带图形+短信验证码）或 `login --link`（已有账号）。成功后 token 自动保存，后续调用免输。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（升级/重装 skill 不丢配置）。可用环境变量 `XHS_CONFIG_PATH` 覆盖（测试隔离用）。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示，所以一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次加 `--base-url <url>` 覆盖。
- **⚠️ 安全提示（重要）**：默认服务地址是**明文 http**，token 会在公网明文传输。客户端每次请求都会在 stderr 提示。请知悉该风险；如环境允许，建议通过 `config set base-url https://...` 切换到 https 服务地址（需服务端已配好证书）。
- 所有命令支持全局参数 `--token <token>`（临时覆盖配置文件中的 token）。
- `~/.xhs-platform/config.json` 含 token，**不要泄露、不要提交 git**。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。直接解析 stdout 即可。
- 交互提示（如「请把预估点数报给用户确认」）一律走 **stderr**，不要解析，但其中给用户的引导话术应照做。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。
- `collect --wait` 单次最长 10 分钟（默认 600s 超时），属正常现象，不要中途重试。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"xhs-profile","version":"2.0.1","capability":"xhs_profile"}}
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

### collect — 提交整单主页采集任务

```bash
node cli.js collect --url "https://www.xiaohongshu.com/user/profile/5b4c369611be104d815b1ba9"                 # 默认 1 页 (30 条)
node cli.js collect --url "<主页链接>" --pages 3                    # 3 页 (约 90 条, 预扣 15 点)
node cli.js collect --url "<主页链接>" --pages 3 --wait             # 提交并等待结果
node cli.js collect --url "<主页链接>" --pages 3 --wait --timeout 600 --force
```

- `--url`：博主主页链接（`/user/profile/<id>` 直链或 xhslink 短链；填笔记链接会被拒绝）。
- `--pages`：采集页数 1~10（默认 1，每页 30 条）。
- `--wait`：等待任务终态再返回（推荐）；`--timeout` 轮询超时（默认 600s）；`--interval` 轮询间隔（默认 5s）。
- `--force`：跳过 24h 相同内容去重强制重提（幂等键混入时间戳）。

`--wait` 完成后的输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261012_ab12cd34","capability":"xhs_profile","status":"done",
 "success_count":1,"fail_count":0,"charged_quota":15,"refunded_quota":5,
 "items":[{"id":"1","payload":{"profile_url":"https://...","pages":3},
   "result":{"profile_url":"https://...","blogger_id":"5b4c...","blogger_nickname":"某博主",
             "requested_pages":3,"collected_count":62,
             "settle_charged":10,"refunded_diff":5,
             "notes":[{"note_id":"64ab...","title":"秋季穿搭合集",
                        "note_type":"normal","liked_count":"1.2万","publish_time":"2026-09-15",
                        "sticky":false,
                        "cover_url":"https://sns-webpic-qc.xhscdn.com/...",
                        "url":"https://www.xiaohongshu.com/explore/64ab...?xsec_token=...&xsec_source=pc_user"},
                       ...]},
   "status":"success"}]}}
```

**拿到结果后必须把 `collected_count` / `settle_charged` / `refunded_diff` 如实汇报给用户（见「交互协议」）。**

### query — 查询任务状态与结果

```bash
node cli.js query <task_id>            # 单次查询
node cli.js query <task_id> --wait     # 轮询到终态 (默认 600s 超时)
```

### export — 导出整单结果 CSV

```bash
node cli.js export <task_id> --wait --out 博主笔记.csv
```

下载任务结果 CSV（BOM 头，Excel 直开不乱码）：任务汇总（主页链接/博主/状态/请求页数/实采数/实收点数/退差点数）+ 笔记明细（标题/类型/点赞数/发布时间/置顶/封面/笔记直链）。导出文件保留 7 天。

### session — 会话模式（一页一页采）

```bash
node cli.js session start --url "<主页链接>"     # 建会话 (免费), 返回 session_id
node cli.js session step <session_id>            # 步进一页 (30 条 = 5 点; no_more 不扣费)
node cli.js session status <session_id>          # 会话状态/累计统计/余额
node cli.js session list [--status active]       # 会话列表
node cli.js session notes <session_id> [--page 2]  # 已采笔记分页拉取 (免费)
node cli.js session export <session_id> --out 博主笔记.csv  # 累计结果 CSV (免费)
node cli.js session finish <session_id>          # 主动结束 (释放节点)
```

`session step` 输出示例：

```json
{"ok":true,"data":{"no_more":false,"type":"page","page_no":1,
 "notes":[{"note_id":"64ab...","title":"...","note_type":"video","liked_count":"890",
           "publish_time":"2026-10-01","sticky":false,"cover_url":"...","url":"https://..."},...],
 "has_more":true,"nickname":"某博主","note_total":"135",
 "pages_collected":1,"notes_collected":30,"charged_steps":1,"quota_balance":5}}
```

- 首步返回 `nickname`（博主昵称）和 `note_total`（笔记总数，供估算总页数）。
- `has_more: false` 后再次 step 返回 `no_more: true`，**不扣费**。
- 会话空闲 20 分钟自动过期；`session finish` 主动结束（幂等）。

### logout — 登出（切换账号）

```bash
node cli.js logout
```

### config — 配置管理

```bash
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show        # token 脱敏显示
```

## 典型工作流（agent 照此执行）

1. 用户说「帮我采集这个博主的主页笔记」→ `node cli.js quota` 确认余额。
2. 和用户确认模式：
   - 知道要采多少 → 整单：确认页数，算预估点数 `页数×5`，**明确告知计费规则（预扣/结算退差/零头按一页计/零结果失败被封全退）并等确认** → `collect --url <链接> --pages N --wait`。
   - 想边采边看 → 会话：`session start`（免费）→ 逐次 `session step`（每步前确认扣 5 点）→ `no_more` 或用户说停 → `session finish`。
3. 如实汇报：实采条数、实收点数、退差点数；简要展示笔记列表（标题/点赞数/发布时间）。
4. 用户要文件 → `export <task_id> --wait --out <文件>.csv` 或 `session export <session_id> --out <文件>.csv`，交付路径。
5. 用户要继续分析 → 基于笔记直链（带 xsec_token）用 xhs-dpt 采完整互动数（含收藏/评论/分享数）或 xhs-comments 采评论。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 链接无效（非主页链接）| 检查链接形态；笔记链接引导用 xhs-dpt / xhs-comments（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| TIMEOUT | 等待超时（任务仍在跑） | 任务未丢：稍后 `query <task_id>` 查终态；预扣仍在，终态后按实采结算 |
| 5001 | 采集服务暂不可用（无在线主页节点/超时/风控） | 点数已全额返还；稍后重试；持续不可用提示联系客服 18722121663 |
| 5001（博主被封/主页不可见） | 「该账户违反《社区规范》其内容无法查看」或主页 404 | 点数已全额返还；如实告知用户该博主无法采集，不要重试同一链接 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- **免费**：quota / query / session status|list|notes|export / config，以及参数校验拒绝的请求；会话 `session start` 建会话免费；`no_more` 步进免费。
- **预扣（整单）**：`页数 × 5`，提交成功立即扣除。
- **结算退差（整单）**：任务成功后按 `ceil(实采条数/30) × 5` 实收，差值自动返还（`refunded_diff`）；实采多于请求量时不多收（封顶预扣额）。
- **按步扣费（会话）**：每次成功步进一页扣 5 点，扣费前会检查是否还有下一页（没有则免费返回 `no_more`）。
- **全额返还**：零结果（博主暂无笔记）、节点离线/超时、风控/登录拦截、博主被封或主页不可见。
- **置顶笔记**：置顶笔记可能跨页重复出现，已自动去重，实采条数以去重后为准（退差随之准确）。

## 红线

- 仅采集**公开**博主主页数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功或具体条数；风控/博主笔记不足时如实透出（点数按实采结算，用户不损失）。
- 笔记列表含博主公开昵称、发布时间等信息：**仅用于用户已授权或公开可获取的调研/分析场景**，遵守平台与数据合规要求；不在未授权场景下转售、滥用；CSV 导出文件请告知用户自行妥善保管。
