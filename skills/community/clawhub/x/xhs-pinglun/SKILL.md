---
name: xhs-comments
slug: xhs-pinglun
displayName: 小红书评论分步采集
version: 2.0.1
description: 小红书笔记评论分步采集工具（用户洞察，会话制）。当用户需要采集/查询小红书笔记的评论内容——昵称、评论正文、点赞数、IP 属地、子评论数，按页逐步采集并实时返回给用户、可按需展开子评论、导出评论明细 CSV（Excel 直开），或提到"小红书评论采集/评论内容/评论抓取/用户评论/评论导出/舆情/笔记评论"时使用本 skill。适合评论区舆情监测、用户反馈收集、爆款笔记评论洞察、KOL 粉丝声音分析等场景。**转链与互动数采集免费；每采一页主评论或展开一次子评论扣 1 点数（注册送 10 点）。**
---

# 小红书评论分步采集 Skill（xhs-comments v2）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用。v2 起改为**分步会话制**：先免费拿到笔记评论总数 → 用户确认后按页/按展开逐步计费采集，每一步的结果立即返回给你展示给用户。

- **能采什么**：公开笔记的评论明细（`nickname` 昵称、`content` 评论正文、`like_count` 点赞数、`ip_location` IP 属地、`sub_count` 子评论数、`comment_id` / `root_comment_id`）。主评论每页 10 条（含 0~2 条内嵌子评论预览）；子评论点一次展开约 5 条。
- **适用场景**：评论区舆情监测、用户反馈收集、爆款笔记评论洞察、KOL 粉丝声音分析、竞品笔记评论对比。
- **计费模型（与 v1 不同）**：建会话（含自动转链补 xsec_token + 互动数采集）**免费**；之后**每执行一步扣 1 点数**——「采一页主评论」是一步，「对某条主评论展开一次子评论」也是一步。
- **省心机制**：无效链接不建会话不扣费、采到底/no_more 的步不扣费、服务侧失败自动返还当步点数、Agent 友好（stdout 纯 JSON + 统一退出码）。
- 采集由**平台调度内网浏览器节点**完成（节点登录态在浏览器端人工维护，平台不持有账号）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题（注册失败、点数充值、采集结果异常、批量采购等），请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **每步采集 0.2 元**（1 点数 = 1 步：一页主评论 10 条，或一次子评论展开约 5 条）。
- 建会话（转链 + 互动数查询）免费；注册即送 **10 免费点数**（可采 10 步）。
- 点数不足时提示用户充值；充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 交互协议（agent 必须严格遵守）

v2 是**人机分步交互**，不是一次性跑完。请按下面的流程驱动对话：

1. **建会话（免费）**：`node cli.js start --url "<笔记链接>"`。直链（带不带 xsec_token 均可）和 `xhslink.com` 短链都直接传，服务端自动转链补齐 token，无需调用其它转链 skill。
2. **报数确认（必须）**：把返回的 `metrics.comment_count`（评论总数）和 `estimated_pages`（预估页数，每页 10 条 = 1 点）**明确告知用户**，例如「这篇笔记共约 326 条评论，全采约需 33 页（33 点）。要开始采集吗？」。**未经用户确认不要执行任何 step。**
3. **按页采集**：用户确认后 `node cli.js step --session <id>` 采下一页主评论（默认即 --page）。把本页 10 条评论整理展示给用户。
4. **每页采完询问下一步**：
   - 若 `has_more_main=true`，问用户「是否继续采下一页（再扣 1 点）？」
   - 若返回的 `expandable` 非空（本页有主评论含可展开子评论），列出这些评论（`root_comment_id`、子评论总数、已采数），问用户「是否展开某条的子评论（每次展开约 5 条、扣 1 点）？」
