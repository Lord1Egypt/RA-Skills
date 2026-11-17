---
name: tiktok-opportunity-research
description: "研究TikTok搜索结果、作品结构、达人数据和用户反馈，筛选值得继续验证的机会。当用户询问TikTok选题、TikTok增长、用户痛点、获取TikTok视频数据、获取博主作品、看TikTok评论、做市场调研分析、做竞品/对标账号监控或评论舆情分析使用。触发词：TikTok搜索、TikTok评论、TikTok作品、博主作品、市场调研、对标账号、TikTok竞品分析、TikTok数据分析、短视频运营、TikTok舆情监控、热点追踪、爆款挖掘、tiktok search、tiktok work、douyin comments。"
license: MIT
version: 1.1.1
metadata:
  openclaw:
    emoji: "🎵"
    primaryEnv: GUAIKEI_API_TOKEN
    requires:
      bins:
        - node
      env:
        - GUAIKEI_API_TOKEN
  enabled: true
  type: command
  runtime: "nodejs@16.14.0+"
  requires:
    bins: ["node"]
    env: ["GUAIKEI_API_TOKEN"]
  env_desc:
    GUAIKEI_API_TOKEN: "TikTok 数据 API 访问令牌。未配置时无法调用接口；可通过 https://www.guaikei.com 开通并获取支持。"
  keywords:
    - "TikTok"
    - "tiktok"
    - "抖音国际版"
    - "TikTok搜索"
    - "TikTok评论"
    - "TikTok博主"
    - "爆款选题"
    - "竞品分析"
    - "评论舆情"
  category:
    - "Integrations"
    - "Research"
    - "数据分析"
    - "内容创作"
    - "商业运营"
  tags:
    - "TikTok"
    - "抖音国际版"
    - "关键词搜索"
    - "视频评论"
    - "博主作品"
    - "竞品分析"
    - "选题调研"
    - "舆情分析"
    - "爆款挖掘"
    - "KOL筛选"
    - "海外短视频"
    - "TikTok数据"
    - "TikTok搜索"
    - "TikTok评论"
    - "TikTok作品"
    - "TikTok达人"
    - "TikTok达人数据"
    - "TikTok达人作品"
    - "TikTokKOL"
    - "TikTokKOL作品"
    - "TikTok博主"
    - "TikTok博主作品"
    - "TikTok网红"
    - "TikTok竞品分析"
    - "TikTok数据分析"
    - "TikTok选题"
    - "TikTok爆款"
    - "TikTok视频下载"
    - "TikTok运营工具"
    - "TikTok关键词挖掘"
    - "TikTok舆情"
    - "TikTok内容分析"
    - "评论区洞察"
    - "短视频运营"
    - "短视频数据"
    - "跨境营销"
    - "海外社媒"
    - "红人营销"
    - "网红筛选"
    - "营销分析"
    - "content-analysis"
    - "competitor-analysis"
    - "influencer-tracking"
    - "social-listening"
    - "social-media-analytics"
    - "short-video"
    - "short-video-marketing"
    - "content-discovery"
    - "video-search"
    - "viral-content"
    - "market-research"
    - "data-scraping"
    - "api-wrapper"
    - "tiktok"
  schemas:
    - name: "输出信封"
      file: "assets/output_envelope.schema.json"
    - name: "搜索入参"
      file: "assets/search_cli_req.schema.json"
    - name: "搜索出参"
      file: "assets/search_cli_resp.schema.json"
    - name: "作品入参"
      file: "assets/post_cli_req.schema.json"
    - name: "作品出参"
      file: "assets/post_cli_resp.schema.json"
    - name: "评论入参"
      file: "assets/comment_cli_req.schema.json"
    - name: "评论出参"
      file: "assets/comment_cli_resp.schema.json"
  examples:
    - "帮我搜 TikTok 上 AI 点赞最多的视频 → node scripts/tiktok/search-cli.js --keyword \"AI\" --sort 1 --limit 20"
    - "最近一周 TikTok 的 AI model，要 20 条 → node scripts/tiktok/search-cli.js --keyword \"AI model\" --time 7 --limit 20"
    - "这个 TikTok 博主最近 30 条作品 → node scripts/tiktok/post-cli.js --url \"https://www.tiktok.com/@username\" --sort 0 --limit 30"
    - "这个 TikTok 博主什么最火 → node scripts/tiktok/post-cli.js --url \"https://www.tiktok.com/@username\" --sort 1 --limit 30"
    - "这条 TikTok 视频评论区在说什么，帮我归纳舆情 → node scripts/tiktok/comment-cli.js --url \"https://www.tiktok.com/@username/video/1234567890123456789\" --limit 40"
    - "盯一下这个竞品账号最近发了什么 → node scripts/tiktok/post-cli.js --url \"https://www.tiktok.com/@competitor\" --limit 10"
