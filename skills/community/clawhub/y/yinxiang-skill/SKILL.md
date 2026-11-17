---
name: yinxiang-skill
description: This skill should be used when the user says "授权印象笔记"、"印象笔记授权"、"配置印象笔记" to guide the authorization flow. Use this skill when the user says "记一下"、"帮我记录"、"存到笔记"、"记录一下"、"保存到笔记"、"帮我存一下"、"记到 XX 笔记本"、"存到 XX 笔记本" to save content to Evernote via API. Use this skill when the user says "更新笔记"、"修改笔记"、"编辑笔记"、"给笔记添加标签"、"删除笔记标签"、"清空笔记标签"、"修改笔记本"、"移动笔记" to update note title, Markdown content, notebook, or tags by note GUID; when updating tags, pass the complete final tag set in tagNames, and pass clearTags=true if the final tag set is empty or the user wants to clear all tags. Use this skill when the user asks to "批量创建笔记本"、"创建一套笔记本"、"创建笔记本体系"、"批量移动笔记"、"整理笔记" to decompose the request and call existing note APIs multiple times. Use this skill when the user sends a URL with "保存"、"剪藏"、"收藏" to clip the webpage. Use this skill when the user says "列出笔记"、"有哪些笔记"、"有什么笔记" to list notes. Use this skill when the user says "最近笔记"、"最近的笔记"、"查找最近笔记" to search notes created in the last 3 days. Use this skill when the user says "搜一下"、"搜下"、"帮我搜索"、"找找我哪些笔记提到了 XX" to search notes, or asks "有多少篇"、"一共多少篇"、"总数" for notes filtered by keyword, title, tag, notebook, note GUID, or created-time range. Use this skill when the user says "有哪些笔记本"、"有什么笔记本"、"列出笔记本" to list notebooks. Use this skill when the user says "创建笔记本"、"新建笔记本"、"建一个笔记本" to create a notebook. Use this skill when the user says "创建标签"、"新建标签"、"建一个标签" to create a standalone tag. Use this skill when the user says "有哪些标签"、"有什么标签"、"列出所有标签" to list tags. Use this skill when the user says "笔记详情 XXX"、"XXX 笔记详情" to get note detail.
version: 1.0.4
trigger:
  command: "/yinxiang"
metadata: {"openclaw": {"emoji": "📓", "primaryEnv": "YX_AUTH_TOKEN"}}
---

# YX Note - 印象笔记 Skill

## 重要说明

- **不要创建本地文件**代替调用 API
- **不要自行生成或猜测 token**
- **不要引导用户去 developer/token 页面**，正确授权地址是 `https://app.yinxiang.com/third/skills-oauth/`
- 优先使用 `scripts/` 中当前平台对应的脚本或 `references/api-commands.md` 中的命令调用 API；如果参考脚本疑似有误、在当前环境运行异常、输出格式不适合继续处理，或与接口文档/字段声明不一致，不要修改 skill 内置参考脚本，改为以 `references/api-commands.md` 的接口地址、请求字段、Token 规则为准，自行生成可运行的临时 bash/PowerShell 脚本并执行，真实调用 API。允许生成临时脚本来发起真实 API 请求；不得用本地文件、模拟数据或手写结果代替 API 调用结果，不得编造返回结果。
- 创建笔记和网页剪藏场景互斥：有 URL + 剪藏意图 → 场景三；纯文字记录 → 场景一
- **只推荐当前 skill 已支持的能力**。回答“还可以帮你...”或推荐下一步前，必须先核对下方原子能力列表；不要推荐未接入的能力。
- 用户要求未支持能力时，明确说明当前不支持，并给出已支持的替代操作；不要先推荐该能力再说无法实现。
- 支持范围以下方场景和原子能力列表为准；未列入的请求一律视为不支持，不调用脚本，不声称支持。
- 所有业务接口请求体都要传 `source` 标识请求来源，统一传 `"source":"skill"`。
- 可以根据接口返回的 `code`、`status.code`、`msg`、`message` 等字段判断结果，但用户可见回复不要展示接口原始返回、JSON 或技术字段。成功时用自然语言说明成功；无匹配结果时只说没有找到匹配内容；失败时参考 `message`/`msg` 的含义，结合用户原始请求改写成中文自然语言原因，不要照抄英文接口消息；如果没有可用原因，只说操作失败或出错。给出自然语言结论后，不要再追加“接口返回 code/status/msg/message 表示...”之类的解释。

---

## 平台检测

