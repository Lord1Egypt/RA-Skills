# 参数取值

只在拼参或核对枚举时读。

## 热搜 `hot-cli.js`

| flag | 默认 | 允许 |
| --- | --- | --- |
| `--category` / `-c` | `realtimehot` | `realtimehot` 实时、`fun` 文娱、`social` 社会、`sportnav` 体育、`lifenav` 生活、`gamenav` ACG、`technologynav` 科技 |

省略类目 = 实时热搜。写出不在表内的值 → `INVALID_ARGS`，不会改回 `realtimehot`。

## 搜索 `search-cli.js`

| flag | 默认 | 允许 |
| --- | --- | --- |
| `--keyword` / `-k` | 必填 | 1-50 字；不能是链接；不含 `< > " ' &` |
| `--search-type` / `-s` | `1` | `1` 综合、`2` 实时、`3` 用户、`4` 视频、`5` 热门、`6` 话题、`7` 超话 |
| `--limit` / `-l` | `10` | 整数 1-10000。包月实际最多 30 |

只接受上表 1-7。不要传采集侧其它数字。

## 评论 `comment-cli.js`

| flag | 默认 | 允许 |
| --- | --- | --- |
| `--url` / `-u` | 必填 | 含 `weibo.com/` 或 `weibo.cn/`，1-255 字 |
| `--sort` / `-s` | `0` | `0` 按热度、`1` 按时间 |
| `--limit` / `-l` | `10` | 整数 1-10000。包月实际最多 50 |

常见链接：`weibo.com/<uid>/<mid>`、`weibo.com/detail/<mid>`、`weibo.com/status/<mid>`、`m.weibo.cn/detail/<mid>`、`m.weibo.cn/status/<mid>`。

## 共用

- `--save`：把完整信封写入本地日志。也可设环境变量 `GUAIKEI_ENABLE_LOG=1`。
- `--json-args`：一个 JSON 对象，键名是 `category` / `keyword` / `search_type` / `url` / `sort` / `limit` / `save`，与其它 flag 互斥。
- `--help` / `-h`：只打印帮助，退出码 0，不请求接口。