5. **展开子评论**：用户指定后 `node cli.js step --session <id> --expand --root <root_comment_id>`。返回本次约 5 条子评论；若 `sub_has_more=true`，**先展示本次结果，再问用户是否继续展开该条**（继续再扣 1 点）。
6. **结束**：用户说够了 → `node cli.js finish --session <id>` 结束会话释放采集节点；需要文件 → `node cli.js export --session <id> --out 评论.csv`。
7. **20 分钟空闲租约**：每步采完后会话保持 20 分钟；超时无继续指令会话自动过期、节点释放。过期后（错误码 3006 / status=expired）如需继续，只能重新 `start` 建会话从头采（原会话已采数据仍可用 `comments`/`export` 读取）。

**no_more 免扣费**：`step` 返回 `no_more: true` 表示主评论已采完（或该主评论子评论已全部展开），**该次请求不扣费**，如实告知用户。

**中途失败自愈**：若采集节点的标签页意外被关，服务端会自动重试一次（重开页面并按进度快进恢复），只扣 1 次费用；重试仍失败则当步点数自动返还、会话 failed，如实告知用户。

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
- 交互提示（如「请把评论数报给用户确认」）一律走 **stderr**，不要解析，但其中给用户的引导话术应照做。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败（重新 login）；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。
- `step` 单次最长约 3 分钟（节点滚动/展开 + 回传），属正常现象，不要中途重试。

## 命令清单

### version — 查看版本与安装信息

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"xhs-comments","version":"2.0.1","capability":"xhs_comments"}}
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

### start — 建立采集会话（免费）

```bash
node cli.js start --url "https://www.xiaohongshu.com/explore/6ac86a34000000001801361e?xsec_token=..."
node cli.js start --url "https://xhslink.com/a/xxxx"     # 短链直接传, 服务端自动展开转链
```

- 服务端自动完成：链接解析 → 短链/缺 token 自动转链（免费）→ 互动数采集（免费）→ 建会话。
- 链接无效 / 笔记不可见 → 直接报错，**不建会话不扣费**。

输出示例：

```json
{"ok":true,"data":{"session_id":"9f1c...32位","note_id":"6ac86a34000000001801361e",
 "note_url":"https://www.xiaohongshu.com/explore/...?xsec_token=...","title":"示例笔记标题",
 "status":"active",
 "metrics":{"comment_count":"326","liked_count":"1.2万","collected_count":"890","share_count":"45"},
 "estimated_pages":33}}
```

**拿到结果后必须先把评论总数和预估页数报给用户确认，再开始 step（见「交互协议」）。**

### step — 步进采集（每步 1 点）

```bash
node cli.js step --session <id>                              # 采下一页主评论（默认 --page）
node cli.js step --session <id> --page                       # 同上, 显式写法
node cli.js step --session <id> --expand --root <主评论id>    # 对指定主评论展开一次子评论
```

采一页主评论的输出示例：

```json
{"ok":true,"data":{"session_id":"9f1c...","type":"page","page_no":1,
 "comments":[{"comment_id":"c1","root_comment_id":"","nickname":"小红薯","content":"太好看了！",
              "like_count":125,"ip_location":"浙江","sub_count":3}, ...],
 "has_more_main":true,
 "expandable":[{"root_comment_id":"c1","sub_comment_count":12,"subs_collected":2,"has_more":true}],
 "mains_collected":10,"subs_collected":5,"quota_balance":9}}
```

展开一次子评论的输出示例：

```json
{"ok":true,"data":{"session_id":"9f1c...","type":"expand","root_comment_id":"c1",
 "comments":[{"comment_id":"s1","root_comment_id":"c1","nickname":"路人甲","content":"求链接",
              "like_count":12,"ip_location":"上海","sub_count":0}, ...],
 "sub_has_more":true,"subs_collected_for_root":7,"quota_balance":8}}
```

- `expandable` 中 `has_more=true` 的条目表示子评论还没展开完，可继续 `--expand`。
- 已采完时返回 `{"no_more":true,...}`（不扣费）。

### status — 查询会话状态（免费）

