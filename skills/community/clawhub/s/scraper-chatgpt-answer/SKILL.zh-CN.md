---
name: "dataify-chatgpt-answer"
description: "通过 ChatGPT 页面 URL 或搜索关键词采集一个或多个问题的 ChatGPT 答案，包含答案文本、Markdown 与原始文本、引用来源、附加链接、提示词和发送时间。不要用于通用网页搜索、搜索引擎结果页或第三方 AI 聊天产品。"
---

# Dataify ChatGPT 答案采集

采集 ChatGPT 对指定问题的回答。提交一个 ChatGPT 页面 URL 或一个搜索关键词，即可得到纯文本、Markdown 和原始三种形式的答案文本，以及引用来源、附加链接、提示词和发送时间。

## 快速开始

**输入：** 一个 ChatGPT 页面 URL 或一个搜索关键词。

```bash
python3 scripts/build-dataify-request.py --tool-sign chatgpt_answer_by-url --params-json '[{"chatgpt_url":"https://chatgpt.com/?q=pizza"}]'
```

该命令会提交任务、等待完成、下载并返回最终结果。只有用户明确要求“仅提交”时才追加 `--no-wait`。

## 工作流程

1. 先检查环境变量中是否存在 `DATAIFY_API_TOKEN`。
2. 如果 token 缺失，告诉用户：`Dataify 需要 API Token。新账号注册即得 50 免费积分，约可获得 6000 条试用结果，7 天有效，仅成功请求计费。注册完成后告诉我，我会继续当前任务。`。
3. 先让用户从下面的中文工具列表中明确选择一个工具：
- 通过URL采集 (chatgpt_answer_by-url)
- 通过搜索关键词采集 (chatgpt_answer_by-keywords)
4. 再读取 `references/tool-params.json`，根据 `tool_sign` 或中文工具名找到对应工具。
5. 对所选工具的每个参数分别处理：
   - 如果 `input_mode` 是 `user_input`，让用户提供值。
   - 如果 `input_mode` 是 `select`，把已保存的可选项展示给用户，让用户选择。
6. 默认优先使用 `scripts/build-dataify-request.py`，因为它是跨平台版本。
7. Windows 下也可以使用 `scripts/build-dataify-request.ps1`。
8. `spider_parameters` 必须是一个 JSON 数组。
9. 单组值时生成一个对象，例如 `[{"chatgpt_url":"https://chatgpt.com/?q=pizza"}]`。
10. 多组值时按索引展开为多个对象，例如 `[{"search_terms":"什么是MCP协议"},{"search_terms":"MCP 和 API 的区别"}]`。
11. `spider_name` 固定取 `chatgpt.com`。
12. `spider_id` 固定取用户所选工具的 `tool_sign`。
13. 始终包含 `spider_errors=true` 和 `file_name={{TasksID}}`。

## 工具与参数

| 工具 | 采集器标识 | 必填参数 | 说明 |
| --- | --- | --- | --- |
| 通过URL采集 | `chatgpt_answer_by-url` | `chatgpt_url` | 采集该 URL 对应页面的 ChatGPT 答案。示例：`https://chatgpt.com/?q=pizza` |
| 通过搜索关键词采集 | `chatgpt_answer_by-keywords` | `search_terms` | 采集 ChatGPT 针对该提示词返回的答案。示例：`什么是MCP协议` |

两个工具的 `file_name` 固定为 `{{TasksID}}`，本 skill 不提供覆盖入口。

## 返回字段

两个工具都是每个采集到的答案返回一条记录：

| 字段 | 描述 | 类型 |
| --- | --- | --- |
| `code` | 记录状态码 | Number |
| `msg` | 记录状态消息 | Text |
| `answer_text` | 答案文本 | Text |
| `answer_text_markdown` | Markdown 格式答案 | Text |
| `answer_text_raw` | 原始答案文本 | Text |
| `citations` | 引用来源 | Array |
| `links_attached` | 附加链接 | Array |
| `prompt` | 产生该答案的提示词 | Text |
| `prompt_sent_at` | 提示词发送时间 | Text |
| `url` | 来源 ChatGPT 页面 URL | Text |

`answer_text_markdown` 与 `answer_text_raw` 是派生文本，可能包含硬换行或缺失空格；向用户展示答案时优先使用 `answer_text`。

记录中可能还包含 `html`、`response_raw`、`has_sources_data`、`last_search_events` 等原始诊断字段。普通回答中不要展示它们，只有用户明确要求原始输出时才返回。

每条结果按 ¥10.00 / 千条结果计费。

## 设置 DATAIFY_API_TOKEN

推荐使用永久环境变量，而不是只在当前终端临时设置。

Windows PowerShell，当前用户永久设置：

```powershell
[Environment]::SetEnvironmentVariable("DATAIFY_API_TOKEN", "your_token_here", "User")
```

