---
name: wb-profile
slug: wb-user-profile
displayName: 微博用户主页采集
version: 1.0.0
description: 微博用户主页采集工具。当用户提供微博博主主页链接，需要采集该博主发布的微博列表——微博正文、转发数/评论数/点赞数、发布时间、微博链接（原创与转发都会采集并保留转发关系），导出结果 CSV（Excel 直开），或提到"微博主页/博主微博/达人微博列表/微博账号采集"时使用本 skill。适合达人筛选、博主内容盘点、竞品账号监测、KOL 背调等场景。支持 weibo.com/u/<用户ID>、/profile/<用户ID> 直链与 t.cn 短链。**一页（约 20 条）= 1 点数；预扣按页数、结算按实采量退差；零结果或失败全额返还（注册送 10 点）。**
---

# 微博用户主页采集 Skill（wb-profile）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交微博用户主页链接 + 页数 → 平台调度内网浏览器节点调用 `/ajax/statuses/mymblog`（按 `since_id` 游标翻页）→ 拿到该博主主页的微博列表。**原创与转发都会采集，并保留转发关系**（`is_repost` 及原微博 ID/作者/正文）。结果可直接导出 CSV（BOM 头，Excel 直开不乱码）。

- **能采什么**：微博正文、发布时间、转发数/评论数/点赞数、微博 ID（`post_id`）与 bid、原帖链接；转发微博额外带 `reposted_post_id` / `reposted_author_nickname` / `reposted_text`。
- **适用场景**：达人筛选、博主内容盘点、竞品账号监测、KOL 背调等。
- **省心机制**：预扣按页数、结算按实采量退差、零结果/失败全额返还、Agent 友好（stdout 纯 JSON + 统一退出码）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题，请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **一页（约 20 条）0.1 元**（每 1 点数抵扣一页；预扣按页数、结算按实采量退差）。
- 注册即送 **10 免费点数**；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## ⚠️ 链接要求（重要，提交前必读）

**本 skill 只接受微博用户主页链接**：

1. **支持的链接形态**：
   - `https://weibo.com/u/2062260913`（`/u/<用户ID>`，最常见）
   - `https://weibo.com/profile/2062260913`（`/profile/<用户ID>`）
   - `https://weibo.com/2062260913`（裸 `/<用户ID>`）
   - `https://t.cn/<短码>`（短链直接提交，节点浏览器自动还原）

2. **单条微博链接（`weibo.com/<用户ID>/<微博ID>`）不要提交本 skill**：单篇采集请用 `wb-collect`，评论请用 `wb-comments`。传了主帖链接会被识别并提示改用什么 skill，不会误扣费。

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
{"ok":true,"data":{"name":"wb-profile","version":"1.0.0","capability":"wb_profile"}}
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
node cli.js config set base-url http://127.0.0.1:8084
node cli.js config show
```

### collect — 提交主页采集任务

```bash
node cli.js collect --url "https://weibo.com/u/2062260913"
node cli.js collect --url "https://weibo.com/u/2062260913" --pages 3 --wait
node cli.js collect --url "https://weibo.com/u/2062260913" --force   # 跳过 24h 去重
```

- `--pages` 1~10（默认 1），每页约 20 条。
- 幂等键按参数派生；`--force` 混入时间戳生成新键。

输出示例（不带 `--wait`）：

```json
{"ok":true,"data":{"task_id":"t_20261029_ea3da09f","total":1,"valid_count":1,"invalid_count":0,
 "charged":5,"quota_balance":5,"status":"pending"}}
```

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id> [--wait] [--interval 秒] [--timeout 秒]
```

终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261029_ea3da09f","status":"done","success_count":1,"fail_count":0,
 "items":[{"id":1,"status":"success",
   "result":{"profile_url":"https://weibo.com/u/2062260913","profile_user_id":"2062260913",
             "blogger_nickname":"法拉利中国","requested_pages":1,"collected_count":20,
             "settle_charged":5,"refunded_diff":0,
             "videos":[{"post_id":"5355022847312021","bid":"Rn5owuGbP",
                        "title":"驻足静赏，尽览风华...","share_count":"668",
                        "comment_count":"720","like_count":"4585",
                        "is_repost":0,"create_time":"2026-10-21 10:00:00"}]}}]}}
```

**解读要点（agent 必读）**：
- `collected_count` 实采条数、`settle_charged` 实收点数 —— **按这两个字段如实汇报计费**。
- 三个计数是**字符串**；**空串 = 未采集到**，不是 0。
- `is_repost=1` 的行是转发微博，原微博信息在 `reposted_*` 字段。
- 归属校验：只保留该博主自己的微博，页面上混入的他人微博会被过滤。

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out 博主微博.csv
```

两段式 CSV（BOM 头）：任务汇总 + 微博明细（正文/转发·评论·点赞/时间/链接/转发关系）。

## 典型工作流（agent 照此执行）

1. 确认链接是主页形态（`/u/<用户ID>`、`/profile/<用户ID>`、裸 `/<用户ID>` 或 `t.cn` 短链）。
2. `node cli.js quota` — 确认点数够（一页 1 点）。
3. `node cli.js collect --url <主页链接> [--pages N] --wait`。
4. 解析 stdout JSON，把 `result.videos` 整理成表格；按 `collected_count` / `settle_charged` 如实汇报。
5. 用户要文件时 `node cli.js export <task_id> --wait --out <文件名>.csv`。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误 / 链接校验未通过（非主页链接、域名不对） | 消息里说明原因：单篇链接改用 `wb-collect`，评论改用 `wb-comments`（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 走 `register --link` 或 `login --link`（退出码 2） |
| 2003 | 需要图形验证码 | 统一走 `--link`；仍无法解决拨打 18722121663 |
| 3001 | 点数不足 | 提示充值，不要重试（退出码 3） |
| 3003 / 3004 | 任务或导出不存在 | 检查 task_id 是否属于当前账号 |
| `status=failed` + 零结果 | 用户无内容 / 主页不可见 / 页面异常 | 点数已全额返还 |
| 4290 | 触发限流 | 稍后重试 |
| TIMEOUT | 轮询超时 | 稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 base_url（退出码 4） |

## 计费规则提示

- 预扣 = 页数 × 1 点；结算按**实采页数**退差。
- **零结果或失败全额返还**（用户无内容、主页不可见、页面异常、无在线微博节点、超时、风控拦截）。
- 同一用户同一主页 + 页数 24h 内默认去重；`--force` 强制重提会正常扣费。

## 红线

- 仅采集**公开**微博数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出。
