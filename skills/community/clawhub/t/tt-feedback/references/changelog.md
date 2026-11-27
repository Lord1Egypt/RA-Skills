# TikTok用户反馈洞察 更新日志

## 1.1.3

- 新增 `references/faq.md`；SKILL 写入 Windows cmd/PowerShell 双壳例与「cmd 只用双引号」。
- CLI 支持 `--json-args`（与传统 flag 互斥；键名用 `keyword`/`url`/`sort` 等）；`parseCliArgs` 统一入口；SKILL/faq 补例。
- 落盘开关统一为 `GUAIKEI_ENABLE_LOG=1` 或 CLI `--save`；废弃 `TT_GUAIKEI_ENABLE_LOG`。
- `backendCodes`：在余额判断之后将裸 `errcode === 14` 稳定映射为 `PLAN_LIMIT`；搜索余额官方码 `16` 稳定映射为 `INSUFFICIENT_BALANCE`。
- 按 path 区分接口：搜索侧裸 `errcode === 15` 不再标为余额不足（现行后端搜索余额为 16；查价失败为 1）；修正 `request.js` 过时注释。
- 搜索侧裸 `errcode === 2`（插入失败）不再映射为 `RATE_LIMITED`；统一创建重试口径（注释 / readme：频控等稳定业务码不重试）。
- stdout 信封顶层可选 `cost`（透传取数接口花费估算；错误省略）。

## 1.1.2

- 链接 tidy 首尾 scrub 补齐中文引号/书名号等，避免 `「」` 粘在 `@user/video/id` 后误判。
- `finishSuccess` 先落盘再 drain stdout，再 stderr 提示后 `exit(0)`。
- 错误码改为 errmsg 优先：`INSUFFICIENT_BALANCE`（搜索 16 / 作品评论 15）、`RATE_LIMITED`（含搜索频控 errcode 1）、`DAILY_LIMIT`（18）。
- SKILL 不再要求 Agent 记裸数字 `"15"`/`"16"`。

## 1.1.1

- 明确套餐双上限：技能硬上限仍为 10000（按量）；包月 Token 搜索/作品最多 30、评论最多 40。
- 后端 errcode `14` 映射为稳定 `PLAN_LIMIT`；Agent 禁止同参重试，可建议降 `--limit` 或升级套餐（须用户同意）。
- 文档与示例同步：评论示例改为包月安全的 40，避免按「100 条」直接踩坑。

## 1.1.0

- 写明查询最长大约等 15 分钟，以及搜索 9 分钟、作品和评论 20 分钟的任务复用窗口。
- 创建阶段最后一次失败不再打成「还要重试」。stderr 时间与信封一样用北京时间。
- 支持 `--` 结束选项。以 `-` 开头的关键词用 `--keyword=-AI` 或 `node scripts/tiktok/search-cli.js -- -AI`。
- 日志文件名加上进程号。POSIX 上日志仅当前用户可读写；Windows 靠临时目录隔离。超长文件名仍保留 `.json`。
- stdout 统一为同一份 JSON 信封；非法参数直接失败，不再改成默认值后继续请求。
- 空结果退出码为 0。查询在任务处理中继续等待；未完成不再当成空结果，次数用尽返回 `TIMEOUT`。
- 增加搜索、作品、评论的入参、出参和输出信封 schema，字段与用户文档、采集结果对齐。
- 作品只接受主页、`@用户名` 或整段 `MS4w` sec_uid；评论只接受 `/video/数字id` 或纯数字 `aweme_id`。
- 链接会补 `www`、把 `http` 改成 `https`，并去掉 query。短链和 `/photo/` 直接失败。短参数大小写都可以。
- 搜索结果用 `author_uid`（用户名）补 `author_url`；评论结果用 `user_uid` 补 `user_url`。数字 uid 不交给作品命令。
- HTTP 429 和 5xx 会重试。查询时业务错误立即失败，只有 `errcode 1` 继续等待。
- 关键词不合法退出码为 2。Token 缺失也输出 `AUTH_REQUIRED` JSON。
- 成功结果默认不写文件。需要留底时设置 `TT_GUAIKEI_ENABLE_LOG=1`。

## 1.0.0

- tiktok-skill 技能首次发布。
- 提供 TikTok 通用搜索功能，支持通过关键词搜索视频数据。
- 提供 TikTok 作品获取功能，支持获取 KOL 的最新/最热作品数据。
- 提供 TikTok 评论抓取功能，支持获取指定视频的评论数据。
