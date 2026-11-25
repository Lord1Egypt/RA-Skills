---
name: wb-comments
slug: wb-pinglun
displayName: 微博评论采集（会话制）
version: 1.0.0
description: 微博评论采集工具（分步会话）。当用户需要采集某条微博下面的评论——发布者昵称、评论内容、时间、点赞数、回复@、二级回复，导出评论 CSV（Excel 直开），或提到"微博评论/评论采集/评论导出/评论分析/评论区舆情"时使用本 skill。支持 weibo.com/<用户ID>/<微博ID> 直链与 t.cn 短链（短链由节点自动还原）。分步会话制：start 建会话（免费探测）后按页采集主评论（每页固定 20 条）、按需展开某条主评论的回复，每一步实时返回增量结果，由 AI 询问用户是否继续（每步 1 点数，注册送 10 点）。适合评论舆情分析、用户口碑调研、评论区选题、活动效果评估等场景。
---

# 微博评论采集 Skill（wb-comments，会话制）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：**分步会话制**采集微博评论。先 `start`（免费探测微博正文与评论总数），再按页采主评论、按需展开某条主评论的二级回复 —— 每一步都返回增量结果，由 agent 决定是否继续。全部评论可导出 CSV（BOM 头，Excel 直开不乱码）。

- **能采什么**：主评论与二级回复的发布者昵称（`nickname`）、作者 ID、评论正文（`text`，表情会还原成 `[允悲]` 这类文案）、点赞数（`digg_count`）、发布时间（`create_time`）、二级回复的**回复对象昵称**（`reply_to_nickname`）、评论 ID（`cid`）与根评论 ID（`root_cid`）。
- **为什么是会话制**：评论量往往很大（几百到几千条），一次采完既贵又慢。会话制让你先看到评论总数、按页推进、只对"回复多"的主评论展开，把钱花在刀刃上。
- **计费**：`start` 建会话**免费**；之后**每步 1 点数**（采一页主评论 = 1 步，展开一次回复 = 1 步）；**某一步一条都没采到时不扣费**（已是最后一页/回复已展开完/本次无新增）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题，请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **每步 0.1 元**（每 1 点数抵扣一步；建会话免费，无新增的步骤不扣费）。
- 注册即送 **10 免费点数**；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 链接要求（重要，提交前必读）

**本 skill 只接受微博主帖链接**：

- `https://weibo.com/2153789604/RoCNr3H8I`（`<用户ID>/<微博ID>`，最常见）
- `https://weibo.com/detail/5358690090880816`（`/detail/<mid>`）
- `https://t.cn/<短码>`（短链直接提交，节点浏览器自动还原）

用户主页链接请用 `wb-profile`，单篇主帖数据（正文/转发·评论·点赞数）请用 `wb-collect`。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放。
- 首次使用需先 `register --link`（注册即送 10 点数）或 `login --link`（已有账号），成功后 token 自动保存。
- **配置文件（含 token）存放于用户级目录 `~/.xhs-platform/config.json`**（与小红书/抖音/快手/B站系列 skill 共用同一账号体系）。可用环境变量 `XHS_CONFIG_PATH` 覆盖。
- **安全策略：登录和注册（发短信）每次都强制图形验证码**，终端无法展示，一律走 `--link` 微信扫码/链接方式。
- 后端服务地址默认 `http://st.aidata366.com`，可用 `node cli.js config set base-url <url>` 修改，或单次加 `--base-url <url>` 覆盖。
- **⚠️ 安全提示**：默认服务地址是**明文 http**，token 会在公网明文传输；如环境允许建议切 https。
- `~/.xhs-platform/config.json` 含 token，**不要泄露、不要提交 git**。

## 输出规约（重要）

- **stdout 只输出 JSON**：成功 `{"ok":true,"data":{...}}`，失败 `{"ok":false,"code":<业务码>,"message":"..."}`。
- 交互提示、轮询进度一律走 **stderr**，不要解析。
- 退出码：`0` 成功；`1` 参数/用法错误；`2` 认证失败；`3` 点数不足；`4` 网络/服务不可达；`5` 其它业务错误。

## 命令清单

### version

```bash
node cli.js version
```

```json
{"ok":true,"data":{"name":"wb-comments","version":"1.0.0","capability":"wb_comments"}}
```

### register / login / quota / logout / config

与 `wb-collect` skill 完全一致（同一账号体系、同一配置文件）：

