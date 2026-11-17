# 印象笔记 API 命令参考

## Token 变量说明

| 平台 | Token 表达式 |
|------|-------------|
| macOS / Linux (bash) | `$(cat ~/.config/yinxiang-skill/token 2>/dev/null \|\| echo "$YX_AUTH_TOKEN")` |
| Windows (PowerShell) | `$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }` |

以下各场景分别提供 **bash** 和 **PowerShell** 两种命令，按实际运行平台选用。

所有业务接口请求体都要传 `source` 标识请求来源，统一传 `"source":"skill"`。

如果 `scripts/` 中的参考脚本疑似有误、在当前环境运行异常、输出格式不适合继续处理，或与本文档的接口地址、请求字段或 Token 规则不一致，不要修改 skill 内置参考脚本，改为以本文档为准，自行生成可运行的临时 bash/PowerShell 脚本并执行，真实调用 API。允许生成临时脚本来发起真实 API 请求；不得用本地文件、模拟数据或手写结果代替 API 调用结果，不得编造返回结果。

可以根据接口返回的 `code`、`status.code`、`msg`、`message` 等字段判断结果，但用户可见回复不要展示接口原始返回、JSON 或技术字段。成功时用自然语言说明成功；失败时参考 `message`/`msg` 的含义，结合用户原始请求改写成中文自然语言原因，不要照抄英文接口消息；如果没有可用原因，只说操作失败或出错。给出自然语言结论后，不要再追加“接口返回 code/status/msg/message 表示...”之类的解释。

---

## 创建笔记

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNoteFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"title":"TITLE","content":"CONTENT","source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"title":"TITLE","content":"CONTENT","source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNoteFromMCP" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

- `content` 为笔记正文，支持 Markdown 标准语法
- 创建笔记必须有正文内容；缺少正文时先询问用户
- 指定笔记本时追加 `"notebookGuid":"GUID"`
- 指定标签时追加 `"tagNames":["标签1","标签2"]`（标签名数组，不存在的标签会自动创建）

返回 `{"code":0}` 表示成功；否则参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因。回复用户时不要直接展示接口返回字段，不要照抄英文接口消息，例如不要写“接口返回 code=.../message=...”，应说“创建失败：原因”或简单说“创建失败”。

---

## 更新笔记

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"noteGuid":"GUID","title":"TITLE","content":"CONTENT","notebookGuid":"NOTEBOOK_GUID","tagNames":["标签1","标签2"],"source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"noteGuid":"GUID","title":"TITLE","content":"CONTENT","notebookGuid":"NOTEBOOK_GUID","tagNames":["标签1","标签2"],"source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

- `noteGuid` 为要更新的笔记 GUID，必填
- 用户只提供标题或关键词但没有 `noteGuid` 时，先搜索笔记或列出笔记，让用户确认要更新的笔记 ID；搜索/列表结果只用于确认笔记 ID，不用于校验标签名称
- `title`、`content`、`notebookGuid`、`tagNames`、`clearTags` 为可选更新字段
- `content` 为 Markdown 格式文本，服务端会转换为 HTML 后保存
- 请求体包含 `content` 字段时，即使用户已直接提供 `noteGuid`，也必须先提示并等待用户确认："确认要修改笔记内容吗？此操作会将笔记里的原有内容替换掉。" 用户确认后再调用更新笔记接口
- `tagNames` 为标签名称数组，表示更新后的标签全集，不是增量
- 增加或删除标签时，先获取笔记详情中的当前 `data.dataDetail.tagList[].tagName`，合并或移除后计算完整最终标签列表
- 最终标签列表非空时，传完整最终 `tagNames`，不传 `clearTags`
- 最终标签列表为空时，或用户明确要求清空全部标签时，必须传 `"clearTags":true`；不要只传空数组 `tagNames: []`，后端会把空 `tagNames` 当作未修改标签
- 用户没有要求修改标签时，不传 `tagNames`，也不传 `clearTags`
- 返回 `{"code":0}` 表示成功；成功时取 `noteGuid`；否则参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因。回复用户时不要直接展示接口返回字段，不要照抄英文接口消息，应说“更新失败：原因”或简单说“更新失败”

