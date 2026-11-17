---
name: wechat-sou
description: 微信搜一搜公开数据只读：按关键词搜微信文章、微信视频。触发：微信搜索、搜一搜、公众号文章、视频号、微信热门、微信最新、wechat search、wechat article、wechat video。抖音、小红书、快手、B站、微博不要用本技能。不支持图片搜索、正文抓取、账号登录。
license: MIT
version: 1.1.1
metadata:
  openclaw:
    emoji: "🔍"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  runtime: "nodejs@16.14.0+"
  env_desc:
    GUAIKEI_API_TOKEN: "微信搜一搜数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通并获取支持。"
  keywords:
    - "微信"
    - "微信搜索"
    - "搜一搜"
    - "公众号"
    - "视频号"
    - "微信文章"
    - "微信视频"
    - "wechat"
    - "wechat search"
    - "wechat article"
    - "wechat video"
  category:
    - "数据分析"
    - "内容创作"
    - "Data&APIs"
  tags:
    - "wechat"
    - "search"
    - "video"
    - "article"
    - "微信"
    - "微信搜索"
    - "数据挖掘"
    - "内容分析"
    - "竞品分析"
  schemas:
    - name: "输出信封"
      file: "assets/output_envelope.schema.json"
    - name: "文章搜索入参"
      file: "assets/article_cli_req.schema.json"
    - name: "文章搜索出参"
      file: "assets/article_cli_resp.schema.json"
    - name: "视频搜索入参"
      file: "assets/video_cli_req.schema.json"
    - name: "视频搜索出参"
      file: "assets/video_cli_resp.schema.json"
  examples:
    - name: 搜索"AI"的微信文章
      command: node scripts/wechat/article-cli.js --keyword AI
      description: 快速获取关键词相关文章数据
    - name: 搜索"AI"的热门微信文章
      command: node scripts/wechat/article-cli.js --keyword AI --sort 2
      description: 挖掘爆款文章特征
    - name: 搜索"AI"的最近1天发布的微信文章
      command: node scripts/wechat/article-cli.js --keyword AI --publishTime 1
      description: 获取最新关键词相关文章
    - name: 搜索"AI"的微信视频
      command: node scripts/wechat/video-cli.js --keyword AI
      description: 快速获取关键词相关视频数据
    - name: 搜索"AI"的最新微信视频
      command: node scripts/wechat/video-cli.js --keyword AI --sort 1
      description: 获取最新关键词相关视频
    - name: 搜索长度在5-20分钟的"AI"的微信视频
      command: node scripts/wechat/video-cli.js --keyword AI --sort 2 --duration 2
      description: 按时长筛选视频
---

# 微信搜一搜实时检索：实时获取微信生态最新内容（文章/视频/图片）

微信公开搜索数据只读获取。支持**按关键词搜文章**、**按关键词搜视频**，输出结构化 JSON。不支持图片搜索、文章正文抓取、账号登录或写操作。

## 1. ⚠️ 执行前置清单（每次执行前必须过一遍）

1. **先 `cd` 到本 SKILL.md 所在目录**，再执行下面的 `node scripts/wechat/*.js` 命令。
2. **确认环境变量 `GUAIKEI_API_TOKEN` 已配置且有效**。未配置 → 不执行命令，直接走 §7 的 `AUTH_REQUIRED` 话术，禁止先跑一遍"试试看"。**禁止把 TOKEN 写进命令行参数。**
3. **一次只跑一条命令，跑完等它自己结束**。查询最多 20 次，间隔从 2 秒起倍增，单次最长 60 秒；算上单次请求 20 秒超时，`--limit` 很大时可能较长。**进程未退出前不要判定失败，不要并发或重复发起同一条命令。**
4. **必填参数不齐就先追问**，禁止猜测关键词。

## 2. 🎯 识别卡（选命令，命中即停）

| 用户要什么                         | 命令                                      | 最少要有    |
| ---------------------------------- | ----------------------------------------- | ----------- |
| 搜微信文章、公众号文章、搜一搜文章 | `node scripts/wechat/article-cli.js`      | `--keyword` |
| 搜微信视频、视频号相关内容         | `node scripts/wechat/video-cli.js`        | `--keyword` |

**不要用本技能**：抖音 / 小红书 / 快手 / B站 / 微博；图片搜索；要文章全文正文；要登录微信账号。

## 3. 🛠️ 命令与参数

> 完整取值见 `references/options.md`（**仅在需要确认枚举含义时才读**）。

### 3.1 文章搜索 `article-cli.js`

| 参数            | 缩写 | 必填 | 取值                                           | 默认 |
| --------------- | ---- | ---- | ---------------------------------------------- | ---- |
| `--keyword`     | `-k` | ✅   | 2–50 个字符，不能是链接，不含 `< > " ' &`      | —    |
| `--sort`        | `-s` |      | 0 综合 / 1 最新 / 2 最热                       | 0    |
| `--publishTime` | `-t` |      | 0 不限 / 1 最近1天 / 2 最近7天 / 3 最近半年    | 0    |
| `--limit`       | `-l` |      | 1–10000（**包月 Token 实际最多 20**）          | 10   |

### 3.2 视频搜索 `video-cli.js`

