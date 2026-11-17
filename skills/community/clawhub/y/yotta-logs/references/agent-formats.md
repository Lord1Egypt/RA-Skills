# AI 智能体会话 / 记忆存储格式普查登记表（agent-formats）

> v0.2.0 通用化依据：元史（yotta-logs）不再只认 JSONL，按「格式族 × 字段别名归一 + 配置兜底」适配一切格式。
> 本表是普查结论：6 大格式族、统一记录模型、字段别名映射、已知根与配置兜底。引擎行为见 `cli.md` / `format.md`。

## 一、总览：6 大格式族

| # | 格式族 | format | 代表智能体 / 存储 | 特征 |
|---|---|---|---|---|
| 1 | JSONL | jsonl | Claude Code / Codex CLI / Gemini 新版 / Copilot / Qwen / 多数会话 | 每行一个 JSON 对象，追加写入 |
| 2 | 单文件 JSON | json | Cline / Roo / Continue / Gemini 旧版 | 一个文件存整个会话 / 会话集（数组或对象） |
| 3 | SQLite | sqlite | opencode / Cursor state.vscdb / Trae / Copilot CLI session-store / CodeBuddy | 关系表存会话 / 消息 / 片段，字段多为 JSON 字符串 |
| 4 | Markdown | markdown | Aider .aider.chat.history.md / 各类自由笔记 | # 标题 + 正文 |
| 5 | 结构化 Markdown（YAML frontmatter） | markdown | yotta-memory / agent-code / opencode-agent-memory | --- frontmatter 元数据 + 正文 |
| 6 | 二进制 / 专有 / 加密 | binary | Windsurf pbtxt / Cascade / JetBrains Nitrite | 只降级读标题，不崩 |

## 二、统一记录模型 Record

所有 reader 产同构记录：`{source, format, kind, session, time, role, text, path, meta}`。

| 字段 | 说明 | 字段别名（按序取首个命中） |
|---|---|---|
| source | 来源名（如 codex-sessions / opencode-db / yottamemory-facts / codex-notes） | 来源登记名 |
| format | jsonl / json / sqlite / markdown / binary | 文件嗅探 / 配置 |
| kind | session / memory / note / log | 来源登记或逐记录判定 |
| session | 会话 ID / 文件名主干 / 相对路径 | session_id / thread_id / sessionId / session / conversation_id / threadId；缺省取文件主干 |
| time | 归一化 ISO 时间戳（秒 / 毫秒自动推断） | timestamp / time_created / created / time / ts / date / created_at / mtime / updated |
| role | user / assistant / tool / system / developer；结构化 md 的 type=FACT/PREF/BOUND/COMMIT → role | role / type / kind（message 内或 payload 内均可） |
| text | 人类可读文本 | text / content / body / message / statement；content 列表取 type=text / input_text / output_text |
| path | 绝对路径 | 文件路径 |
| meta | 额外字段（title / tags / tools / cost / tokens…） | title←title / subject / name / # 一级标题 |

## 三、各格式族详情

### 3.1 JSONL（jsonl）

- 代表：Claude Code（~/.claude/projects/*）、Codex CLI（~/.codex/sessions，CODEX_HOME 可覆盖；嵌套子目录）、Clawdbot（~/.clawdbot/agents/*/sessions）、opencode sessions 目录、Gemini 新版、Copilot、Qwen。
- 每行一个 JSON 对象：`type=session/message`；`message.role`；`message.content` 字符串或列表（type=text/toolCall/toolResult）；`message.usage`。
- Codex rollout 形态（本机实测 2026-08-27）：`{timestamp, type, payload:{type, role, content, usage}}`——`payload.type=message` 取 role / content；`payload.type=function_call / function_call_output / local_shell_call` 归一为 tool 并提取工具名；reasoning / event_msg 不进文本。
- 可选 `sessions.json` 索引（别名 → 会话 ID）。
- 容错：坏行跳过并计数，不中断。

### 3.2 单文件 JSON（json）