```bash
node cli.js register --link
node cli.js register --check --access-token "<串>"
node cli.js login --link
node cli.js login --check --access-token "<串>"
node cli.js quota
node cli.js logout
node cli.js config show
```

### start — 建立采集会话（免费）

```bash
node cli.js start --url "https://weibo.com/2153789604/RoCNr3H8I"
```

节点打开微博探测正文与评论总数，**不扣费**。stderr 会提示「请把评论数和预估页数告知用户，确认后再执行 step 开始计费」——**agent 必须先向用户报数并征得同意再 step**。

```json
{"ok":true,"data":{"session_id":"003e1a74c03b432e821325f8ca1921cb","post_id":"5355022847312021",
 "bid":"Rn5owuGbP","title":"驻足静赏，尽览风华...","author_nickname":"法拉利中国",
 "status":"active","metrics":{"comment_count":"720","liked_count":"4585","share_count":"668"},
 "estimated_pages":36,"has_more_main":true}}
```

> 注意：`comment_count` 是页面显示的评论总数，微博接口会过滤一部分，实际可采条数通常少于这个数，属正常。

### step — 采集一步（每步 1 点数）

```bash
node cli.js step --session <session_id>                       # 采下一页主评论（每页 20 条）
node cli.js step --session <session_id> --expand --root <cid>  # 展开某条主评论的下一页回复
```

- 采主评论：返回本页新增的主评论（含随页带回的少量二级回复）与本页「可展开回复」的主评论列表（`expandable`，带 `sub_count` 与已采数）。
- 展开回复：`--root` 取自上一步 `expandable` 里的 `root_cid`，返回该主评论下一页新增回复。
- `no_more=true` 表示已采到底，**本次不扣费**。

### status — 查看会话状态（免费）

```bash
node cli.js status --session <session_id>
```

### comments — 拉取会话已累计的全部评论（免费）

```bash
node cli.js comments --session <session_id> [--page 1] [--page-size 100]
```

断点续看/全量拉取用，不额外扣费。

### finish — 结束会话（释放节点）

```bash
node cli.js finish --session <session_id>
```

采完请务必执行，释放采集节点标签页（会话也会在长时间无操作后自动过期释放）。

### sessions — 列出自己的会话

```bash
node cli.js sessions [--page 1] [--status active]
```

### export — 导出评论 CSV

```bash
node cli.js export --session <session_id> --out 评论.csv
```

导出该会话累计的全部评论（含二级回复与回复对象），BOM 头，Excel 直开不乱码。

## 典型工作流（agent 照此执行）

1. `node cli.js start --url <微博链接>`（免费）。
2. **把评论总数与预估页数报给用户，问要不要继续、大约采多少**——这一步必须做，不能自作主张一路采到底。
3. 用户同意后：`node cli.js step --session <sid>` 采一页主评论（1 点）；把本页评论整理给用户看。
4. 若 `expandable` 里有用户感兴趣的主评论（回复数多的），**问用户**要不要展开；同意后 `node cli.js step --session <sid> --expand --root <cid>`（1 点）。
5. 重复 3/4 直到 `no_more` 或用户喊停。
6. `node cli.js export --session <sid> --out <文件名>.csv` 交付文件。
7. 收尾 `node cli.js finish --session <sid>`。

**每一步都要先问再做**：这是会话制的核心纪律，也是帮用户省点数的关键。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 链接校验未通过 / root 不在可展开列表 | 检查链接形态；`--root` 必须取自上一步 `expandable`（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 走 `register --link` 或 `login --link`（退出码 2） |
| 2003 | 需要图形验证码 | 统一走 `--link`；仍无法解决拨打 18722121663 |
| 3001 | 点数不足 | 提示充值，不要重试（退出码 3） |
| 3003 | 会话不存在或不属于当前账号 | 检查 session_id；会话可能已过期释放，重新 `start` |
| `no_more: true` | 主评论/回复已采到底 | 本次未扣费，不要再重复 step |
| 4290 | 触发限流 | 稍后重试 |
| NETWORK_ERROR | 网络/服务不可达 | 检查 base_url（退出码 4） |

## 计费规则提示

- `start` 建会话**免费**。
- 每个 `step` 1 点数；**本步一条都没采到（到底/无新增）不扣费**。
- 服务侧故障（无在线微博节点/超时/风控拦截）导致的步也会返还。
- `status` / `comments` / `sessions` / `export` / `finish` 均不扣费。

## 红线

- 仅采集**公开**评论数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出。
- **每一步扣费前必须先征得用户同意**，不要静默连续 step。