| 参数         | 缩写 | 必填 | 取值                                                 | 默认 |
| ------------ | ---- | ---- | ---------------------------------------------------- | ---- |
| `--keyword`  | `-k` | ✅   | 2–50 个字符，不能是链接，不含 `< > " ' &`            | —    |
| `--sort`     | `-s` |      | 0 综合 / 1 最新 / 2 最热                             | 0    |
| `--duration` | `-d` |      | 0 不限 / 1 5分钟以下 / 2 5-20分钟 / 3 20分钟以上     | 0    |
| `--limit`    | `-l` |      | 1–10000（**包月 Token 实际最多 20**）                | 10   |

**数量约定**：未指定 `--limit` 时只返回 10 条。用户未要求更多时不要加大。包月超限返回 `PLAN_LIMIT`，**禁止当网络错误重试**。

**任务窗口**：创建后约 9 分钟内同参可复用任务；结果约 15 分钟内可查询。`TIMEOUT` 后必须**同参再调并等待**，不要改参数。

## 4. 🧾 输出契约

- **stdout**：仅一块合法 JSON 信封（见 `assets/output_envelope.schema.json`）
- **stderr**：人类可读日志（Banner / INFO），不要转述给用户
- 成功时 `results` 为数组；`empty` / `error` 时 `results` 为 `null`

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | INVALID_KEYWORD | INVALID_ARGS | AUTH_REQUIRED | AUTH_ERROR | PLAN_LIMIT | TIMEOUT | ...",
  "message": "人类可读说明",
  "timestamp": "2026/11/7 17:00:00",
  "request": { "command": "article", "keyword": "AI", "sort": 0, "limit": 10 },
  "metadata": { "skill_version": "1.1.1", "runtime_version": "22.x", "execution_time": 1234, "total": 10 },
  "results": []
}
```

**向用户汇报时只摘关键字段**（文章：标题/作者/时间/`url`；视频：标题/作者/时长/点赞/时间）。不要把整份 JSON 原样粘贴。视频结果当前通常**没有可打开 url**，有 `docid`/`exportid` 时如实说明。

结果自动落盘到技能目录 `logs/`，便于复盘。

## 5. 🚨 退出码与错误码 → Agent 应对

| error_code | 退出码 | Agent 必须做什么 |
| ---------- | ------ | ---------------- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3 | **禁止重试**。引导到 https://www.guaikei.com 开通并配置 `GUAIKEI_API_TOKEN` |
| `PLAN_LIMIT` | 1 | **禁止同参重试**。建议降低 `--limit`（包月 ≤20）或升级按量；**须用户同意后再跑** |
| `INSUFFICIENT_BALANCE` | 1 | 余额不足（后端 15）。**禁止同参重试**。引导官网充值 |
| `RATE_LIMITED` | 1 | 短时间提交过多（后端 2）。**禁止立即重试** |
| `DAILY_LIMIT` | 1 | 今日消费已达每日上限（后端 `CheckDayMoney` **18**）。**禁止同参重试**。明日再试或到官网调整限额 |
| `INVALID_KEYWORD` | 1 | 请用户换词；**禁止自动改词重试** |
| `INVALID_ARGS` | 2 | 按 `--help` 修正后重试**一次**；**禁止改成默认值后自动再跑** |
| `NO_MATCH`（status=empty） | 0 | 如实告知无结果；可建议放宽条件，**经用户同意后**再试 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 可同参再调**最多 1 次**并等待；约 9 分钟内服务端仍复用同任务。禁止改参「重做」 |
| `HTTP_5xx` / 其他 | 1 | 如实报告 `message`，不编造原因，不反复重试 |

## 6. 🛑 硬性禁止条款

- 不得编造数据；不得把空结果说成有结果。
- 不得在未征得用户同意时自动修改搜索条件重试。
- `AUTH_*` / `PLAN_LIMIT` / 余额与频控类错误后不得同参瞎重试。
- 不得把 TOKEN 写进 argv；不得把 stderr 日志原文转述给用户。
- 不得用本技能做登录态、私密数据或任何写操作。
- 不得在未 cd 到技能目录的情况下执行命令。

## 7. 🧠 追问模板

- 缺关键词：「你想搜微信里的什么内容？给我一个关键词，例如"AI 教程"。」
- 文章还是视频不明：「你是要搜微信文章，还是微信视频？」
- 数量不明：「默认返回 10 条，需要更多的话告诉我具体条数（包月最多 20）。」

## 8. 🔧 环境与合规

- 环境：Node.js 16.14.0+；必需环境变量 `GUAIKEI_API_TOKEN`（16–256 位字母、数字、下划线或连字符）。
- 配置：Windows cmd `set GUAIKEI_API_TOKEN=你的TOKEN`；PowerShell `$env:GUAIKEI_API_TOKEN="你的TOKEN"`；Linux/macOS `export GUAIKEI_API_TOKEN=你的TOKEN`。
- 可选：`GUAIKEI_API_HOST` 覆盖 API 域名（默认 `www.guaikei.com`）。
- 合规：仅处理微信公开搜索数据；调用会把关键词发送至第三方 API（www.guaikei.com）；数据仅限个人/团队内部分析，禁止违规分发。
- 支持：https://www.guaikei.com
