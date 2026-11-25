---
name: wb-search
slug: wb-keyword-search
displayName: 微博关键词搜索采集
version: 1.0.0
description: 微博关键词搜索采集工具。当用户需要按关键词搜索微博并采集结果列表——微博正文、转发数/评论数/点赞数、作者昵称、发布时间、微博链接，并按微博类型（全部/原创/关注人/认证用户/媒体/观点/网友讨论）、排序（综合/热门/实时）、起止日期筛选，导出搜索结果 CSV（Excel 直开），或提到"微博搜索/搜微博/关键词采集/搜索结果导出/选题/竞品微博列表"时使用本 skill。适合内容选题调研、竞品监测、达人初筛、品类微博盘点等场景。**一页（20 条）= 1 点数；预扣按请求量、结算按实采量退差；零结果或失败全额返还（注册送 10 点）。**
---

# 微博关键词搜索采集 Skill（wb-search）

封装「小红书能力平台」（FastAPI，`/api/v1`）的 CLI，供 AI agent 调用：提交关键词 + 采集条数（可选类型/排序/起止日期）→ 平台调度内网浏览器节点打开 `s.weibo.com` 搜索页逐页解析 SSR 卡片 → 拿到微博列表（正文、作者、发布时间、转发/评论/点赞三项计数、微博链接）。结果可直接导出 CSV（BOM 头，Excel 直开不乱码）。

- **能采什么**：微博正文（`title`/`text`）、作者昵称与 ID、发布时间（`create_time`）、**转发数（`share_count`）、评论数（`comment_count`）、点赞数（`like_count`）**（三项都由搜索页直出，无需逐条补采）、微博 ID（`post_id`）与 bid、原帖链接。
- **筛选维度**：关键词（`--keyword`）、采集条数（`--count`，1~500）、微博类型（`--type`）、排序（`--sort`）、起止日期（`--start-date` / `--end-date`）。
- **省心机制**：预扣按请求量、结算按实采量自动退差、零结果/失败全额返还、Agent 友好（stdout 纯 JSON + 统一退出码）。
- 客户端是零依赖 CLI（Node ≥ 18，无需 `npm install`），全部采集逻辑在后端完成。

## 客服支持

注册或使用过程中遇到任何问题，请引导用户联系客服：

- **客服微信**（扫码添加）：http://st.aidata366.com/assets/concat.png
- **客服电话**：**18722121663**

## 收费价格

- **点数换算：0.1 元 = 1 点数。**
- **一页（20 条）0.1 元**（每 1 点数抵扣一页；预扣按请求量、结算按实采量退差）。
- 注册即送 **10 免费点数**；点数不足时提示用户充值。
- 充值或大量购买可享优惠，请联系客服 **18722121663** 洽谈。

## 筛选参数（提交前必读）

| 参数 | 取值 | 默认 |
|---|---|---|
| `--keyword` | 搜索关键词（≤64 字符；**不是链接**，传链接会被拒） | 必填 |
| `--count` | 1~500，想采集的条数 | 50 |
| `--type` | `typeall`=全部 / `ori`=原创 / `atten`=关注人 / `vip`=认证用户 / `category_4`=媒体 / `viewpoint`=观点 / `discuss`=网友讨论 | `typeall` |
| `--sort` | `default`=综合 / `hot`=热门 / `realtime`=实时 | `default` |
| `--start-date` / `--end-date` | `YYYY-MM-DD`，起止日期（含当天） | 不限 |

- 类型/排序传了白名单外的值**不会报错，会回落到默认值**（与服务端一致），所以提交前请确认取值拼写。
- 日期必须是 `YYYY-MM-DD` 且为合法日期；开始日期不能晚于结束日期，否则直接拒绝（不扣费）。

## 前置条件

- **Node.js ≥ 18**（使用内置 fetch，零 npm 依赖）。
- **不注册不登录没有任何点数**：所有接口都需要 token，10 免费点数在注册成功后发放到账号。
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
{"ok":true,"data":{"name":"wb-search","version":"1.0.0","capability":"wb_search"}}
```

### register / login / quota / logout / config

与 `wb-collect` skill 完全一致（同一账号体系、同一配置文件），此处不再赘述：

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

`register --link` 的 stderr 会给出可直接复制给用户的注册引导话术，**agent 必须原样发给用户**。

### submit — 提交搜索采集任务

```bash
node cli.js submit --keyword "法拉利"
node cli.js submit --keyword "法拉利" --count 100 --wait
node cli.js submit --keyword "法拉利" --type ori --sort hot --wait
node cli.js submit --keyword "法拉利" --start-date 2026-10-01 --end-date 2026-10-29 --wait
node cli.js submit --keyword "法拉利" --force      # 跳过 24h 内容去重强制重提
```

- 每任务 1 个关键词。
- 幂等键按参数派生，同参数重试不重复扣费；`--force` 混入时间戳生成新键（服务端同时跳过 24h 去重）。
- 提交前会读一次价格并在 stderr 透出预估点数。

输出示例（不带 `--wait`）：

```json
{"ok":true,"data":{"task_id":"t_20261029_67c73013","total":1,"valid_count":1,"invalid_count":0,
 "charged":5,"quota_balance":5,"status":"pending","estimated_points":5,"price_per_unit":5}}
