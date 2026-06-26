# WeChat Article Assistant 接口文档

## 目录

- [1. 文档范围](#1-文档范围)
- [2. 调用约定](#2-调用约定)
- [3. 全局参数](#3-全局参数)
- [4. 环境变量](#4-环境变量)
- [5. 返回格式](#5-返回格式)
- [6. 命令分组总览](#6-命令分组总览)
- [7. 登录与会话接口](#7-登录与会话接口)
- [8. 代理与诊断接口](#8-代理与诊断接口)
- [9. 公众号管理接口](#9-公众号管理接口)
- [10. 同步接口](#10-同步接口)
- [11. 文章接口](#11-文章接口)
- [12. 调试与测试接口](#12-调试与测试接口)
- [13. Inbound Context 约定](#13-inbound-context-约定)
- [14. 错误与退出码约定](#14-错误与退出码约定)

## 1. 文档范围

本文档描述当前 Skill 的本地 CLI 接口，供以下场景使用：

- OpenClaw/Trae 通过本地命令调用 Skill
- 开发者手动执行命令进行联调
- 后续为 Skill 包装更高层调用器时作为接口基线

本文档以当前实现为准，不描述已经废弃的旧 Web API。

## 2. 调用约定

主入口：

```bash
python scripts/wechat_article_assistant.py <command> [options]
```

建议在自动化中统一带 `--json`：

```bash
python scripts/wechat_article_assistant.py <command> ... --json
```

说明：

- 带 `--json` 时返回 JSON 包装结果。
- 不带 `--json` 时返回 `formatted_text` 或简化文本。
- 命令成功退出码为 `0`。
- 命令失败退出码为 `1`。

## 3. 全局参数

所有命令都支持以下全局参数：

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--debug` | flag | `false` | 开启调试日志，同时输出到控制台和日志文件 |
| `--log-level` | string | 空 | 指定日志级别，如 `DEBUG` / `INFO` / `WARNING` |
| `--log-console` | bool | `null` | 是否输出控制台日志 |
| `--log-file` | bool | `null` | 是否写入日志文件 |

说明：

- `--debug` 的优先级高于 `--log-level`。
- 当未显式指定日志参数时，默认保持安静，不输出详细日志。

## 4. 环境变量

### 4.1 数据目录

| 变量名 | 说明 |
| --- | --- |
| `WECHAT_ARTICLE_ASSISTANT_HOME` | Skill 数据根目录，优先级更高 |
| `WECHAT_ARTICLE_OPENCLAW_HOME` | 兼容旧命名的数据根目录 |

说明：

- 当前实现同时兼容上述两套变量名。
- 若两者同时存在，优先使用 `WECHAT_ARTICLE_ASSISTANT_HOME`。
- 若两者都未设置，则默认使用 `~/.openclaw/media/wechat-article-assistant/`。

默认目录（未显式设置环境变量时）：

```text
~/.openclaw/media/wechat-article-assistant/
```

### 4.2 日志

| 变量名 | 说明 |
| --- | --- |
| `WECHAT_ARTICLE_ASSISTANT_LOG_LEVEL` | 日志级别，优先级更高 |
| `WECHAT_ARTICLE_ASSISTANT_LOG_CONSOLE` | 是否输出控制台日志，优先级更高 |
| `WECHAT_ARTICLE_ASSISTANT_LOG_TO_FILE` | 是否写入日志文件，优先级更高 |
| `WECHAT_ARTICLE_OPENCLAW_LOG_LEVEL` | 兼容旧命名的日志级别 |
| `WECHAT_ARTICLE_OPENCLAW_LOG_CONSOLE` | 兼容旧命名的控制台日志开关 |
| `WECHAT_ARTICLE_OPENCLAW_LOG_TO_FILE` | 兼容旧命名的文件日志开关 |

### 4.3 目录约定

在根目录下默认创建：

- `app.db`
- `downloads/articles/`
- `downloads/images/`
- `qrcodes/`
- `logs/wechat_article_assistant.log`

## 5. 返回格式

### 5.1 成功返回

```json
{
  "success": true,
  "data": {},
  "formatted_text": "..."
}
```

### 5.2 失败返回

```json
{
  "success": false,
  "error": "...",
  "formatted_text": "..."
}
```

### 5.3 通用约定

- `success`
  表示命令执行是否成功。
- `data`
  成功时的结构化返回数据。
- `error`
  失败时的错误信息。
- `formatted_text`
  面向文本场景的简化输出。

## 6. 命令分组总览

### 6.1 登录与会话

- `login-start`
- `login-poll`
- `login-wait`
- `login-import`
- `login-info`
- `login-clear`

### 6.2 代理与诊断

- `proxy-set`
- `proxy-show`
- `doctor`

### 6.3 公众号管理

- `search-account`
- `resolve-account-url`
- `add-account`
- `add-account-by-keyword`
- `add-account-by-url`
- `list-accounts`
- `delete-account`
- `list-sync-targets`
- `set-sync-target`

### 6.4 同步

- `sync`
- `sync-all`
- `sync-due`
- `sync-logs`

### 6.5 文章

- `list-account-articles`
- `recent-articles`
- `article-detail`

## 7. 登录与会话接口

### 7.1 `login-start`

用途：

- 生成微信公众号平台登录二维码。
- 可选通过 OpenClaw 发送二维码图片。

示例：

```bash
python scripts/wechat_article_assistant.py login-start --channel telegram --target telegram:5747692163 --account 8606699467 --json
python scripts/wechat_article_assistant.py login-start --channel telegram --target telegram:5747692163 --account 8606699467 --inbound-meta-file meta.json --json
python scripts/wechat_article_assistant.py login-start --channel telegram --target telegram:5747692163 --account 8606699467 --wait true --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--sid` | 否 | 自定义会话 ID |
| `--wait` | 否 | 生成二维码后是否直接等待登录完成 |
| `--timeout` | 否 | 配合 `--wait` 使用的最长等待秒数 |
| `--interval` | 否 | 配合 `--wait` 使用的轮询间隔秒数 |
| `--notify` | 否 | 是否发送二维码和登录结果通知 |
| `--channel` | 否 | 消息渠道。需要脚本主动调用 OpenClaw 发二维码时建议显式传入 |
| `--target` | 否 | 消息目标。需要脚本主动调用 OpenClaw 发二维码时建议显式传入 |
| `--account` | 否 | 消息账号。需要脚本主动调用 OpenClaw 发二维码时建议显式传入 |
| `--inbound-meta-json` | 否 | Inbound Context JSON |
| `--inbound-meta-file` | 否 | Inbound Context 文件 |
| `--json` | 否 | 输出 JSON |

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `sid` | 登录会话 ID |
| `qr_path` | 本地二维码图片路径 |
| `expires_at` | 过期时间戳 |
| `notify` | 若启用消息发送，表示二维码发送结果 |
| `auto_wait` | 是否启用了自动等待模式 |
| `wait_result` | 启用 `--wait true` 时，包含最终登录结果摘要 |
| `message_target` | 脚本实际使用的消息目标参数，包含 `channel`、`target`、`account` |

副作用：

- 写入 `login_qrcode_session`
- 保存二维码图片到 `qrcodes/`
- 当启用 `--wait true` 时，会继续轮询登录状态并在成功后自动发送通知，无需用户额外回报“已登录”

### 7.2 `login-poll`

用途：

- 轮询指定二维码会话的扫码状态。

示例：

```bash
python scripts/wechat_article_assistant.py login-poll --sid skill_xxx --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--sid` | 是 | 登录会话 ID |
| `--notify` | 否 | 状态变化时是否发送通知 |
| 消息相关参数 | 否 | 与 `login-start` 相同 |

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `sid` | 会话 ID |
| `status` | 微信原始状态码 |
| `status_text` | 状态文字 |
| `logged_in` | 是否已经完成登录 |
| `need_refresh` | 二维码是否需要刷新 |
| `nickname` | 登录成功后返回 |
| `token` | 登录成功后返回 |

### 7.3 `login-wait`

用途：

- 在超时时间内重复轮询，直到登录完成或需要刷新二维码。

示例：

```bash
python scripts/wechat_article_assistant.py login-wait --sid skill_xxx --timeout 300 --interval 3 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--sid` | 是 | 登录会话 ID |
| `--timeout` | 否 | 最大等待秒数 |
| `--interval` | 否 | 轮询间隔秒数 |
| `--notify` | 否 | 是否发送通知 |

### 7.4 `login-import`

用途：

- 导入旧系统 cookie/token 文件。

示例：

```bash
python scripts/wechat_article_assistant.py login-import --file path/to/cookie.json --validate true --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--file` | 是 | 登录文件路径 |
| `--validate` | 否 | 导入后是否立即校验 |

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `logged_in` | 是否校验成功 |
| `nickname` | 当前登录账号昵称 |
| `head_img` | 头像 |
| `token` | 登录 token |
| `source` | 登录来源 |
| `expires_at` | 过期时间戳 |
| `last_validated_at` | 最近校验时间戳 |

### 7.5 `login-info`

用途：

- 查看当前登录会话。

示例：

```bash
python scripts/wechat_article_assistant.py login-info --validate true --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--validate` | 否 | 是否主动校验 |

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `logged_in` | 当前登录态是否有效 |
| `nickname` | 账号昵称 |
| `head_img` | 头像 |
| `token` | token |
| `source` | 来源 |
| `expires_at` | cookie 最早过期时间 |
| `last_validated_at` | 最近校验时间 |

### 7.6 `login-clear`

用途：

- 清除当前登录会话和二维码会话。

示例：

```bash
python scripts/wechat_article_assistant.py login-clear --json
```

## 8. 代理与诊断接口

### 8.1 `proxy-set`

用途：

- 设置代理配置。

示例：

```bash
python scripts/wechat_article_assistant.py proxy-set \
  --url http://127.0.0.1:7890 \
  --enabled true \
  --apply-article-fetch true \
  --apply-sync true \
  --json
```

代理类型说明：

1. **标准 HTTP/HTTPS 代理**
   - 形如 `http://host:port`
   - 主要适合后台接口同步、列表拉取等场景

2. **文章抓取网关代理（旧项目兼容）**
   - 形如 `https://proxy.example.com`
   - 实际调用时，Skill 会在 `article-detail` 中自动拼成：
     `proxy_url?url=<文章短链接>`
   - 若最简模式失败，再回退尝试：
     `proxy_url?url=<文章短链接>&headers=<json>`

**统一测试方式：**

当用户提供的是文章抓取网关代理时，优先按下面方式测试，而不是先用标准 CONNECT 隧道代理测试：

```text
代理地址/?url=https://www.baidu.com/
```

示例：

```text
https://wechat.zzgzai.online/?url=https://www.baidu.com/
```

如果该 URL 能正常打开，说明这更像“URL 转发网关”而不是标准隧道代理。

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--url` | 否 | 代理地址 |
| `--enabled` | 否 | 是否启用代理 |
| `--apply-article-fetch` | 否 | 文章详情抓取是否走代理 |
| `--apply-sync` | 否 | 同步与远端列表是否走代理 |

成功返回字段：

- 直接返回 `proxy_config` 当前记录。

### 8.2 `proxy-show`

用途：

- 查看当前代理配置。

示例：

```bash
python scripts/wechat_article_assistant.py proxy-show --json
```

### 8.3 `doctor`

用途：

- 汇总诊断登录态与代理状态。

示例：

```bash
python scripts/wechat_article_assistant.py doctor --json
```

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `logged_in` | 登录校验是否通过 |
| `login_session` | 脱敏后的登录会话摘要 |
| `login_health` | 登录健康检查结果 |
| `proxy_config` | 当前代理配置 |
| `proxy_health.sync` | 同步场景下的代理健康 |
| `proxy_health.article` | 文章抓取场景下的代理健康 |

说明：

- `doctor` 不回显完整 cookie。
- 若代理不可用，会返回可读错误信息。

## 9. 公众号管理接口

### 9.1 `search-account`

用途：

- 根据关键字搜索公众号。

示例：

```bash
python scripts/wechat_article_assistant.py search-account "四川省图书馆" --limit 10 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `keyword` | 是 | 搜索关键字 |
| `--limit` | 否 | 候选数量 |

返回主要字段：

- `keyword`
- `total`
- `accounts[]`

### 9.2 `resolve-account-url`

用途：

- 根据公众号文章链接反查公众号。

示例：

```bash
python scripts/wechat_article_assistant.py resolve-account-url --url "https://mp.weixin.qq.com/s/example" --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--url` | 是 | 公众号文章链接 |
| `--limit` | 否 | 搜索候选数量 |

返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `url` | 归一化后的文章链接 |
| `resolved_name` | 从文章页解析出的公众号名称 |
| `total` | 候选数量 |
| `accounts` | 匹配候选 |

注意：

- 若文章页面被微信拦截为“环境异常”，该命令也会失败。

### 9.3 `add-account`

用途：

- 手动添加公众号。

示例：

```bash
python scripts/wechat_article_assistant.py add-account \
  --fakeid "MzkzODk1MzA5NA==" \
  --nickname "水e交费" \
  --initial-sync false \
  --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--fakeid` | 是 | 公众号 fakeid |
| `--nickname` | 是 | 昵称 |
| `--alias` | 否 | 别名 |
| `--avatar` | 否 | 头像 URL |
| `--service-type` | 否 | 服务类型 |
| `--signature` | 否 | 公众号简介 |
| `--enable-sync` | 否 | 是否启用同步 |
| `--sync-hour` | 否 | 同步小时 |
| `--sync-minute` | 否 | 同步分钟 |
| `--initial-sync` | 否 | 添加后是否立即同步 |

### 9.4 `add-account-by-keyword`

用途：

- 根据关键字自动添加唯一匹配公众号。

示例：

```bash
python scripts/wechat_article_assistant.py add-account-by-keyword "水e交费" --initial-sync false --json
```

行为说明：

- 若存在多个候选，会返回失败并带候选列表。

### 9.5 `add-account-by-url`

用途：

- 根据文章链接自动识别公众号并添加。

示例：

```bash
python scripts/wechat_article_assistant.py add-account-by-url \
  --url "https://mp.weixin.qq.com/s/example" \
  --initial-sync false \
  --json
```

依赖：

- 文章链接必须可解析公众号名称。

### 9.6 `list-accounts`

用途：

- 列出本地已维护公众号。

示例：

```bash
python scripts/wechat_article_assistant.py list-accounts --json
```

返回字段包括：

- `fakeid`
- `nickname`
- `alias`
- `avatar`
- `service_type`
- `signature`
- `enabled`
- `total_count`
- `articles_synced`
- `last_sync_at`
- `sync_hour`
- `sync_minute`
- `last_sync_status`
- `last_sync_message`

### 9.7 `delete-account`

用途：

- 删除公众号及其本地文章、文章详情与同步配置。

示例：

```bash
python scripts/wechat_article_assistant.py delete-account --fakeid "MzkzODk1MzA5NA==" --json
python scripts/wechat_article_assistant.py delete-account --nickname "水e交费" --json
```

### 9.8 `list-sync-targets`

用途：

- 查看同步目标配置。

示例：

```bash
python scripts/wechat_article_assistant.py list-sync-targets --json
```

### 9.9 `set-sync-target`

用途：

- 设置某个公众号的同步启用状态与时间。

示例：

```bash
python scripts/wechat_article_assistant.py set-sync-target \
  --fakeid "MzkzODk1MzA5NA==" \
  --enabled true \
  --sync-hour 8 \
  --sync-minute 0 \
  --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--fakeid` / `--nickname` | 二选一 | 目标公众号 |
| `--enabled` | 否 | 是否启用 |
| `--sync-hour` | 否 | 小时 |
| `--sync-minute` | 否 | 分钟 |

## 10. 同步接口

### 10.0 固定脚本入口

用于 OpenClaw cron / 外部调度器稳定调用：

```bash
bash ${HOME}/.openclaw/workspace/skills/wechat-article-assistant/scripts/run_sync_all.sh
```

用途：

- 封装“同步全部已启用公众号”的固定入口
- 适合 OpenClaw cron 任务长期调用
- 后续如需补登录校验、日志、失败告警，优先扩展该脚本

推荐的 OpenClaw cron 设计：

- 使用 `openclaw cron add`
- `--session isolated`
- `--announce`
- `--tz "Asia/Shanghai"`
- 如需整点精确执行，加 `--exact`
- 让 cron job 调用该固定脚本入口，而不是依赖 agent 每次临时拼接底层 Python 命令

### 10.1 `sync`

用途：

- 手动同步单个公众号。

示例：

```bash
python scripts/wechat_article_assistant.py sync --fakeid "MzkzODk1MzA5NA==" --json
```

返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `fakeid` | 公众号 fakeid |
| `articles_synced` | 本次新增文章数 |
| `total_count` | 微信接口报告的总消息数 |
| `pages_fetched` | 本次实际抓取页数 |
| `existing_hit_page` | 首次遇到本地已存在文章的页号；未命中则为 `null` |
| `extra_pages_after_existing` | 命中已存在文章后额外继续抓取的页数 |
| `message` | 文本说明 |

说明：

- 当前同步策略在首次遇到“本地已存在文章”后，不会立即停止，而是默认再多抓 `1` 页做冗余，降低因置顶/重发/列表波动导致的漏抓风险。

### 10.2 `sync-all`

用途：

- 同步所有启用的公众号。

示例：

```bash
python scripts/wechat_article_assistant.py sync-all --json
python scripts/wechat_article_assistant.py sync-all --interval-seconds 180 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--interval-seconds` | 否 | 不同公众号之间的同步间隔秒数，用于降低频控风险 |

返回主要字段：

- `total`
- `success`
- `failed`
- `interval_seconds`
- `results`

### 10.3 `sync-due`

用途：

- 供外部定时任务调用，同步当前时间点以及最近若干分钟内应执行但尚未执行的公众号。

示例：

```bash
python scripts/wechat_article_assistant.py sync-due --json
python scripts/wechat_article_assistant.py sync-due --grace-minutes 5 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--grace-minutes` | 否 | 允许补跑的分钟窗口，默认 `3` |

返回主要字段：

- `checked`
- `due`
- `grace_minutes`
- `results`

### 10.4 `sync-logs`

用途：

- 查询同步日志。

示例：

```bash
python scripts/wechat_article_assistant.py sync-logs --limit 20 --json
python scripts/wechat_article_assistant.py sync-logs --fakeid "MzkzODk1MzA5NA==" --limit 20 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--fakeid` | 否 | 按公众号过滤 |
| `--limit` | 否 | 返回条数 |

返回字段包括：

- `id`
- `fakeid`
- `nickname`
- `status`
- `message`
- `articles_synced`
- `started_at`
- `finished_at`
- `created_at`

## 11. 文章接口

### 11.1 `list-account-articles`

用途：

- 查询公众号文章清单。

示例：

```bash
python scripts/wechat_article_assistant.py list-account-articles \
  --fakeid "MzkzODk1MzA5NA==" \
  --remote true \
  --count 10 \
  --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--fakeid` / `--nickname` | 二选一 | 目标公众号 |
| `--begin` | 否 | 起始偏移 |
| `--count` | 否 | 返回条数 |
| `--keyword` | 否 | 关键字过滤 |
| `--remote` | 否 | 是否查远端 |
| `--save` | 否 | 远端结果是否写入本地 |

远端模式返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `fakeid` | 公众号 fakeid |
| `nickname` | 公众号昵称 |
| `remote` | 固定为 `true` |
| `total_count` | 微信接口返回总消息数 |
| `fetched_count` | 当前这一次远端请求实际展开出的文章数 |
| `returned_count` | 本次实际返回给调用方的文章数 |
| `articles` | 文章数组 |

说明：

- `--count` 目前同时影响远端请求页大小和最终返回切片大小。
- 由于微信返回的是 publish 列表，展开后实际文章数可能大于 `count`。
- 当前实现会先抓取并展开，再按 `count` 截断返回结果。

本地模式返回主要字段：

- `fakeid`
- `nickname`
- `remote = false`
- `articles`
- `total`

### 11.2 `recent-articles`

用途：

- 查询最近 N 小时本地文章。

示例：

```bash
python scripts/wechat_article_assistant.py recent-articles --hours 24 --limit 50 --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--hours` | 否 | 最近多少小时 |
| `--limit` | 否 | 最大返回数量 |

### 11.3 `article-detail`

用途：

- 获取单篇文章详情并可落地导出。

示例：

```bash
python scripts/wechat_article_assistant.py article-detail \
  --aid "2247484786_8" \
  --download-images true \
  --include-html false \
  --save true \
  --json
```

```bash
python scripts/wechat_article_assistant.py article-detail \
  --link "https://mp.weixin.qq.com/s/example" \
  --download-images true \
  --include-html false \
  --force-refresh false \
  --save true \
  --json
```

参数：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--aid` / `--link` | 二选一 | 文章标识 |
| `--download-images` | 否 | 是否下载图片 |
| `--include-html` | 否 | 是否返回并保存 HTML |
| `--force-refresh` | 否 | 是否跳过缓存重新抓取 |
| `--save` | 否 | 是否保存 `article.json` / `article.md` |

成功返回主要字段：

| 字段 | 说明 |
| --- | --- |
| `article_id` | 文章唯一标识，格式 `fakeid:aid` |
| `fakeid` | 公众号 fakeid |
| `aid` | 文章 aid |
| `title` | 标题；命中缓存时也会返回同样字段 |
| `author_name` | 作者；命中缓存时也会返回同样字段 |
| `account_name` | 公众号名称 |
| `digest` | 摘要；命中缓存时也会返回同样字段 |
| `link` | 文章链接 |
| `create_time` | 发布时间戳 |
| `create_time_formatted` | 格式化时间 |
| `markdown_content` | Markdown 正文 |
| `html_content` | HTML 正文，需 `include_html=true` |
| `text_content` | 纯文本正文 |
| `images` | 图片处理结果数组 |
| `saved_json_path` | JSON 落地路径 |
| `saved_md_path` | Markdown 落地路径 |
| `saved_html_path` | HTML 落地路径 |
| `cached` | 是否命中缓存 |

缓存说明：

- 默认优先返回本地 `article_detail` 缓存。
- 如需重新抓取远端正文，请显式传 `--force-refresh true`。
- 缓存命中与首次抓取时，返回字段结构保持一致。

代理说明：

- 当 `apply_article_fetch=true` 且配置的是“文章抓取网关代理”时，`article-detail` 会优先把原始文章链接归一化为**短链接**（`https://mp.weixin.qq.com/s/...`）后再请求代理。
- 当前代理顺序为：
  1. `proxy_url?url=<文章短链接>`
  2. 若失败，再尝试 `proxy_url?url=<文章短链接>&headers=<json>`
- 不要默认把这类代理当成标准 `requests proxies` 的 HTTP 隧道代理。

常见错误：

- `未找到文章链接，请提供 link 或确保 aid 已在本地数据库中存在`
- `微信返回环境异常校验页，请配置代理后重试文章详情抓取`
- `未能抓取到有效文章正文`

## 12. 调试与测试接口

### 12.1 `scripts/dev/smoke_test.py`

用途：

- 以步骤化方式调用 Skill CLI，用于开发与联调。

示例：

```bash
python scripts/dev/smoke_test.py \
  --cookie-file "E:\01-AICode\10-docker\wechat-article-exporter\data\kv\cookie\e803819fd88945db923afe63aecc0c54" \
  --steps doctor,login-import,search,add,remote-list
```

常用参数：

| 参数 | 说明 |
| --- | --- |
| `--home` | 测试数据目录 |
| `--cookie-file` | 登录文件 |
| `--keyword` | 测试公众号关键字 |
| `--fakeid` | 手工指定 fakeid |
| `--article-aid` | 手工指定文章 aid |
| `--article-link` | 手工指定文章链接 |
| `--proxy-url` | 测试代理地址 |
| `--steps` | 要执行的步骤列表 |
| `--continue-on-error` | 出错后继续 |
| `--debug` | 为子命令开启 debug |

输出特征：

- 每一步打印命令结果。
- 会打印 stdout/stderr。
- 最后输出测试状态摘要。

## 13. Inbound Context 约定

当需要自动发送二维码或通知时，CLI 支持读取 Inbound Context。

输入格式：

```json
{
  "schema": "openclaw.inbound_meta.v1",
  "chat_id": "telegram:5747692163",
  "account_id": "8606699467",
  "channel": "telegram"
}
```

字段映射：

| 输入字段 | 内部用途 |
| --- | --- |
| `channel` | 消息渠道 |
| `chat_id` | `target` |
| `account_id` | `account` |

支持两种传入方式：

- `--inbound-meta-json`
- `--inbound-meta-file`

## 14. 错误与退出码约定

### 14.1 退出码

| 退出码 | 含义 |
| --- | --- |
| `0` | 命令执行成功 |
| `1` | 命令执行失败 |

### 14.2 常见错误分类

#### 输入参数错误

- 缺少必填参数
- 布尔值解析失败
- 指定的公众号或文章不存在

#### 登录错误

- 未找到登录会话
- 登录态过期
- 导入文件缺少 token 或 cookies

#### 代理错误

- 代理已启用但 URL 缺失
- 代理连接失败
- 代理连通性检查失败

#### 微信抓取错误

- 微信接口返回非 0 状态码
- 微信文章页返回环境异常
- 微信文章正文解析失败

### 14.3 自动化调用建议

- 永远带 `--json`
- 基于 `success` 判断业务结果
- 同时检查进程退出码
- 对“环境异常”与“代理连接失败”做专门分支处理
