# 📱 微博舆情VOC｜热搜榜 · 关键词搜索 · 微博评论

微博公开数据只读技能。热搜、关键词搜索、单条微博评论。零第三方依赖，Node.js >= 16.14。

Agent 入口是 [SKILL.md](SKILL.md)。本文件给直接跑命令的人。

## 🔑 环境

```bat
set GUAIKEI_API_TOKEN=你的TOKEN
```

TOKEN 为 16-256 位字母、数字、下划线或连字符。请求发往 `https://www.guaikei.com`，请求头 `TOKEN`。

## ⚡ 命令

| 脚本 | 作用 | 必填 |
| --- | --- | --- |
| `scripts/weibo/hot-cli.js` | 热搜榜 | 无，默认 `realtimehot` |
| `scripts/weibo/search-cli.js` | 关键词搜索 | `--keyword` |
| `scripts/weibo/comment-cli.js` | 一条微博的评论 | `--url` |

```bat
node scripts\weibo\hot-cli.js --category social
node scripts\weibo\search-cli.js --keyword "AI 教程" --search-type 1 --limit 10
node scripts\weibo\comment-cli.js --url "https://weibo.com/detail/123" --sort 0 --limit 20
```

也可 `npm run hot` / `npm run search` / `npm run comment`，参数接在 `--` 后面。

stdout 是 JSON 信封，日志在 stderr。加 `--save` 或 `GUAIKEI_ENABLE_LOG=1` 才把完整结果写到系统临时目录 `weibo-guaikei/logs/`。

## 📋 参数

热搜 `--category`：`realtimehot` 实时、`fun` 文娱、`social` 社会、`sportnav` 体育、`lifenav` 生活、`gamenav` ACG、`technologynav` 科技。

搜索 `--search-type`：`1` 综合、`2` 实时、`3` 用户、`4` 视频、`5` 热门、`6` 话题、`7` 超话。关键词 1-50 字，不能是链接。

评论 `--sort`：`0` 按热度、`1` 按时间。链接须含 `weibo.com/` 或 `weibo.cn/`。

`--limit` 默认 10，范围 1-10000。包月搜索最多 30、评论最多 50。非法枚举直接失败，不会改成默认值再请求。

创建任务后，查询只带返回的任务 id。命令对外不暴露这个 id；超时后用同一组参数再跑，服务端在窗口内续等。

## 💰 计费路径

热搜 `weibo/hot`（按次）。搜索 `weibo/search`（每 10 条一页）。评论 `weibo/comment`（每 20 条一页）。成功或空结果的信封里可能有 `cost`。
