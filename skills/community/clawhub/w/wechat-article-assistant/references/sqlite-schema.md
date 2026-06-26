# SQLite Schema Notes

## login_session

- 仅保存 1 条记录
- 保存 token、cookie 列表、cookie header、昵称、头像、来源和校验时间
- 当前设计按“单公众号平台账号”工作

## login_qrcode_session

- 保存二维码登录的临时 cookie
- 用于 `login-start -> login-poll/login-wait`
- 过期后可以直接丢弃

## proxy_config

- 当前固定使用 `name = default`
- `apply_article_fetch = 1` 表示抓单篇文章详情时走代理
- `apply_sync = 1` 表示同步公众号文章列表和远端文章清单时走代理

## account

- 保存公众号基础信息与累计同步计数
- `enabled` 只是账号层级启用状态

## sync_config

- 保存外部定时任务读取的同步时间点
- 本 Skill 不自带常驻 scheduler
- 推荐由 OpenClaw 定时任务或系统计划任务周期调用 `sync-due`

## article

- 保存文章元数据
- 主键为 `fakeid:aid`
- `detail_fetched = 1` 表示至少成功抓取过一次正文

## article_detail

- 保存正文 Markdown / HTML / 文本缓存
- 同时记录 `article.json`、`article.md`、`article.html` 的落地路径

## sync_log

- 每次同步都会写入一条日志
- 包含状态、消息、新增文章数、开始结束时间
