# CLI 协议（cli）

入口：`scripts/yotta_logs.py`（Python 3.8+ 标准库，零依赖）。

## 通用选项

| 选项 | 说明 |
|---|---|
| --dir PATH | 日志 / 记忆目录或文件；目录自动嗅探格式族（jsonl / json / sqlite / markdown），也支持单文件（含 .db / .md / .jsonl） |
| --source NAME | 只检索指定来源（可多次；名称见 locate 登记，如 codex-sessions / opencode-db / yottamemory-facts / codex-notes） |
| --kind KIND | 只检索指定类型：session / memory / note / log |
| --format FMT | 只检索指定格式：jsonl / json / sqlite / markdown / binary |
| --json | 输出纯净 JSON（stdout 无其它噪音） |
| --no-redact | 关闭默认脱敏 |
| --limit N | 最多返回 N 条（默认 50） |
| --version | 打印版本 |

未指定 --dir 时：依次尝试 YOTTA_LOGS_DIR → discover 全源登记（locate 逻辑），并按默认检索范围（会话 + 结构化记忆开、自由笔记 / 二进制日志关）过滤；显式 --source / --kind / --format 可覆盖默认范围。

## 子命令

### locate
全源登记：遍历所有 reader 的 discover()，登记本机存在的日志 / 记忆源（来源 / 格式 / 类型 / 路径 / 默认开关）。`--json` 输出 `{tool, version, default_scope, sources[]}`。无源退出码 1。

### scan
列出所有会话（跨源）：来源 / 会话 ID / 日期（首条消息）/ 消息数 / 大小 / 别名。支持 `--source/--kind/--format`、`--limit`（全局截断）、`--json`。空结果退出码 1。

### search <query>
跨源检索，输出时间线命中（来源 / 会话 / 时间 / 角色 / 原文片段）。

| 选项 | 说明 |
|---|---|
| --regex | 把 query 当正则（默认不区分大小写） |
| --date YYYY-MM-DD | 只检索指定日期（也支持 YYYY-MM） |
| -s / --session SID | 只检索指定会话 ID / 别名（可多次） |
| --role ROLE | user / assistant / tool / system / developer |
| --context N | 命中上下文半径字符数（默认 40） |
| --limit N | 最多返回 N 条（默认 50） |

--json 输出：`{command, tool, version, query, regex, sources[], total_matches, sessions_hit, truncated, matches[]}`，每条命中含 `source / format / kind / session / timestamp / role / line / match / text`。

### session <sid>
提取单个会话原文（时间线 + 角色 + 文本）。`--role` 过滤、`--tools` 标注工具调用、`--source/--kind/--format`、`--limit`、`--json`。未知会话退出码 4。跨源同名会话取第一个，可用 `--source` 消歧。

### stats
会话统计（跨源）：会话 / 消息 / 角色分布 / token / 成本 / 时间范围 / 分源（by_source）；`--daily` 输出每日汇总；`-s/--session` 限定单会话。空结果退出码 1。

### tools
工具调用次数排行（toolCall / toolResult / payload function_call 的工具名计数），`-s/--session` 限定单会话。

### version
打印 `yotta-logs 0.2.0`。

## 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功（检索到结果 / 操作完成） |
| 1 | 无匹配 / 空结果集 |
| 4 | 用法错误 / 路径不存在 / 未知会话 / 致命异常 |

## JSON 输出约定

- stdout 只输出 JSON，进度 / 提示走 stderr；
- `ensure_ascii=False`，中文原样输出；stdout 已重配 UTF-8（GBK 控制台不炸）。

## 配置（配置兜底）

- 配置文件：`$YOTTA_LOGS_CONFIG`；未设置时 Windows 用 `%APPDATA%\yotta-logs\config.json`，Unix 用 `$XDG_CONFIG_HOME/yotta-logs/config.json` 或 `~/.config/yotta-logs/config.json`；
- `default_scope`：默认检索范围（默认 `["session", "memory"]`）；
- `sources[]`：自定义源（path / format / kind / name / table / col_time / col_role / col_text / col_session / col_title），引擎零改动接入怪格式。
- 示例见 `agent-formats.md` 第五节。
