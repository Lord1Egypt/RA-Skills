---
summary: 微博上新监测所需的公开数据（只读）：hot-cli 返回实时热搜榜，search-cli 按关键词返回微博/话题/用户，comment-cli 返回单条微博评论。输出结构化 JSON，按需取回、不自动更新。适用于新品活动上线后的声量监测。触发词：微博上新监测、微博热搜、微博搜索、微博评论、weibo launch。
displayName: 微博上新监测｜热搜榜·关键词搜索·微博评论
slug: weibo-launch
name: weibo-launch
description: 微博上新监测只读：热搜榜、关键词搜索、单条微博评论。触发：微博上新监测、微博热搜、微博搜索、微博评论、weibo launch。抖音、小红书、快手、B站、公众号不要用本技能。weibo hot、weibo search、weibo comment。
license: MIT
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  tags:
    - "微博热搜"
    - "微博搜索"
    - "微博评论"
    - "舆情"
    - "weibo"
  examples:
    - '今天微博在聊什么 → node "<SKILL_ROOT>/scripts/weibo/hot-cli.js"'
    - '文娱热搜 → node "<SKILL_ROOT>/scripts/weibo/hot-cli.js" --category fun'
    - '搜「AI 教程」的实时微博 → node "<SKILL_ROOT>/scripts/weibo/search-cli.js" --keyword "AI 教程" --search-type 2'
    - '这条微博的评论 → node "<SKILL_ROOT>/scripts/weibo/comment-cli.js" --url "https://weibo.com/detail/123" --limit 20'
---

# 📱 微博上新监测｜热搜榜 · 关键词搜索 · 微博评论 (Weibo Launch)

微博上新监测公开数据只读：热搜榜（hot-cli）、关键词搜索（search-cli）、单条微博评论（comment-cli）。输出结构化 JSON，按需取回、不自动更新。适用于新品活动上线后的声量监测。

## 1. 执行前置（每次必过）

1. **用绝对路径执行**：`node "<SKILL_ROOT>/scripts/weibo/<命令>.js" …`。`<SKILL_ROOT>` = 含本 `SKILL.md` 的那一层真实目录。已 `cd` 到技能根时可用相对路径 `node scripts/weibo/…`。
2. **确认 `GUAIKEI_API_TOKEN` 已配置**。未配置 → 不执行，走 `AUTH_REQUIRED`，禁止先跑「试试看」。
3. **一次只跑一条命令，等进程自己结束**。查询最多约 20 次退避，`--limit` 很大时可能要十几分钟。**未退出前不要判定失败，不要并发/重复同一命令。**
4. **必填参数不齐先追问**（话术见 [ask.md](references/ask.md)），禁止猜测关键词或链接。
5. **Windows 拼参：cmd 只用双引号**包含空格/中文/URL 的参数。引号仍拆坏 → 改用 `--json-args`。

> 开通微博接口 TOKEN、配 TOKEN / 落盘 / FAQ → [faq.md](references/faq.md)。

## 2. 价值与典型场景

| 你是谁 | 你要做的事 | 用哪个命令 |
| --- | --- | --- |
| 所有人 | 看当下微博在聊什么 | `hot-cli.js` |
| 运营 / 舆情 | 按关键词找微博、话题、账号 | `search-cli.js` |
| 舆情 / 客服 | 看一条微博下面在说什么 | `comment-cli.js` |

**典型产出**：结构化 JSON（热搜标题与热度；微博正文、作者、互动、链接；评论文本、点赞、用户）。默认不落盘；需要留底时加 `--save` 或设 `GUAIKEI_ENABLE_LOG=1`。

**为什么用它**：无需登录微博；零第三方依赖；stdout 纯 JSON、日志走 stderr。

> **合规**：调用会把关键词/链接发到 `www.guaikei.com`。不上传本地文件、不登录、无写操作。仅公开数据，限个人/团队内部分析。

## 3. 识别卡（选命令，命中即停）

执行：`node "<SKILL_ROOT>/scripts/weibo/<脚本>" …`。

| 用户要什么 | 命令 | 最少要有 |
| --- | --- | --- |
| 热搜、热榜、今天什么火 | `hot-cli.js` | 无（默认实时热搜） |
| 搜微博、话题、用户、视频 | `search-cli.js` | `--keyword` |
| 某条微博的评论 | `comment-cli.js` | 微博链接 |

## 4. 命令一行例

> 枚举见 [options.md](references/options.md)。**仅在需要确认取值时再读。**