清空标签请求示例：

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"noteGuid":"GUID","clearTags":true,"source":"skill"}'
```

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"noteGuid":"GUID","clearTags":true,"source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/updateNoteFromMCP" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

常用脚本调用：

```bash
# macOS / Linux
scripts/update-note.sh "GUID" "新的标题"
scripts/update-note.sh "GUID" "" "# 新内容"
scripts/update-note.sh "GUID" "" "" "NOTEBOOK_GUID"
scripts/update-note.sh "GUID" "" "" "" "工作,重要"
scripts/update-note.sh "GUID" "" "" "" ""
```

```powershell
# Windows
.\scripts\update-note.ps1 -NoteGuid "GUID" -Title "新的标题"
.\scripts\update-note.ps1 -NoteGuid "GUID" -Content "# 新内容"
.\scripts\update-note.ps1 -NoteGuid "GUID" -NotebookGuid "NOTEBOOK_GUID"
.\scripts\update-note.ps1 -NoteGuid "GUID" -TagNames @("工作","重要")
.\scripts\update-note.ps1 -NoteGuid "GUID" -ClearTags
```

---

## 网页剪藏

剪藏场景优先参考 `scripts/clip-url.sh` / `scripts/clip-url.ps1` 的流程实现，因为脚本已包含“后台发起剪藏请求、最多等待 5 秒读取接口返回、等待超时不终止剪藏请求”的处理。若脚本在当前环境不可用、执行异常，或与本文档接口地址/请求字段不一致，可参考脚本逻辑自行生成等价命令；等价命令必须保留：后台请求继续执行、最多等待 5 秒观察返回、5 秒内无返回时回复固定话术、5 秒内有返回时输出接口响应并按通用结果规则判断成功或失败。

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/clipper-gateway/restful/v1/clipAndSaveNote" \
  -H "Content-Type: text/plain" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -H "clipper-c-auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"url":"URL","source":"skill"}' &
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"url":"URL","source":"skill"}'
Start-Job { param($t,$b) Invoke-WebRequest -Uri "https://app.yinxiang.com/third/clipper-gateway/restful/v1/clipAndSaveNote" -Method POST -Headers @{auth=$t;"clipper-c-auth"=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($b)) -ContentType "text/plain; charset=utf-8" -UseBasicParsing } -ArgumentList $t,$body
```

指定笔记本时，请求体追加 `"notebookGuid":"GUID"`。

结果处理：
- 后台发起剪藏请求，最多等待 5 秒读取接口返回；等待超时也不要终止剪藏请求
- 5 秒内没有拿到接口返回时，告知“剪藏任务已提交，请稍后到APP里查看剪藏结果”
- 5 秒内拿到接口返回时，按通用结果规则判断；`code == 0` 或 `status.code == 0` 表示提交成功。成功时结合返回内容自然说明剪藏结果；如果返回中包含笔记 ID 等关键信息，可以一并展示
- 如果接口返回失败、`code` / `status.code` 表示失败，或响应里有明确失败结果，参考 `message` / `msg` 字段，结合用户请求改写成中文失败原因

---

## 列出笔记

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

- `data.total` 表示当前查询条件下的笔记总数；不要用返回列表长度代替 `data.total`
- `data.noteDetailList` 中每条笔记至少按实际字段展示笔记 ID 和标题：笔记 ID 优先取 `noteGuid`，兼容 `guid` / `noteId`；标题优先取 `noteTitle`，兼容 `title`
- 用户说“最近笔记/最近的笔记/查找最近笔记”，或在其他搜索条件里说“最近”时，将“最近”作为笔记创建时间筛选条件，固定按最近 3 天生成 `startTime` 和 `endTime`，单位为 UTC 毫秒时间戳
- 不要展示正文；若用户需要完整内容，必须再用笔记 ID 调用 **获取笔记详情** 接口
- 总数 `< 100` 时，自然说明本次查询条件下的总数，然后展示笔记列表。
- 总数 `>= 100` 时，必须根据 `data.total` 触发提示，即使接口本次实际返回列表少于 100 条也要提示。回复结构为：
  1. 自然说明本次查询条件下的总数，并追加固定话术：“为了避免列表太长影响阅读，最多返回100条笔记。”
  2. 单独一段使用固定话术：“受AI上下文长度限制，建议你让我对笔记做总结时，一次不要超过20篇。”
  3. 列出本次响应中可展示的笔记列表，最多 100 条。