触发任意场景前，首先判断当前 shell 环境，**二选一执行**：

**若当前为 bash/zsh（macOS / Linux）：**
```bash
uname -s
```
返回 `Darwin` → macOS；返回 `Linux` → Linux。后续使用 **bash 命令**。

**若当前为 PowerShell（Windows）：**
```powershell
$env:OS
```
返回 `Windows_NT` → Windows。后续使用 **PowerShell 命令**。

> 判断依据：能否识别 `uname` 命令。可以 → bash 环境；不能（报错"未找到命令"）→ PowerShell 环境。

---

## Token 加载

所有 API 调用使用以下 Token 表达式：

| 平台 | Token 表达式 |
|------|-------------|
| OpenClaw | 自动注入 `YX_AUTH_TOKEN` 环境变量 |
| macOS / Linux (bash) | `$(cat ~/.config/yinxiang-skill/token 2>/dev/null \|\| echo "$YX_AUTH_TOKEN")` |
| Windows (PowerShell) | `$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }` |

---

## 前置检查

触发任意笔记场景前，验证 Token：

**macOS / Linux：**
```bash
bash -c 'T="$(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")"; [ -n "$T" ] && echo "已授权" || echo "未授权"'
```

**Windows (PowerShell)：**
```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }; if ($t) { "已授权" } else { "未授权" }
```

Token 为空 → 停止执行，提示用户说"授权印象笔记"。

---

## 复合任务与批量操作

用户一次提出多个操作时，先拆成当前 skill 已支持的能力，再按依赖顺序执行。
优先使用最匹配的已支持脚本或接口；如果没有专用批量能力，就循环调用原子能力。如果某一步没有对应能力，先向用户说明不支持该步骤。
下文脚本按当前平台选择：macOS/Linux 使用 `.sh`，Windows 使用 `.ps1`。

**原子能力：**
- 创建笔记：`scripts/create-note.sh` / `scripts/create-note.ps1`
- 更新/移动笔记/更新标签：`scripts/update-note.sh` / `scripts/update-note.ps1`
- 网页剪藏：`scripts/clip-url.sh` / `scripts/clip-url.ps1`
- 创建笔记本：`scripts/create-notebook.sh` / `scripts/create-notebook.ps1`
- 创建标签：`scripts/create-tag.sh` / `scripts/create-tag.ps1`
- 搜索笔记：`scripts/search-notes.sh` / `scripts/search-notes.ps1`
- 列出笔记：`scripts/list-notes.sh` / `scripts/list-notes.ps1`
- 列出笔记本：`scripts/list-notebooks.sh` / `scripts/list-notebooks.ps1`
- 列出标签：`scripts/list-tags.sh` / `scripts/list-tags.ps1`
- 获取笔记详情：`scripts/get-note-detail.sh` / `scripts/get-note-detail.ps1`

**批量操作通用规则：**
- 用户已明确给出所有操作对象时，可按顺序执行
- 需要 AI 搜索、推断、归类出来的操作对象，必须先让用户确认后再修改
- 修改类操作执行后，汇总成功项和失败项；部分失败时列出失败原因

**示例：批量创建笔记本**
- 用户明确列出笔记本名称时，直接提取所有一层笔记本名称
- 用户只要求“创建一套/一个体系”但未列出名称时，先给出拟创建的笔记本名称列表，等用户确认后再执行
- 确认名称后，按名称逐个执行创建笔记本脚本
- 汇总每个笔记本的创建结果；部分失败时列出失败项

**示例：批量移动笔记**
- 先确定目标笔记本；若用户给的是名称，先执行场景六获取 `notebookGuid`
- 若用户明确给出多个 `noteGuid`，逐个执行更新笔记脚本，仅传 `noteGuid` 和 `notebookGuid`
- 若用户只描述“同类型笔记”或“关于某主题的笔记”，先执行场景五搜索笔记或场景四列出笔记，让用户确认要移动的笔记列表
- 不要移动未确认的笔记；搜索得到的笔记列表必须经用户确认后才能批量移动
- 汇总每篇笔记的移动结果；部分失败时列出失败项

**复合任务示例：**
- 用户要求“创建 A、B、C 三个笔记本，并把这些笔记移动到 A”时，先逐个创建笔记本；若用户已明确给出 `noteGuid`，再逐个更新笔记的 `notebookGuid`；若需要搜索获取笔记，必须先让用户确认搜索结果
- 用户要求“给这些笔记加标签/删标签/清空标签”时，逐篇按更新笔记规则处理；增加或删除标签前先获取当前标签，计算最终标签全集。最终标签非空时传 `tagNames`，最终标签为空时传 `clearTags=true`；若这些笔记来自搜索结果，必须先让用户确认