```

带 `--wait` 时最终输出同 `query` 的完整结果（默认超时 600s，节点翻页约 3-5 分钟）。

### query — 查询任务 / 拉取结果

```bash
node cli.js query <task_id> [--wait] [--interval 秒] [--timeout 秒]
```

终态输出示例：

```json
{"ok":true,"data":{"task_id":"t_20261029_67c73013","status":"done","success_count":1,"fail_count":0,
 "items":[{"id":1,"status":"success",
   "result":{"keyword":"法拉利","requested_count":20,"collected_count":20,
             "settle_charged":5,"refunded_diff":0,
             "videos":[{"post_id":"5359194924384651","bid":"RoPVGioEb",
                        "title":"法拉利官方墨西哥海报这张好啊...",
                        "share_count":"10","comment_count":"15","like_count":"169",
                        "author_nickname":"Leliana19","create_time":"2026-10-28 16:51:00",
                        "url":"https://weibo.com/1189295834/RoLP34nLp"}]}}]}}
```

**解读要点（agent 必读）**：
- `collected_count` 是实采条数，`settle_charged` 是实收点数，`refunded_diff` 是退差点数 —— **按这三个字段如实向用户汇报**，不要按提交时的预扣数说。
- 三个计数是**字符串**；**空串 = 未采集到**，不是 0。
- 微博搜索页显示的评论总数与实际可采评论条数常有差异（接口会过滤），属正常。

### export — 导出 CSV

```bash
node cli.js export <task_id> --wait --out 微博搜索.csv
```

两段式 CSV（BOM 头）：任务汇总 + 微博明细（正文/转发·评论·点赞/作者/时间/链接）。

## 典型工作流（agent 照此执行）

1. 与用户确认关键词；如用户还要筛选，确认类型/排序/起止日期。
2. `node cli.js quota` — 确认点数够（一页 1 点，先估 `ceil(条数/20)`）。
3. `node cli.js submit --keyword "<关键词>" [--count N] [--type T] [--sort S] [--start-date D] [--end-date D] --wait`。
4. 解析 stdout JSON，把 `result.videos` 整理成表格返回；**按 `collected_count` / `settle_charged` 如实汇报计费**。
5. 用户要文件时 `node cli.js export <task_id> --wait --out <文件名>.csv`。

## 错误处理指引

| code | 含义 | agent 下一步 |
|---|---|---|
| 1001 | 参数错误（关键词为空/超长、日期格式错、关键词里混了链接） | 修正参数后重提（退出码 1） |
| 1002 / 1003 | 未登录 / token 失效 | 走 `register --link` 或 `login --link`（退出码 2） |
| 2003 | 需要图形验证码 | 统一走 `--link`；仍无法解决拨打 18722121663 |
| 3001 | 点数不足 | 提示充值，不要重试（退出码 3） |
| 3003 / 3004 | 任务或导出不存在 | 检查 task_id 是否属于当前账号 |
| `status=failed` + 零结果 | 关键词无结果或页面异常 | 点数已全额返还，换个关键词重试 |
| 4290 | 触发限流 | 稍后重试 |
| TIMEOUT | 轮询超时 | 稍后 `query <task_id>` 再查（退出码 5） |
| NETWORK_ERROR | 网络/服务不可达 | 检查 base_url（退出码 4） |

## 计费规则提示

- 预扣 = `ceil(请求条数 / 20)` 点；结算按**实采量**退差（零头按一页计）。
- **零结果或失败全额返还**（关键词无结果、页面异常、无在线微博节点、超时、风控拦截）。
- 同一用户同一关键词 + 参数 24h 内默认去重；`--force` 强制重提会正常扣费。

## 红线

- 仅采集**公开**微博数据；不用于任何违法违规用途。
- 不要向用户承诺 100% 成功；风控导致的失败如实透出。
