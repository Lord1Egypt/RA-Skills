# 日志 / 记忆格式（format）

元史 v0.2.0 起按「格式族 × 字段别名归一 + 配置兜底」适配一切格式，统一产出 Record。
格式普查与各智能体存储位置见 `agent-formats.md`。

## 统一记录模型 Record

所有 reader 产同构记录：

| 字段 | 说明 |
|---|---|
| source | 来源名（codex-sessions / opencode-db / yottamemory-facts / codex-notes …） |
| format | jsonl / json / sqlite / markdown / binary |
| kind | session / memory / note / log |
| session | 会话 ID / 文件名主干 |
| time | 归一化 ISO 时间戳（秒 / 毫秒自动推断，Z 转 +00:00） |
| role | user / assistant / tool / system / developer；结构化 md 为 FACT/PREF/BOUND/COMMIT |
| text | 人类可读文本 |
| path | 绝对路径 |
| meta | 额外字段（title / tags / tools / cost / tokens_in / tokens_out / line …） |

## 字段别名归一（适配一切关键字段）

| 语义 | 别名（按序取首个命中） |
|---|---|
| time | timestamp / time_created / created / time / ts / date / created_at / mtime / updated |
| role | role / type / kind（message 内或 payload 内均可） |
| text | text / content / body / message / statement / text_content |
| session | session_id / thread_id / sessionId / session / conversation_id / threadId |
| title | title / subject / name / heading；md 无 frontmatter 时取 # 一级标题 |

- content 为列表时取 `type=text / input_text / output_text` 项；
- JSON 字符串字段自动解包一层；
- 秒 / 毫秒时间戳自动推断（13 位及以上按毫秒）。

## 各格式族读取规则

### JSONL（jsonl）

- 目录 = 会话集（支持嵌套子目录，如 Codex `sessions/2026/08/27/xxx.jsonl`）；可选 `sessions.json` 索引（别名 → 会话 ID）。
- 每行一个 JSON 对象；`message` / `payload` 内取 role / content / usage。
- Codex rollout 形态：`payload.type=message` 取 role / content；`function_call / function_call_output / local_shell_call` 归一为 tool 并提取工具名；reasoning / event_msg 不进文本。
- 坏行跳过并计入 invalid。

### 单文件 JSON（json）

- 数组 = 一条条消息；对象 = {会话ID: [消息...]} 或 {会话ID: 单消息}。

### SQLite（sqlite）

- 只读连接 `file:<path>?mode=ro`（uri=True），绝不写库。
- opencode schema 实测：session(id, title, cost, tokens_input, tokens_output, time_created[毫秒]) + message(id, session_id, data[JSON role]) + part(message_id, data[JSON type=text/tool/reasoning])。text 部分取 text 字段；tool 部分取 tool 字段为工具名；reasoning 不进文本。
- 通用兜底：配置指定 table / col_time / col_role / col_text / col_session / col_title；未指定则按字段别名嗅探消息类表。

### Markdown（markdown）

- 有 YAML frontmatter（`---` 开头）：type→role、subject→title、statement→text、created/updated/date→time、tags/confidence/scope/owner/immutable→meta；kind=memory。
- 无 frontmatter：# 一级标题→title，正文→text，mtime→time；kind=note。
- frontmatter 解析为零依赖 YAML 子集（key: value / key: [a, b] / 引号包裹）。

### 二进制 / 专有 / 加密（binary）

- 只降级读 title（文件名 / 首个可读片段），不崩；kind=log。

## 会话 ID 规则

- JSONL / Markdown / Binary：文件名主干（去掉扩展名）；
- 单文件 JSON 数组：文件主干；对象：键名（会话 ID）；
- SQLite：session 表 id（opencode）或 col_session 列值；无会话列时取文件主干。

## 容错规则

- 坏行 / 坏 JSON 字段跳过并计数（invalid），不中断检索；
- 二进制 / 加密文件只回退标题，不抛错；
- 所有读取均为只读，绝不修改 / 删除 / 写入。