```bash
node cli.js status --session <id>
```

返回会话状态（active/done/expired/failed）、累计采集量（pages/mains/subs）、已扣费步数、点数余额、互动数。

### comments — 拉取已累计的评论明细（免费）

```bash
node cli.js comments --session <id> --page 1 --page-size 100
```

分页读取本会话已落库的全部评论（含历史，不止增量），适合中途回顾。

### export — 导出累计结果 CSV（免费）

```bash
node cli.js export --session <id> --out 评论明细.csv
```

下载本会话已累计的全部评论 CSV（BOM 头，Excel 直开不乱码）：昵称/内容/点赞数/IP属地/子评论数。

### finish — 结束会话（免费）

```bash
node cli.js finish --session <id>
```

主动结束会话、释放采集节点（之后该节点可接其它任务）。不 finish 也会在空闲 20 分钟后自动过期。

### sessions — 列出自己的会话（免费）

```bash
node cli.js sessions
node cli.js sessions --status active --page 1
```

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

1. 拿到用户给的笔记链接后 `node cli.js quota` 确认有余额，然后 `node cli.js start --url "<链接>"`（短链/裸链直接传，自动转链）。
2. 把 `comment_count` 和 `estimated_pages` 报给用户，说明全采预估点数，**等用户确认**。
3. 循环：`step --session <id>` 采一页 → 展示本页 10 条 → 报告 `has_more_main` 与 `expandable` 列表 → 问用户「继续下一页？展开哪条的子评论？还是结束？」
4. 用户要子评论：`step --session <id> --expand --root <id>` → 展示本次约 5 条 → `sub_has_more` 为 true 时问是否继续展开。
5. 用户说结束：`finish --session <id>`；要文件：`export --session <id> --out 评论明细.csv`，把 CSV 路径交给用户。
6. 全程注意 20 分钟空闲上限，用户长时间未回复后先 `status` 确认会话是否还活着。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 链接无效 / 笔记不可见 | 检查链接有效性；笔记已删/私密则如实告知（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 未注册走 `register --link`（送 10 点数），已有账号走 `login --link`；完成后 `--check`（退出码 2） |
| LOGIN_PENDING / LOGIN_EXPIRED | 用户未完成 / 会话过期 | 提醒用户完成扫码后重试 `--check`，或重新 `--link`（退出码 2） |
| 2003 | 需要图形验证码 | 终端无法完成，统一走 `--link`；仍无法解决拨打客服电话 18722121663 |
| 3001 | 点数不足 | 提示用户拨打客服电话 18722121663 充值，不要重试（退出码 3） |
| 3006 | 会话不存在/已过期/已结束 | 20 分钟空闲会自动过期；已采数据可用 `comments`/`export` 读取，继续采集需重新 `start` |
| 5001 | 采集服务暂不可用（无在线节点/节点掉线） | 稍后重试；持续不可用时提示用户联系客服 18722121663 |
| 4290 | 触发限流 | 稍等后重试（Retry-After） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 `config show` 的 base_url（退出码 4） |

## 计费规则提示

- **免费**：start（含自动转链 + 互动数采集）、status / comments / sessions / finish / export / quota，以及返回 `no_more` 的 step。
- **每步 1 点**：一次 `step --page`（一页主评论）或一次 `step --expand`（一次子评论展开）。
- **自动返还**：服务侧故障（节点掉线且自愈重试也失败、风控拦截等）的当步点数自动返还；会话置 failed 时已采数据仍可读取。
- **不返还**：笔记中途被删/转私密等业务性失败已完成的部分正常计费。

## 红线

- 仅采集**公开**笔记数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出。
- 评论含用户公开昵称、IP 属地等个人信息：**仅用于用户已授权或公开可获取的舆情/反馈分析场景**，遵守平台与数据合规要求；不在未授权场景下转售、滥用或长期留存可识别个人信息；CSV 导出文件请告知用户自行妥善保管。