- 不要向用户说明“接口实际返回 X 条”“本次返回列表数量”等技术细节；如果接口只返回了少于 100 条，就列出实际返回的这些条目即可。

---

## 搜索笔记

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"keyword":"KEYWORD","source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"keyword":"KEYWORD","source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/searchNotesByFilter" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

复杂条件搜索使用同一接口，按需传入 JSON；只传用户明确要求的过滤字段：

```bash
scripts/search-notes.sh --json '{"keyword":"复盘","notebookGuid":"nb_123","tagNames":["工作","项目A"],"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
scripts/search-notes.sh --json '{"keyword":"复盘","startTime":1782835200000,"endTime":1785513599999,"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
```

```powershell
.\scripts\search-notes.ps1 -Json '{"keyword":"复盘","notebookGuid":"nb_123","tagNames":["工作","项目A"],"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
.\scripts\search-notes.ps1 -Json '{"keyword":"复盘","startTime":1782835200000,"endTime":1785513599999,"source":"skill","resultSpec":{"includeContent":false,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
```

请求字段：

- `source`：请求来源，固定传 `skill`
- `keyword`：全文关键词，可选
- `title`：标题关键词，可选
- `tagNames`：标签名数组，可选
- `notebookName`：笔记本名称，可选
- `notebookGuid`：笔记本 GUID，可选；已知 GUID 时优先只传 `notebookGuid`，不要同时传 `notebookName`
- `guids`：指定笔记 GUID 数组，可选
- `startTime`、`endTime`：笔记创建时间范围，可选，单位为 UTC 毫秒时间戳
- 不要添加搜索接口未声明的参数。
- 当前 skill 只支持按笔记创建时间查询，`startTime`、`endTime` 表示创建时间范围；不支持按更新时间、修改时间或编辑时间查询。
- 用户明确要求按“更新时间/修改时间/编辑时间/今天更新了哪些笔记”等条件查询时，不要直接按创建时间发起查询；先说明“当前我只支持按笔记创建时间查询，暂不支持按更新时间查询”，再询问是否改查对应时间范围内创建的笔记。
- 用户给出自然语言日期或时间时，先按用户所在本地时区理解该时间范围，再转换成 UTC 毫秒时间戳传给接口。
- 只给日期时，开始日期取当天 `00:00:00.000`，结束日期取当天 `23:59:59.999`，再转换成 UTC 毫秒时间戳。
- “今天/昨天/周五/最近两天”等相对日期或星期说法，先按用户所在本地时区和当前日期确定本地时间范围，再转换成 UTC 毫秒时间戳。
- 用户说“最近”时，不要追问，固定理解为最近 3 天，直接按最近 3 天的笔记创建时间搜索。
- “最近”可以和关键词、标题、标签、笔记本、笔记 ID 等条件组合，组合条件统一通过 `scripts/search-notes.* --json` 传入同一个请求体。
- 不要基于搜索/列表结果校验标签名称。

时间意图示例：

- 用户说“今天的笔记有哪些” → 查询今天本地 `00:00:00.000` 到 `23:59:59.999` 创建的笔记
- 用户说“今天更新了哪些笔记” → 不直接查询；先说明当前只支持按笔记创建时间查询，并询问是否改查今天创建的笔记
- 用户说“A 笔记本下最近有哪些笔记” → 同时传入笔记本条件和最近 3 天创建时间范围

响应字段：