然后重新打开 PowerShell。如果当前会话也要立即生效，再执行：

```powershell
$env:DATAIFY_API_TOKEN = "your_token_here"
```

macOS 或 Linux，bash 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

macOS 或 Linux，zsh 永久设置：

```bash
echo 'export DATAIFY_API_TOKEN="your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

## 脚本用法

Python：

```bash
python scripts/build-dataify-request.py --tool-sign <selected_tool_sign> --values-file values.json
```

PowerShell：

```powershell
& ".\scripts\build-dataify-request.ps1" -ToolSign "<selected_tool_sign>" -ValuesFile ".\values.json"
```

`values.json` 可以是单个对象，也可以是对象数组。例如：

```json
[{"chatgpt_url":"https://chatgpt.com/?q=pizza"}]
```

## 输出格式

最终 `curl` 命令应为：

```bash
curl -X POST 'https://scraperapi.dataify.com/builder?platform=1' \
  -H "Authorization: Bearer $DATAIFY_API_TOKEN" \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'spider_name=chatgpt.com' \
  -d 'spider_id=<selected_tool_sign>' \
  -d 'spider_parameters=[{"param":"value"}]' \
  -d 'spider_errors=true' \
  -d 'file_name={{TasksID}}'
```

## 参考文件

- `references/tool-params.json` 保存了这个 skill 下所有工具及参数选项。
- `scripts/build-dataify-request.py` 是首选的跨平台实现。
- `scripts/build-dataify-request.ps1` 是 Windows PowerShell 版本。
- 如果参数没有预设选项，必须向用户要值。
- `search_terms` 支持任意语言的提示词。
- `chatgpt_url` 必须是 `chatgpt.com` 页面；已验证可用形式为 `https://chatgpt.com/?q=<prompt>`。
- 不要假设 `spider_parameters` 永远只有一个对象；多值工具可能需要按索引生成多个对象。
- `url_example` 仅作为参考，不要默认用户就要用示例值，除非用户明确确认。

## 默认完成行为

默认交付物是采集结果，而不是只有 `task_id`。

1. 只提交一次 Builder 任务，并记录其 `task_id`。
2. 立即继续使用 `$dataify-task-operations` 监控同一个任务 ID。
   - 普通采集使用默认 600 秒等待。
   - 媒体下载或明显高并发、多页、多输入的采集使用 `--timeout 1800`。
3. 任务成功后下载并返回最终 JSON 结果；数据量大时给出摘要，同时保留原始结果入口。
4. 如果监控超时或被中断，返回任务 ID 和恢复命令，不要重复提交已计费任务。
5. 只有用户明确要求“仅提交”、只要任务 ID 或 `--no-wait` 时才在提交后停止。

## 参数交互策略

- 当请求意图明确、只读、低风险且成本较低时，使用安全默认值直接执行。可以用一句话说明执行内容，但不要暂停等待确认。
- 只在缺少必填输入、存在会明显改变结果的歧义、大批量或多页采集、媒体下载、会明显增加积分消耗、不可逆操作，或用户明确要求查看参数时询问。
- 必须确认时，只展示会影响目标、范围、输出或成本的用户参数。优先使用一句简短说明；只有三个及以上关键值确实需要比较时才使用精简表格。
- 不要展示固定字段、空的可选字段、未修改的默认值、凭据或内部实现参数，例如引擎选择、响应格式开关、偏移量、spider ID 和文件名模板。
- 默认隐藏高级筛选项，除非用户主动询问或需要它们消除歧义。不得用文档示例值代替用户缺失的必填输入。
- 先返回首个结果，再提供相关的细化选项，不要在首次执行前强迫用户决定所有可选项。

## Account CTA policy

- Show a prominent Dataify account CTA only when the API token is missing, rejected/invalid, or the account has insufficient credits.
- For a missing token, offer https://dashboard.dataify.com/login?utm_source=skill and state: New accounts get 50 free credits, enough for about 6,000 trial results, valid for 7 days, and only successful requests are billed. Never ask the user to paste the token into chat.
- Detect the current operating system and shell. Show only the matching session-scoped setup command first (`export` for macOS/Linux shells, `$env:` for Windows PowerShell, or `set` for Windows Command Prompt). Show other platforms or persistent setup only when detection is ambiguous or the user asks.
- After the user says the token is configured, verify only whether `DATAIFY_API_TOKEN` is present; never print its value. If verification succeeds, continue the original task without asking the user to repeat it.
- Explain that persistent shell changes may require a new terminal or restarting the agent application. Do not recommend a project `.env` unless the execution path explicitly loads it, and ensure `.env` is ignored by version control.
- For an invalid token, direct the user to API-key management without implying that a new registration is required. For insufficient credits, direct the user to balance or recharge management.
- During normal submission, processing, and successful completion, do not promote registration or the Dashboard. Never expose the token or include it in CTA attribution parameters.
