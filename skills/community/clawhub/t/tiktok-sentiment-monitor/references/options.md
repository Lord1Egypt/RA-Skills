# TikTok定向舆情监测助手 技能 · 完整参数说明

> 所有命令必须在**技能根目录**执行。stdout 输出纯 JSON，日志走 stderr。
> 字段级结构以 `assets/*.schema.json`（JSON Schema draft-07）为准。

---

## 1. 🔎 关键词搜索 `search-cli.js`

```bash
node scripts/tiktok/search-cli.js --keyword <关键词> [--sort <排序>] [--time <时间>] [--limit <数量>]
```

| 参数        | 缩写 | 作用       | 可选值                                                                                      | 必填 | 默认 |
| ----------- | :--: | ---------- | ------------------------------------------------------------------------------------------- | :--: | :--: |
| `--keyword` | `-k` | 搜索关键词 | 2–100 字符；不可含 `< > " ' &`，不可含 http 链接                                            |  是  |  —   |
| `--sort`    | `-s` | 排序方式   | `0` 相关度 / `1` 最多点赞                                                                   |  否  | `0`  |
| `--time`    | `-t` | 发布时间   | `0` 全部 / `1` 最近一天 / `7` 最近一周 / `30` 最近一个月 / `90` 最近三个月 / `180` 最近半年 |  否  | `0`  |
| `--limit`   | `-l` | 获取数量   | 1–10000，建议 ≤ 1000                                                                         |  否  | `10` |

关键词也支持位置参数写法：`node scripts/tiktok/search-cli.js "AI model" --sort 1`

```bash
# 搜索 AI 相关内容
node scripts/tiktok/search-cli.js --keyword "AI"

# 找点赞最多的爆款
node scripts/tiktok/search-cli.js --keyword "AI" --sort 1 --limit 20

# 搜索近 7 天的 AI 内容
node scripts/tiktok/search-cli.js --keyword "AI" --time 7 --limit 20

# 搜索半年内 100 条 "AI Model"
node scripts/tiktok/search-cli.js --keyword "AI Model" --time 180 --limit 100
```

**主要返回字段**：`aweme_id`、`desc`、`create_time` / `create_time_str`、`author_uid`、`author_nickname`、`author_sec_uid`、`author_signature`、`author_url`、`digg_count`、`comment_count`、`share_count`、`collect_count`、`share_url`、`play_addr`、`video_cover`、`video_duration`、`music_title`、`music_author`、`tags`、`suggest_words`

---

## 2. 🦸 博主作品 `post-cli.js`

```bash
node scripts/tiktok/post-cli.js --url <主页URL或用户名> [--sort <排序>] [--limit <数量>]
```

| 参数      | 缩写 | 作用                  | 可选值              | 必填 | 默认 |
| --------- | :--: | --------------------- | ------------------- | :--: | :--: |
| `--url`   | `-u` | 博主主页 URL 或用户名 | 见下方说明          |  是  |  —   |
| `--sort`  | `-s` | 作品排序              | `0` 最新 / `1` 最热 |  否  | `0`  |
| `--limit` | `-l` | 获取作品数量          | 1–10000             |  否  | `10` |

> ⚠️ `--sort` 与搜索的 `--sort` 含义不同。

**`--url` 支持的形态**

- 主页：`https://www.tiktok.com/@username`
- 带参数：`https://www.tiktok.com/@username?lang=en`（query 会被自动剥离）
- 直接用户名：`username`
- 搜索结果中的 `author_sec_uid`

> ⚠️ 传视频链接（含 `/video/`）会被当作主页处理且结果不符预期。要评论请改用 `comment-cli.js`。

```bash
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --limit 30
node scripts/tiktok/post-cli.js -u "username" -s 1 -l 100
```

**主要返回字段**：`aweme_id`、`desc` / `caption`、`create_time`、`video_url`、`video_cover`、`video_duration`、`digg_count`、`comment_count`、`share_count`、`collect_count`、`music_title`、`music_author`、`tags`、`share_url`

---

## 3. 💬 视频评论 `comment-cli.js`

```bash
node scripts/tiktok/comment-cli.js --url <视频URL或作品ID> [--limit <数量>]
```

| 参数      | 缩写 | 作用               | 可选值              | 必填 | 默认 |
| --------- | :--: | ------------------ | ------------------- | :--: | :--: |
| `--url`   | `-u` | 视频 URL 或作品 ID | 见下方说明          |  是  |  —   |
| `--limit` | `-l` | 获取评论数量       | 1–10000，建议 ≤ 1000 |  否  | `10` |

**`--url` 支持的形态**

- 标准视频页：`https://www.tiktok.com/@username/video/1234567890123456789`
- 直接作品 ID：`1234567890123456789`

```bash
node scripts/tiktok/comment-cli.js --url "https://www.tiktok.com/@username/video/1234567890123456789" --limit 100
node scripts/tiktok/comment-cli.js -u "1234567890123456789" -l 50
```

**主要返回字段**：`cid`、`text`（评论正文）、`create_time`、`digg_count`、`user_uid`、`user_nickname`、`user_sec_uid`、`reply_comment_total`（回复数）

---

## 4. 统一输出信封

```json
{
  "status": "success | empty | error",
  "error_code": "OK | NO_MATCH | AUTH_REQUIRED | INVALID_KEYWORD | ...",
  "message": "人类可读说明",
  "timestamp": "2026-09-16 21:00:00",
  "request": {
    "command": "search",
    "keyword": "AI",
    "sort": 1,
    "time": 0,
    "limit": 20
  },
  "metadata": {
    "skill_version": "1.0.0",
    "skill_name": "tiktok-creator-videos",
    "execution_time": 8421
  },
  "results": [],
  "warnings": ["数量 99999 无效，已回退为 10"]
}
```

## 5. 退出码与错误码

| 退出码 | 含义                                          |
| ------ | --------------------------------------------- |
| `0`    | 成功（`success` 或 `empty`）                  |
| `1`    | 运行错误（网络 / 超时 / 参数非法 / 接口异常） |
| `3`    | `AUTH_REQUIRED`：Token 缺失或格式错误         |

| error_code        | 说明                                   |
| ----------------- | -------------------------------------- |
| `OK`              | 成功                                   |
| `NO_MATCH`        | 请求成功但无匹配数据（`status=empty`） |
| `AUTH_REQUIRED`   | Token 未配置或格式错误                 |
| `INVALID_KEYWORD` | 关键词不合法                           |
| `NETWORK_ERROR`   | 网络异常（已内置重试）                 |
| `TIMEOUT_ERROR`   | 请求超时（已内置重试）                 |

## 6. 重试与回退策略

- 创建任务：最多 3 次；查询任务：最多 20 次；退避间隔从 2 秒起指数增长，上限 30 秒。
- `AUTH_REQUIRED` 与服务端返回的明确业务错误码**不重试**，直接返回。
- 网络超时 / 连接重置会自动重试，无需手动干预。
- 参数非法时**不报错退出**，而是回退为默认值，并在 `warnings` 中说明。