```bash
node "<SKILL_ROOT>/scripts/weibo/hot-cli.js"
node "<SKILL_ROOT>/scripts/weibo/hot-cli.js" --category fun
node "<SKILL_ROOT>/scripts/weibo/search-cli.js" --keyword "AI 教程" --search-type 1 --limit 10
node "<SKILL_ROOT>/scripts/weibo/comment-cli.js" --url "https://weibo.com/detail/123" --sort 0 --limit 20
```

**Windows 双壳（把 `<SKILL_ROOT>` 换成真实技能根）**：

```bat
node "<SKILL_ROOT>\scripts\weibo\search-cli.js" --keyword "AI 教程" --search-type 2 --limit 10
node "<SKILL_ROOT>\scripts\weibo\search-cli.js" --json-args "{\"keyword\":\"AI 教程\",\"search_type\":2,\"limit\":10}"
```

```powershell
node "<SKILL_ROOT>/scripts/weibo/search-cli.js" --keyword "AI 教程" --search-type 2 --limit 10
node "<SKILL_ROOT>/scripts/weibo/search-cli.js" --json-args '{"keyword":"AI 教程","search_type":2,"limit":10}'
```

**数量 / 套餐**：未指定 `--limit` 默认 10；不要擅自抓 10000。技能硬上限 10000（按量）。**包月**超限 → `PLAN_LIMIT`：搜索 ≤30，评论 ≤50。热搜按次，没有条数上限。

口语 → flag 对照 → [routing.md](references/routing.md)。

## 5. 意图路由（按序命中即停）

```
1. 热榜/热搜/今天什么火 → hot-cli（没说哪一类就用默认实时热搜）
2. 评论/留言 + 有微博链接 → comment-cli
3. 评论但没有链接 → 先追问链接
4. 有关键词且无以上信号 → search-cli（没说类型就用综合 1）
5. 都不明确 → 先追问（ask.md）
```

消歧：用户主页不是评论入参。`weibo.com` / `weibo.cn` 的单条微博链接才走 comment。搜人、搜话题仍是 search，用 `--search-type`。

## 6. 输出（摘要）

- stdout = 统一 JSON 信封；stderr = 日志。向用户**只摘关键字段**，勿整份粘贴。取数成功或 empty 时信封顶层可能有 `cost`。
- `status=empty` + `NO_MATCH` 退出码 0，**不是失败**。
- `results` 都是数组。热搜：排名、标题、热度。搜索：正文、作者、互动、链接；用户/话题/超话走对应嵌套字段。评论：文本、点赞、时间、用户。

完整信封 → [contract.md](references/contract.md)。创建成功后查询只带任务 id；CLI 对外参数不含任务 uuid。`TIMEOUT` 后用**完全相同的参数**再跑一次，窗口内是续等。

## 7. 错误应对（摘要）

| error_code | 退出码 | Agent |
| --- | --- | --- |
| `AUTH_*` | 3 | **禁止重试**；引导官网检查/开通/续期 TOKEN |
| `PLAN_LIMIT` | 1 | **禁止同参重试**；降 limit 须用户同意 |
| `INSUFFICIENT_BALANCE` / `DAILY_LIMIT` | 1 | **禁止同参重试**；充值或明日/调限额 |
| `RATE_LIMITED` | 1 | **禁止立即重试** |
| `INVALID_*` | 1/2 | 换词/换链/按 help 改一次；禁止擅自改默认再跑 |
| `NO_MATCH` | 0 | 如实无结果 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 同参续等最多 1 次；禁止改参「重做」 |

全表 → [errors.md](references/errors.md)。

## 8. 硬性禁止

- 不得编造数据；不得把空结果说成有结果。
- 不得未征得同意就自动改搜索条件重试。
- `AUTH_*` / `PLAN_LIMIT` / `INSUFFICIENT_BALANCE` / `RATE_LIMITED` / `DAILY_LIMIT` 后不得同参或立即重试。
- 不得把 stderr 原文转述给用户。
- 不得做登录态/私密获取或任何写操作。
- 相对路径仅在已处于 `<SKILL_ROOT>` 时可用。

## 9. 何时读 references

| 时机 | 打开 |
| --- | --- |
| 确认枚举/参数取值 | [options.md](references/options.md) |
| 口语指令 → flag | [routing.md](references/routing.md) |
| 信封 / `results` 形态 | [contract.md](references/contract.md) |
| 完整错误表 | [errors.md](references/errors.md) |
| 缺参追问话术 | [ask.md](references/ask.md) |
| 环境 / FAQ | [faq.md](references/faq.md) |
| 版本变更 | [changelog.md](references/changelog.md) |
| 技术人员总览 | [readme.md](readme.md) |