- 代表：Cline / Roo / Continue（~/.continue/sessions/*.json）、Gemini 旧版。
- 形态：JSON 数组（每条一个消息）；对象 {会话ID: [消息...]}；对象 {会话ID: 单消息}。
- 归一：数组逐条；对象遍历值。

### 3.3 SQLite（sqlite）

- 代表：opencode（~/.local/share/opencode/opencode.db；XDG_DATA_HOME / OPENCODE_DATA 可覆盖）、Cursor state.vscdb、Trae、Copilot CLI session-store、CodeBuddy。
- opencode 实测 schema（2026-08-27）：
  - `session(id, project_id, title, cost, tokens_input, tokens_output, time_created[毫秒], ...)`
  - `message(id, session_id, time_created[毫秒], data[JSON: role, time, agent, model, ...])`
  - `part(id, message_id, session_id, time_created[毫秒], data[JSON: type=text/tool/reasoning/step-start...])`——text 部分取 `text` 字段；tool 部分取 `tool` 字段为工具名。
- 只读连接：`sqlite3.connect("file:<path>?mode=ro", uri=True)`，绝不写库。
- 通用兜底：配置指定 `table / col_time / col_role / col_text / col_session / col_title`；未指定则按字段别名嗅探「消息类」表。

### 3.4 Markdown（markdown）

- 代表：Aider（repo 下 *.aider.chat.history.md）、各类自由笔记（Codex memories）。
- 无 frontmatter：`# 一级标题` → title，正文 → text，文件 mtime → time，kind=note。

### 3.5 结构化 Markdown（markdown + YAML frontmatter）

- 代表：yotta-memory（记忆库 facts / private / archive 下的 *.md）、agent-code、opencode-agent-memory。
- frontmatter：`type`（FACT/PREF/BOUND/COMMIT → role）、`subject` → title、`statement` → text、`created / updated / date` → time、`tags / confidence / scope / owner / immutable` → meta。
- 实测样本路径：`<memory_home>/facts/*.md`。`memory_home` 由 `YOTTA_MEMORY_HOME` 或 `~/.yottamemory/config.json` 决定。
- frontmatter 解析为零依赖 YAML 子集（key: value / key: [a, b] / 引号），非完整 YAML。

### 3.6 二进制 / 专有 / 加密（binary）

- 代表：Windsurf pbtxt（~/.codeium/windsurf/**/*.pbtxt）、Cascade、JetBrains Nitrite。
- 只降级读 title（文件名 / 首个可读片段），不崩；kind=log，默认关。

## 四、已知根（discover 全源登记）

| 来源名 | 根路径 | format | kind | 默认范围 |
|---|---|---|---|---|
| codex-sessions | ~/.codex/sessions（CODEX_HOME 覆盖，支持嵌套子目录） | jsonl | session | 开 |
| claude-projects | ~/.claude/projects/* | jsonl | session | 开 |
| clawdbot-sessions | ~/.clawdbot/agents/*/sessions | jsonl | session | 开 |
| opencode-sessions | ~/.config/opencode/sessions | jsonl | session | 开 |
| gemini-sessions | ~/.gemini/sessions | jsonl | session | 开 |
| agents-sessions | ~/.agents/sessions | jsonl | session | 开 |
| opencode-db | ~/.local/share/opencode/opencode.db；$XDG_DATA_HOME/opencode/opencode.db；$OPENCODE_DATA | sqlite | session | 开 |
| cursor-state / code-state | VS Code / Cursor globalStorage 下 state.vscdb（Windows / Linux / macOS） | sqlite | session | 开 |
| continue-sessions | ~/.continue/sessions、~/.config/continue/sessions | json | session | 开 |
| yottamemory-facts | 记忆库 facts（memory_home 配置） | markdown | memory | 开 |
| yottamemory-private | 记忆库 private（memory_home 配置） | markdown | memory | 开 |
| yottamemory-archive | 记忆库 archive（memory_home 配置） | markdown | memory | 开 |
| codex-notes | $CODEX_HOME/memories、~/.codex/memories | markdown | note | 关（显式开） |
| aider-history | 当前目录 *.aider.*.md | markdown | session | 开 |
| windsurf-conv | ~/.codeium/windsurf、~/.windsurf 下 *.pbtxt | binary | log | 关 |
| 自定义 sources | 配置 sources[]（见下） | 任意 | 任意 | 配置 default_scope |

## 五、配置兜底（config.json）

路径：`$YOTTA_LOGS_CONFIG`；未设置时使用平台默认位置：Windows = `%APPDATA%\yotta-logs\config.json`，Unix = `$XDG_CONFIG_HOME/yotta-logs/config.json` 或 `~/.config/yotta-logs/config.json`。

```json
{
  "default_scope": ["session", "memory"],
  "sources": [
    {
      "name": "myapp",
      "path": "/path/to/logs",
      "format": "sqlite",
      "kind": "session",
      "table": "messages",
      "col_time": "created_at",
      "col_role": "role",
      "col_text": "content",
      "col_session": "session_id",
      "col_title": "title"
    }
  ]
}
```

引擎零改动即可接入怪格式（个别 agent 私有 schema 用列映射接入）。

## 六、默认检索范围

- 会话源（kind=session）+ 结构化记忆源（kind=memory）**默认开**；
- 自由笔记（kind=note）与二进制日志（kind=log）**默认关**，可 `--kind note` / `--kind log` 显式开；
- 显式指定 `--dir / --source / --format / --kind` 时以显式条件为准。
