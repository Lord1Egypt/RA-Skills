# TikTok数据智能助手 完整选项参数说明

所有命令在技能根目录执行。stdout 是一份 JSON 信封，日志在 stderr。字段以 `assets/*.schema.json` 为准。

非法的 `--sort`、`--time`、`--limit` 会直接失败（退出码 2），不会改成默认值再请求。

**套餐双上限**：技能硬上限 10000（按量）。包月 Token 超限返回 `PLAN_LIMIT`（后端 errcode 14）：搜索/作品 ≤30，评论 ≤40。不要当网络错误同参重试。

## 1. 关键词搜索 `search-cli.js`

```bash
node scripts/tiktok/search-cli.js --keyword "AI model" --sort 1 --time 7 --limit 20
```

| 参数 | 缩写 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--keyword` | `-k` | 1–100 个字符；不能是链接；不含 `< > " '` | 必填 |
| `--sort` | `-s` | `0` 相关度 / `1` 最多点赞 | `0` |
| `--time` | `-t` | `0` 全部 / `1` 近 1 日 / `7` 近 7 日 / `30` 近 1 月 / `90` 近 3 月 / `180` 近 6 月 | `0` |
| `--limit` | `-l` | 整数 1–10000（**包月 Token 实际最多 30**） | `10` |

搜索没有「最新发布」排序。`--time 2` 会失败。

主要字段：`aweme_id`、`desc`、`create_time`、`author_id`（数字 uid，不要交给作品命令）、`author_uid`（@用户名）、`author_nickname`、`author_sec_uid`、`author_url`（技能补的主页）、`author_follower_count`、`digg_count`、`comment_count`、`play_count`、`share_count`、`collect_count`、`play_addr`、`dynamic_cover`、`duration`、`tags`、`suggest_words`。

`play_addr` 是一条字符串。`duration` 原样返回，一般为毫秒。数字 0 和空字符串可能不出现。

下一步：评论用 `aweme_id`；作品用 `author_sec_uid` 或 `author_url`。

## 2. 博主作品 `post-cli.js`

```bash
node scripts/tiktok/post-cli.js --url "https://www.tiktok.com/@username" --sort 0 --limit 30
node scripts/tiktok/post-cli.js --url "MS4wLjABAAAA..." --sort 1 --limit 20
```

| 参数 | 缩写 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` | `-u` | 主页、`@用户名` 或整段 `MS4w` 开头的 sec_uid | 必填 |
| `--sort` | `-s` | `0` 最新 / `1` 最热 | `0` |
| `--limit` | `-l` | 整数 1–10000（**包月最多 30**） | `10` |

`http` 会改成 `https`，`tiktok.com` 和 `m.tiktok.com` 会补成 `www.tiktok.com`，query 会去掉。视频链接、纯数字作品 id、`vm` / `vt` / `/t/` 短链会直接失败。

主要字段：`aweme_id`、`desc`、`create_time`、`video_url`（字符串数组）、`video_cover`、`video_duration`、`digg_count`、`play_count`、`comment_count`、`share_count`、`collect_count`、`music_title`、`music_author`、`music_duration`、`tags`、`share_url`、`suggest_words`。

`video_duration` 一般为毫秒，`music_duration` 一般为秒。结果里没有博主粉丝对象。查这个作者的下一条评论用 `aweme_id`。

## 3. 视频评论 `comment-cli.js`

```bash
node scripts/tiktok/comment-cli.js --url "https://www.tiktok.com/@username/video/1234567890123456789" --limit 40
node scripts/tiktok/comment-cli.js --url 1234567890123456789 --limit 40
```

| 参数 | 缩写 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` | `-u` | `/video/数字id` 或纯数字 `aweme_id` | 必填 |
| `--limit` | `-l` | 整数 1–10000（**包月最多 40**） | `10` |

主页、sec_uid、短链、`/photo/` 会直接失败。没有 IP 归属地字段。

主要字段：`cid`、`text`、`create_time`、`digg_count`、`reply_comment_total`、`user_id`（不要交给作品命令）、`user_uid`、`user_nickname`、`user_sec_uid`、`user_url`（技能补的主页）。

要看评论者发过什么，把 `user_sec_uid` 或 `user_url` 交给 `post-cli.js`。

## 4. 信封与退出码

```json
{
  "status": "success",
  "error_code": "OK",
  "message": "搜索任务完成",
  "timestamp": "2026/10/26 16:20:00",
  "request": { "command": "search", "keyword": "AI", "sort": 1, "time": 0, "limit": 20 },
  "metadata": { "skill_version": "1.1.1", "runtime_version": "22.22.2", "execution_time": 8421 },
  "results": []
}
```

| 退出码 | 含义 |
| --- | --- |
| `0` | 成功或空结果。`--help` 也是 0，但 stdout 为空 |
| `2` | 参数或关键词不合法 |
| `1` | 链接不合法、网络、超时、接口业务错误 |
| `3` | Token 缺失或无效 |

查询最多 20 次，间隔封顶 60 秒，只算等待大约 15 分钟。未完成时 `error_code` 是 `TIMEOUT`。搜索的 `TIMEOUT` 也可能表示没有可保存的结果，因为采集端不落空的搜索结果。

同一组参数再次执行时，搜索大约 9 分钟内、作品和评论大约 20 分钟内会复用已有任务。搜索等到 `TIMEOUT` 之后再立刻重跑，复用窗口通常已过。

成功结果默认不写文件。需要留底时设置 `TT_GUAIKEI_ENABLE_LOG=1`。