- `data.total` 表示匹配关键词和过滤条件的笔记总数
- 笔记列表取 `data.noteDetailList` 或响应中实际存在的笔记列表字段；每条至少展示笔记 ID 和标题。笔记 ID 优先取 `noteGuid`，兼容 `guid` / `noteId`；标题优先取 `noteTitle`，兼容 `title`
- 不要用返回列表数量代替 `data.total`；用户可见回复里不要说明“接口实际返回 X 条”“本次返回列表数量”等技术细节
- `status.code == 1107` 表示后端明确返回无结果
- `status.code` 成功但 `data.total == 0` 表示查询成功且匹配总数为 0
- 查询成功时展示 `data.total` 和响应中实际返回的笔记 ID、标题
- 总数 `< 100` 时，自然说明本次查询条件下的总数，然后展示笔记列表
- 总数 `>= 100` 时，必须根据 `data.total` 触发提示，即使接口本次实际返回列表少于 100 条也要提示。回复结构为：
  1. 自然说明本次查询条件下的总数，并追加固定话术：“为了避免列表太长影响阅读，最多返回100条笔记。”
  2. 单独一段使用固定话术：“受AI上下文长度限制，建议你让我对笔记做总结时，一次不要超过20篇。”
  3. 列出本次响应中可展示的笔记列表，最多 100 条
- 不要向用户说明“接口实际返回 X 条”“本次返回列表数量”等技术细节；如果接口只返回了少于 100 条，就列出实际返回的这些条目即可
- 不要展示正文；若用户需要完整内容，再用笔记 ID 调用 **获取笔记详情** 接口
- 查询失败时参考 `message`/`msg` 字段的语义线索，结合用户查询对象改写成中文自然语言原因；如果没有可用原因，只告诉用户搜索笔记失败或出错。不要直接展示接口返回字段和值，也不要照抄英文接口消息

---

## 列出笔记本

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listNoteBooks" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listNoteBooks" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

取 `data.noteBookList`，展示 `name` 和 `guid`。

---

## 列出标签

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listTags" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/listTags" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

取 `data.tagList`，展示 `tagName` 和 `tagGuid`。

---

## 创建标签

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createTagFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"tagName":"TAG_NAME","source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"tagName":"TAG_NAME","source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createTagFromMCP" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

- `tagName` 为标签名称，必填
- 返回 `{"code":0}` 表示成功
- 成功时取 `tagGuid`
- 失败时参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因；回复用户时不要直接展示接口返回字段，不要照抄英文接口消息，应说“创建标签失败：原因”或简单说“创建标签失败”

---

## 创建笔记本

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNotebookFromMCP" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"bookName":"BOOK_NAME","source":"skill"}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"bookName":"BOOK_NAME","source":"skill"}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/third-party-note-service/restful/v1/createNotebookFromMCP" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

- `bookName` 为笔记本名称，必填
- 返回 `{"code":0}` 表示成功
- 成功时取 `notebookGuid`，这是新建或已存在的同名笔记本 GUID
- 失败时参考 `message` 字段的语义线索，结合用户请求改写成中文自然语言原因；回复用户时不要直接展示接口返回字段，不要照抄英文接口消息，应说“创建笔记本失败：原因”或简单说“创建笔记本失败”

---

## 获取笔记详情

### macOS / Linux (bash)

```bash
curl -s -X POST \
  "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/getNoteDetail" \
  -H "Content-Type: application/json" \
  -H "auth: $(cat ~/.config/yinxiang-skill/token 2>/dev/null || echo "$YX_AUTH_TOKEN")" \
  -d '{"guid":"GUID","source":"skill","resultSpec":{"includeContent":true,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
```

### Windows (PowerShell)

```powershell
$raw = Get-Content "$HOME\.config\yinxiang-skill\token" -Raw -EA SilentlyContinue; $t = if ($raw) { $raw.Trim() } elseif ($env:YX_AUTH_TOKEN) { $env:YX_AUTH_TOKEN.Trim() }
$body = '{"guid":"GUID","source":"skill","resultSpec":{"includeContent":true,"includeResources":false,"includeTags":true,"includeResourceContent":false}}'
$r = Invoke-WebRequest -Uri "https://app.yinxiang.com/third/ai-chat-note/grpc-api/search/getNoteDetail" -Method POST -Headers @{auth=$t} -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) -ContentType "application/json; charset=utf-8" -UseBasicParsing
$r.Content
```

取 `data.dataDetail`，展示笔记完整内容。
