# 退出码与错误码

| error_code | 退出码 | 含义 | Agent 必须做什么 |
| --- | --- | --- | --- |
| `AUTH_REQUIRED` / `AUTH_ERROR` | 3 | TOKEN 未配置、无效、停用、未开通该接口或已过期 | **禁止重试**。引导到 https://www.guaikei.com 检查、开通或续期。不要把停用说成接口下线 |
| `PLAN_LIMIT` | 1 | 包月单次条数超限。搜索最多 30，评论最多 50 | **禁止同参重试**。转述 `message`；降 `--limit` 须用户同意 |
| `INSUFFICIENT_BALANCE` | 1 | 按量余额不足 | **禁止同参重试**。引导充值 |
| `RATE_LIMITED` | 1 | 短时间提交过多 | **禁止立即重试** |
| `DAILY_LIMIT` | 1 | 今日消费达到每日上限 | **禁止同参重试**。明日再试或到官网调整限额 |
| `INVALID_KEYWORD` | 1 | 关键词为空、超过 50 字、是链接或含 `< > " ' &` | 请用户换词。禁止自动改词 |
| `INVALID_URL` | 1 | 链接不含 weibo.com/ 或 weibo.cn/，或长度不在 1-255 | 请用户给单条微博链接 |
| `INVALID_ARGS` | 2 | 参数解析失败，或类目 / 搜索类型 / 排序 / 数量越界 | 按 `--help` 修正后重试一次。禁止改成默认值后自动再跑 |
| `NO_MATCH`（status=empty） | 0 | 无结果，不是失败 | 如实告知 |
| `TIMEOUT` / `NETWORK_ERROR` | 1 | 仍在处理，或网络失败 | 可同参再跑最多 1 次（窗口内是续等）。禁止改关键词、类目、排序或数量后当成重试 |
| `API_SCHEMA_CHANGED` | 1 | 成功响应不是数组 | 按失败报告，不要说成没有结果 |
| `API_ERROR` | 1 | 上游返回了未单独映射的业务码 | 转述 `message`。不要把裸数字码当成任务过期 |
| `HTTP_404` / `HTTP_410` / `HTTP_5xx` / `HTTP_*` | 1 | 传输层失败 | 如实报告。业务码里的 TOKEN 停用已经映射成 `AUTH_ERROR`，不要和 HTTP 410 混在一起 |

进程还在跑时不要判定失败。stderr 只给排障，不要原样贴给用户。