---

# 🚀 GUAIKEI TikTok机会研究

研究TikTok搜索结果、作品结构、达人数据和用户反馈，筛选值得继续验证的机会。给一个关键词或一条链接，拿回 TikTok 公开视频和评论。不登录，不发布。结果是一份 JSON。

| 你要做的事 | 用哪个命令 | 你拿到什么 |
| --- | --- | --- |
| 找选题、看高赞 | `search-cli.js` | 视频数组。点赞、播放、评论是数字 |
| 看评论区 | `comment-cli.js` | 评论数组 |
| 看博主作品 | `post-cli.js` | 作品数组。没有单独的粉丝总数对象 |

三个命令成功时 `results` 都是数组。空字符串和数字 0 可能不返回，缺失不一定是没有这个字段。

本技能没有视频详情命令，也不下载视频。视频链接只能拉评论。播放地址可能过期。

## 0. 🧭 每次按这个顺序执行

1. 确认环境变量 `GUAIKEI_API_TOKEN` 已配置。没有配置时直接告诉用户去 [GUAIKEI TikTok机会研究官网](https://www.guaikei.com) 开通，不要先跑一遍试探。
2. 在本技能根目录执行 `node scripts/tiktok/<命令>.js`。
3. stderr 出现「处理中」表示任务还在跑。等进程自己退出，再读 stdout 的最后一份 JSON。不要把 stderr 或整份 JSON 念给用户。
4. 按「4. 📦 读结果」的退出码表决定：改参数再试、告诉用户，或停止。

查询最多 20 次。间隔从 2 秒起按 2、4、8、16、32 秒增加，之后每次 60 秒，只算等待大约 15 分钟。每次请求本身还有最多 20 秒超时。宿主如果更早结束进程，按超时处理，不要立刻用同一组参数连打。

同一组参数再次执行时，服务端会复用还没过期的任务：搜索大约 9 分钟内，作品和评论大约 20 分钟内，不会另开一条。搜索如果已经等到 `TIMEOUT`，9 分钟的复用窗口通常已经过去，立刻重跑可能新建一条任务。

- 没有关键词或链接就先问，不要编造
- 搜索不传 `--limit` 是 10 条。用户说「全部」再加大，不要自行抓 10000 条。**包月 Token** 搜索/作品勿超 30、评论勿超 40，否则 `PLAN_LIMIT`
- `status=empty` 且退出码 0 是「接口已经完成，没有结果」，不是命令失败
- 搜索若一直处理中直到 `TIMEOUT`，可能是没有可保存的结果。告诉用户换关键词或稍后再试，不要立刻连打

## 1. 🎯 什么时候调用

满足任一条件即调用：用户提到 TikTok、tiktok 或抖音国际版，并要求搜索、看评论、看博主作品或做选题、竞品、舆情。

不要调用：只让写文案；平台是抖音、小红书、快手、B 站、微博、公众号；要求登录、发布、点赞、下载文件或私密数据；没有关键词也没有可识别链接。

## 2. 🔀 路由

按这个顺序判断，命中即停：

1. 要评论、留言、舆情，且对象是一条视频 → `comment-cli.js`
2. 要作品、主页、账号、博主、达人 → `post-cli.js`
3. 有关键词，且没有上面两类信号 → `search-cli.js`
4. 以上都不明确 → 先追问

链接和 id：

- `tiktok.com/@用户名` 只能给 `post-cli.js`。`http`、缺 `www`、`m.tiktok.com` 会在本地改成 `https://www.tiktok.com/@用户名`
- 整段 `MS4w` 开头的 `sec_uid` 只能给 `post-cli.js`。搜索结果用 `author_sec_uid`，或 `author_url`
- `tiktok.com/@用户名/video/数字` 和纯数字 `aweme_id` 只能给 `comment-cli.js`。搜索或作品结果用 `aweme_id`
- `author_id`、`user_id` 是数字 uid，不要交给作品命令
- `vm.tiktok.com`、`vt.tiktok.com`、`tiktok.com/t/` 短链两个命令都不接受。请用户换成标准链接，不要两个命令都试
- `/photo/` 图文链接不支持
- 只拿到一串数字、又没说明是视频 id 还是别的，按评论用；若用户说的是主页，先问

| 用户说 | 应该传 |
| --- | --- |
| 最火、点赞最多、爆款 | `search-cli.js --sort 1` |
| 搜索相关度、默认搜索 | `search-cli.js --sort 0`。搜索没有「按最新发布」 |
| 近一天 | `--time 1` |
| 近一周、这周 | `--time 7` |
| 近一月 / 近三月 / 近半年 | `--time 30` / `90` / `180` |
| 博主最近发了什么 | `post-cli.js --sort 0 --limit N`。不传 sort 就是最新。没说条数用 10 |
| 这个博主什么最火 | `post-cli.js --sort 1` |
| 评论区 | `comment-cli.js`。没说条数用默认 10 |

搜索的 `--sort 1` 是最多点赞。作品的 `--sort 1` 是最热，`--sort 0` 才是最新。

`--time 2` 不是两天，也不是一周。非法值会直接失败。

## 3. 🎛️ 参数

枚举和数量不在允许范围内时，命令直接失败（退出码 2，`INVALID_ARGS`），不会改成默认值再请求。三个命令都支持 `--help` / `-h`：帮助打在 stderr，退出码 0，stdout 为空。短参数大小写都可以。含空格的关键词用双引号包成一个参数。关键词以 `-` 开头时写成 `--keyword=-AI`，或 `node scripts/tiktok/search-cli.js -- -AI`。完整字段见 `assets/*_cli_req.schema.json` 与 [references/options.md](references/options.md)。

**套餐双上限（重要）**：技能侧硬上限为 10000（按量 Token）。**包月 Token** 超限会返回 `PLAN_LIMIT`（后端 errcode 14），不要当网络错误重试：搜索/作品最多 **30**，评论最多 **40**。具体以官网与本次 `message` 为准。

### 3.1 🔍 关键词搜索

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--keyword` `-k` | 是 | 1–100 个字符，不能是链接，不含 `< > " '` | — |
| `--sort` `-s` | 否 | `0` 相关度 / `1` 最多点赞 | `0` |
| `--time` `-t` | 否 | `0` 全部 / `1` 近 1 日 / `7` 近 7 日 / `30` 近 1 月 / `90` 近 3 月 / `180` 近 6 月 | `0` |
| `--limit` `-l` | 否 | 整数 1–10000（**包月 Token 实际最多 30**） | `10` |

### 3.2 🦸 博主作品

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 主页链接、`@用户名` 或整段 `sec_uid`，最长 255 | — |
| `--sort` `-s` | 否 | `0` 最新 / `1` 最热 | `0` |
| `--limit` `-l` | 否 | 整数 1–10000（**包月最多 30**） | `10` |

### 3.3 💬 视频评论

| 参数 | 必填 | 取值 | 默认 |
| --- | --- | --- | --- |
| `--url` `-u` | 是 | 视频链接或纯数字 `aweme_id`，最长 255 | — |
| `--limit` `-l` | 否 | 整数 1–10000（**包月最多 40**） | `10` |

## 4. 📦 读结果

成功、空结果、失败都是同一份信封。只读 stdout 的最后一份 JSON。`--help` 时 stdout 为空，帮助在 stderr。字段以 `assets/output_envelope.schema.json` 和 `assets/*_cli_resp.schema.json` 为准。

```json
{
  "status": "success",
  "error_code": "OK",
  "message": "搜索任务完成",
  "timestamp": "2026/10/26 16:20:00",
  "request": { "command": "search", "keyword": "AI", "sort": 1, "time": 0, "limit": 20 },
  "metadata": { "skill_version": "1.1.1", "runtime_version": "22.22.2", "execution_time": 8421 },
  "results": [{ "aweme_id": "123", "desc": "...", "digg_count": 100 }]
}
```

空结果仍是退出码 0：`status` 为 `empty`，`error_code` 为 `NO_MATCH`，`results` 为 `null`。失败时 `status` 为 `error`，`results` 为 `null`，`message` 是给人读的原因。

- 搜索、作品、评论成功时 `results` 都是数组
- 搜索作者有三套标识：`aweme_id` 给评论，`author_sec_uid` 或 `author_url` 给作品，`author_id` 是数字 uid
- 评论者同样：`user_sec_uid` 或 `user_url` 给作品，`user_id` 不要交给作品命令
- 作品列表没有粉丝数字段。粉丝在搜索结果的 `author_follower_count`
- 搜索播放地址是字符串 `play_addr`。作品播放地址是字符串数组 `video_url`
- 视频时长用户文档没写单位，按采集端原样的 TikTok 字段理解：视频时长一般为毫秒，音乐时长一般为秒

| 退出码 | error_code | 怎么处理 |
| --- | --- | --- |
| 0 | `OK` / `NO_MATCH` | 没有结果就告诉用户没有匹配内容，不要当成失败重试 |
| 2 | `INVALID_ARGS` / `INVALID_KEYWORD` | 按上一节改参数后再试一次。关键词是链接时改走作品或评论 |
| 1 | `INVALID_URL` | 按路由换命令，或向用户要标准链接。短链不要改命令再试 |
| 3 | `AUTH_REQUIRED` / `AUTH_ERROR` | 停止重试，让用户配置 `GUAIKEI_API_TOKEN` |
| 1 | `TIMEOUT` | 任务仍在处理，搜索也可能是没有可保存的结果。不要立刻重跑。搜索的复用窗口大约只有 9 分钟，等满超时后再跑可能新建一条任务 |
| 1 | `NETWORK_ERROR` / `HTTP_5xx` / `HTTP_429` | 命令内部已经重试过。退出后再失败就告诉用户稍后再试 |
| 1 | `PLAN_LIMIT` | 套餐单次条数超限（常见于包月）。**禁止同参重试**。转述 `message`；可建议降 `--limit`（搜索/作品≤30，评论≤40）或到官网升级按量；**须用户同意后再跑** |
| 1 | `"16"`（搜索）或 `"15"`（作品、评论） | 余额不足。转告 `message`，不要改参数连打 |
| 1 | `"1"` 或 `"2"` | 提交过于密集。等一会儿再试，不要改成另一组参数立刻连打 |
| 1 | 其它十进制数字 | 把 `message` 原样转告 |
| 1 | `API_ERROR` / `UNKNOWN` | 转告 `message`，建议联系官网 |

`error_code` 是字符串。查询还在处理、次数用尽时是 `TIMEOUT`，不是空结果。

## 5. 🔒 合规

只处理 TikTok 公开数据。调用时会把关键词或链接发到 `www.guaikei.com`。不上传本地文件，不登录，不发布，不下载视频文件。

成功结果默认不写文件。需要留底时设置 `TT_GUAIKEI_ENABLE_LOG=1`，文件写到系统临时目录的 `tiktok-guaikei/logs/`。POSIX 上权限是仅当前用户可读写；Windows 不使用这组权限位，靠临时目录本身的用户隔离。

开通 token 或更多帮助：[GUAIKEI TikTok机会研究官网](https://www.guaikei.com)。