---

## 授权场景

**触发词：** "授权印象笔记"、"印象笔记授权"、"配置印象笔记"

1. 告知用户访问授权地址：

   > 请访问 https://app.yinxiang.com/third/skills-oauth/ 完成授权。
   > 授权后页面显示以 **S=s** 开头的 Token，请发给我。

2. 收到 Token 后，按平台执行：

   **OpenClaw（macOS / Linux）：**
   ```bash
   openclaw config set skills.entries.yinxiang-skill.apiKey <Token> && mkdir -p ~/.config/yinxiang-skill && printf '%s' '<Token>' > ~/.config/yinxiang-skill/token && chmod 600 ~/.config/yinxiang-skill/token
   ```

   **OpenClaw（Windows）：**
   ```powershell
   openclaw config set skills.entries.yinxiang-skill.apiKey <Token>; New-Item -ItemType Directory -Force "$HOME\.config\yinxiang-skill" | Out-Null; Set-Content "$HOME\.config\yinxiang-skill\token" '<Token>' -NoNewline -Encoding UTF8
   ```

   **macOS / Linux (Claude Code / Codex / Cursor)：**
   ```bash
   mkdir -p ~/.config/yinxiang-skill && printf '%s' '<Token>' > ~/.config/yinxiang-skill/token && chmod 600 ~/.config/yinxiang-skill/token
   ```

   **Windows (Claude Code / Codex / Cursor)：**
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.config\yinxiang-skill" | Out-Null; Set-Content "$HOME\.config\yinxiang-skill\token" '<Token>' -NoNewline -Encoding UTF8
   ```

3. 告知用户授权成功，展示下方 10 个可用场景。

---

## 场景一：创建笔记

**触发词：** "记一下"、"帮我记录"、"存到笔记"、"记录一下"、"保存到笔记"、"帮我存一下"、"把这个记下来"

**逻辑：**
- 必须有要保存的正文内容；缺少正文时先询问用户要保存什么内容
- 正文支持 Markdown 标准语法，直接将用户内容以 Markdown 格式传入 `content` 字段
- 用户指定标签 → body 中追加 `"tagNames":["标签1","标签2"]`，不存在的标签自动创建
- 用户指定笔记本名称 → 先执行场景六获取列表，按名称匹配 `guid`
- 未指定笔记本 → 不传 `notebookGuid`，存入默认笔记本

读取 `references/api-commands.md`，按当前平台执行 **创建笔记** 部分对应命令。

---

## 场景二：更新笔记

**触发词：** "更新笔记"、"修改笔记"、"编辑笔记"、"给笔记添加标签"、"删除笔记标签"、"清空笔记标签"、"修改笔记本"、"移动笔记"

**逻辑：**
- 必须从用户消息中获取要更新的 `noteGuid`；缺少时先让用户提供笔记 ID
- 用户只提供标题或关键词但没有 `noteGuid` 时，先执行场景五搜索笔记或场景四列出笔记，让用户确认要更新的笔记 ID；搜索/列表结果只用于确认笔记 ID，不用于校验标签名称
- `title`、`content`、`notebookGuid`、`tagNames`、`clearTags` 均为可选更新字段
- `content` 为 Markdown 格式文本，服务端会转换为 HTML 后保存
- 只要本次更新包含 `content` 字段，即使用户已直接提供 `noteGuid`，也必须先提示并等待用户确认："确认要修改笔记内容吗？此操作会将笔记里的原有内容替换掉。" 用户确认后再调用更新笔记接口
- 更新标签时，`tagNames` 必须传更新后的标签全集，不是增量，也不是只传新增/删除的标签
- 用户要求增加或删除标签时，先执行场景十获取笔记详情，读取当前 `data.dataDetail.tagList[].tagName`，合并新增标签或移除指定标签后，计算完整最终标签列表
- 最终标签列表非空时，将完整最终标签列表作为 `tagNames` 传入，不传 `clearTags`
- 最终标签列表为空时，或用户明确要求清空所有标签时，必须传 `"clearTags":true`；不要只传空的 `tagNames`，后端会把空 `tagNames` 当作未修改标签
- 用户没有要求修改标签时，不传 `tagNames`，也不传 `clearTags`
- 用户指定笔记本名称但未提供 GUID → 先执行场景六获取列表，按名称匹配 `guid`
- 只修改笔记本时：仅传 `noteGuid` 和 `notebookGuid`
- 只设置标签时：仅传 `noteGuid` 和最终完整 `tagNames`
- 只清空标签时：仅传 `noteGuid`、`clearTags:true` 和 `source:"skill"`
- 例：当前只有标签 `a`，删除 `a` → 最终标签为 `[]` → 传 `clearTags:true`
- 例：当前标签为 `a`、`b`，删除 `a` → 最终标签为 `["b"]` → 传 `tagNames:["b"]`，不传 `clearTags`
- 例：用户说“清空所有标签” → 传 `clearTags:true`

读取 `references/api-commands.md`，按当前平台执行 **更新笔记** 部分对应命令。

---

## 场景三：网页剪藏

**触发词：** 消息中包含 URL + "保存"/"剪藏"/"收藏"

**逻辑：**
- 用户指定笔记本 → 先执行场景六匹配 `guid`，body 中追加
- 未指定笔记本 → 直接剪藏

读取 `references/api-commands.md`，按当前平台执行 **网页剪藏** 部分对应命令。

---

## 场景四：列出笔记

**触发词：** "列出笔记"、"有哪些笔记"、"我有哪些笔记"

读取 `references/api-commands.md`，按当前平台执行 **列出笔记** 部分对应命令。搜索/列表结果展示规则与场景五一致：展示搜索总数，以及响应中实际返回的笔记 ID 和标题；不要展示正文。用户说“最近笔记/最近的笔记/查找最近笔记”时，这不是列出笔记的独立能力，而是场景五的创建时间筛选条件。

---

## 场景五：搜索笔记

**触发词：** "搜一下"、"搜下"、"帮我搜索"、"找找我哪些笔记提到了"、"笔记里有没有关于"、"最近笔记"、"最近的笔记"、"查找最近笔记"、"有多少篇"、"一共多少篇"、"总数"

从用户消息提取关键词、标题、标签、笔记本、笔记 ID、笔记创建时间范围等条件，读取 `references/api-commands.md`，按当前平台执行 **搜索笔记** 部分对应命令。

搜索接口请求体只使用下方过滤条件映射和 `references/api-commands.md` 已列出的字段，不要添加接口未声明的参数。

**过滤条件映射：**
- 内容关键词 → `keyword`
- 标题关键词 → `title`
- 标签 → `tagNames`
- 笔记本名称 → `notebookName`
- 笔记本 GUID → `notebookGuid`
- 指定笔记 GUID 列表 → `guids`
- 笔记创建时间范围 → `startTime`、`endTime`，使用 UTC 毫秒时间戳
- 用户说“最近笔记/最近的笔记/查找最近笔记”，或在其他搜索条件里说“最近” → 将“最近”作为笔记创建时间筛选条件，按最近 3 天自动生成 `startTime` 和 `endTime`
- 用户问“有多少篇/总数/一共多少”时，仍调用搜索接口并读取 `data.total`

**时间处理规则：**
- 当前 skill 只支持按笔记创建时间查询，`startTime`、`endTime` 表示创建时间范围；不支持按更新时间、修改时间或编辑时间查询。
- 用户明确要求按“更新时间/修改时间/编辑时间/今天更新了哪些笔记”等条件查询时，不要直接按创建时间发起查询；先说明“当前我只支持按笔记创建时间查询，暂不支持按更新时间查询”，再询问是否改查对应时间范围内创建的笔记。
- 用户给出自然语言日期或时间时，先按用户所在本地时区理解该时间范围，再转换成 UTC 毫秒时间戳传给接口。
- 只给日期时，开始日期取当天 `00:00:00.000`，结束日期取当天 `23:59:59.999`，再转换成 UTC 毫秒时间戳。
- “今天/昨天/周五/最近两天”等相对日期或星期说法，先按用户所在本地时区和当前日期确定本地时间范围，再转换成 UTC 毫秒时间戳。
- 用户说“最近”时，不要追问，固定理解为最近 3 天；用当前时刻往前 3 天到当前时刻作为创建时间范围。
- “最近”可以和关键词、标题、标签、笔记本、笔记 ID 等条件组合，组合条件统一通过 `scripts/search-notes.* --json` 传入同一个请求体。

**时间意图示例：**
- 用户说“今天的笔记有哪些” → 查询今天本地 `00:00:00.000` 到 `23:59:59.999` 创建的笔记。
- 用户说“今天更新了哪些笔记” → 不直接查询；先说明当前只支持按笔记创建时间查询，并询问是否改查今天创建的笔记。
- 用户说“A 笔记本下最近有哪些笔记” → 同时传入笔记本条件和最近 3 天创建时间范围。

**结果展示规则：**
- 若响应包含 `data.total`，将其作为搜索总数；不要用返回列表长度代替总数。
- 笔记列表取 `data.noteDetailList` 或响应中实际存在的笔记列表字段；每条至少展示笔记 ID 和标题。笔记 ID 优先取 `noteGuid`，兼容 `guid` / `noteId`；标题优先取 `noteTitle`，兼容 `title`。
- 若返回 `status.code == 1107` 或 `data.total == 0`，只说没有找到匹配内容。
- 如果搜索总数 `< 100`，自然说明本次查询条件下的总数，然后展示笔记列表。
- 如果搜索总数 `>= 100`，必须根据 `data.total` 触发提示，即使接口本次实际返回列表少于 100 条也要提示。回复结构为：
  1. 自然说明本次查询条件下的总数，并追加固定话术：“为了避免列表太长影响阅读，最多返回100条笔记。”
  2. 单独一段使用固定话术：“受AI上下文长度限制，建议你让我对笔记做总结时，一次不要超过20篇。”
  3. 列出本次响应中可展示的笔记列表，最多 100 条。
- 不要向用户说明“接口实际返回 X 条”“本次返回列表数量”等技术细节；如果接口只返回了少于 100 条，就列出实际返回的这些条目即可。
- 不要展示正文；若用户需要完整内容，再用笔记 ID 调用场景十获取笔记详情。

---

## 场景六：列出笔记本

**触发词：** "有哪些笔记本"、"列出笔记本"、"我的笔记本"、"笔记本列表"

读取 `references/api-commands.md`，按当前平台执行 **列出笔记本** 部分对应命令。

---

## 场景七：列出标签

**触发词：** "有哪些标签"、"列出所有标签"、"我的标签"、"标签列表"

读取 `references/api-commands.md`，按当前平台执行 **列出标签** 部分对应命令。

---

## 场景八：创建标签

**触发词：** "创建标签"、"新建标签"、"建一个标签"

从用户消息提取标签名称替换 `TAG_NAME`，读取 `references/api-commands.md`，按当前平台执行 **创建标签** 部分对应命令。

接口返回 `code == 0` 表示成功，展示返回的 `tagGuid`。失败时参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因；如果没有可用原因，只告诉用户创建标签失败。不要直接展示接口返回字段和值，也不要照抄英文接口消息。

---

## 场景九：创建笔记本

**触发词：** "创建笔记本"、"新建笔记本"、"建一个笔记本"

从用户消息提取笔记本名称替换 `BOOK_NAME`，读取 `references/api-commands.md`，按当前平台执行 **创建笔记本** 部分对应命令。

接口返回 `code == 0` 表示成功，展示返回的 `notebookGuid`。失败时参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因；如果没有可用原因，只告诉用户创建笔记本失败。不要直接展示接口返回字段和值，也不要照抄英文接口消息。

---

## 场景十：获取笔记详情

**触发词：** "笔记详情 [ID]"、"[ID] 笔记详情"、"查看笔记 [ID]"

从用户消息提取笔记 GUID 替换 `GUID`，读取 `references/api-commands.md`，按当前平台执行 **获取笔记详情** 部分对应命令。

---

## 参考资料

- **`references/api-commands.md`** - 全部 10 个场景的完整命令（含 bash / PowerShell 两版）及响应处理
- **`scripts/save-token.sh`** - macOS / Linux 保存 Token
- **`scripts/save-token.ps1`** - Windows 保存 Token
- **`scripts/_common.sh`** - macOS / Linux 公共 Token 加载
- **`scripts/_common.ps1`** - Windows PowerShell 公共 Token 加载
- **`scripts/*.ps1`** - Windows 各场景独立脚本（Codex 直接调用）
- **`scripts/*.sh`** - macOS / Linux 各场景独立脚本（Codex 直接调用）
- **`templates/cursorrules`** - Cursor 专用模板，复制到项目根目录并重命名为 `.cursorrules`

## Cursor 使用说明

Cursor 不识别 SKILL.md，需手动配置：

1. 将 `templates/cursorrules` 复制到你的**项目根目录**，重命名为 `.cursorrules`
2. 重新打开 Cursor，即可使用所有触发词操作印象笔记
