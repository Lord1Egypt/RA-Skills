---
name: tmeet-record-ledger
description: "Use the complete official Tencent Meeting record command family to locate recordings, retrieve native smart-minutes summaries and Todos, verify evidence in transcripts, handle recording-access requests, and produce a source-labeled meeting Todo ledger. Use for recording search, playback links, meeting summaries, Todo lists, transcript lookup, access requests, or unfinished follow-up reviews."
---

# 腾讯会议录制纪要待办

以 `tmeet record smart-minutes` 返回的原生智能纪要和待办为首选事实源，结合 `record` 命令树的录制定位、播放地址、转写核验和权限申请能力，整理“会议总结 + 待办账本”。调用 CLI 时完整遵守官方 `tmeet-skill` 的认证、分页、隐私、多结果确认和写操作二次确认规则。

## 命令子树

```text
tmeet
├── auth
│   ├── login
│   └── status
└── record
    ├── list
    ├── address
    ├── search
    ├── smart-minutes
    ├── transcript-get
    ├── transcript-paragraphs
    ├── transcript-search
    ├── permission-apply-prepare
    └── permission-apply-commit
```

本模块允许使用 `record` 下的全部官方命令，不局限于 `smart-minutes`；但不同命令按用户意图选择，不做无目的全量调用。

## 通用规则

1. 先运行 `tmeet auth status`；未登录时前台运行 `tmeet auth login`，不得后台运行。
2. macOS/Linux 使用 `tmeet`，Windows x64 使用 `tmeet.cmd`。
3. 查询命令默认追加 `--compact`；用户要求完整原始字段时除外。
4. 面向用户只展示主题、会议号、时间、必要的姓名与结果。`meeting_id`、`meeting_record_id`、`record_file_id` 仅在内部命令间传递，不回显。
5. 下载/播放地址可能含临时凭据，只在用户明确索取时展示，并注明过期时间，不写入待办账本。
6. 多条候选录制必须让用户选择，不按模型判断擅自选定。
7. 分页使用上一页 `data.next_page_token` 原值。用户未要求“全部”且还有下一页时先询问；超过 5 页或 200 条时再次询问。

## 命令选择

| 用户意图 | 命令与规则 |
|---|---|
| 按会议号或时间列录制 | `record list`；至少提供会议号、内部会议 ID、或完整起止时间中的一组 |
| 要播放/下载地址或取得录制文件 ID | `record address --meeting-record-id ...` |
| 按主题、创建人、纪要/转写内容、时间线或文件类型找录制 | `record search` |
| 要腾讯会议原生总结/Todo | `record smart-minutes --record-file-id ...` |
| 要连续转写详情或按段落位置读取 | `record transcript-get` |
| 要转写段落列表 | `record transcript-paragraphs` |
| 已知录制文件内查关键词 | `record transcript-search --text ...` |
| 内容命令返回无权限 | 先 `permission-apply-prepare`，确认后再 `permission-apply-commit` |

`record search --query-field` 只能使用 `subject`、`creator`、`transcript_content`、`smart_minutes`、`timeline`、`all`；`--file-type` 只能使用 `video`、`audio`、`transcript`、`upload`、`external`、`all`。

Windows PowerShell 示例必须单行书写：

```powershell
tmeet.cmd record list --meeting-code "<MEETING_CODE>" --compact
tmeet.cmd record search --query "<KEYWORD>" --query-field smart_minutes --compact
tmeet.cmd record address --meeting-record-id "<INTERNAL_RECORD_ID>" --compact
tmeet.cmd record smart-minutes --record-file-id "<INTERNAL_RECORD_FILE_ID>" --compact
tmeet.cmd record transcript-search --record-file-id "<INTERNAL_RECORD_FILE_ID>" --text "<KEYWORD>" --compact
```

## 总结与待办工作流

1. 用 `record list` 或 `record search` 定位录制；需要内容文件 ID 时再调用 `record address`。
2. 获取 `smart-minutes`。其原生总结、决议和 Todo 是第一事实源，不让 Agent 无依据重新猜一遍。
3. 仅在需要补充原话、发言人、上下文或时间点时读取 `transcript-get` / `transcript-paragraphs`；仅在用户给出关键词或核验目标时使用 `transcript-search`。
4. 标准化待办字段。责任人、截止时间或状态未明确时分别写“待确认”“待确认”“待处理（默认）”。
5. 同一会议的语义相同待办可以合并，但保留全部来源；不同会议不直接合并，只建立关联。
6. 用户要求长期保存时，将 Markdown/CSV/JSON 写到用户指定位置；未指定时先返回结果，不默认创建外部任务。

### 来源标记

按以下优先级和标签输出：

1. `smart-minutes`：腾讯会议原生智能纪要/原生 Todo。
2. `transcript`：原始转写证据，附段落或时间点。
3. `Agent整理（基于 transcript）`：原生 Todo 没有该项，但 Agent 从转写抽取出的候选待办。
4. `用户补充`：用户明确提供或更新的信息。

若 `smart-minutes` 没有原生 Todo，明确写“智能纪要未返回原生待办”。只有用户要求继续整理或接受兜底时，才从转写抽取候选项，并使用第 3 个标签，不能伪装成原生 Todo。

## 权限申请

`permission-apply-commit` 会发起真实审批，必须跨用户回合确认：

1. 内容命令返回无权限后，执行 `permission-apply-prepare --meeting-record-id ...`。
2. 展示申请类型、会议标题、录制所有者、申请备注、申请人和有效期；不得展示内部 ID。
3. 本轮结束并等待用户下一条真实消息明确确认。不能自问自答、默认同意或在同一回合 commit。
4. 收到确认后，检查 prepare 未过期，并使用同一录制调用 `permission-apply-commit`；过期则重新 prepare 并再次展示确认。
5. 返回审批状态和 `approval_url`。提交申请不等于已获权限；未批准前不能继续读取内容。

## 输出格式

```markdown
# 会议总结｜<会议主题>

- 会议时间：<含时区>
- 会议号：<meeting_code>
- 总结来源：<smart-minutes / transcript / 组合>

## 关键结论
1. <结论>｜来源：<标签和章节/时间点>

## 风险与未决问题
- <风险或“未发现明确记录”>

## 待办记录表
| # | 待办 | 责任人 | 截止时间 | 状态 | 原文依据 | 来源 |
|---:|---|---|---|---|---|---|
| 1 | <待办> | <姓名/待确认> | <时间/待确认> | <状态> | <章节/时间点> | <来源标签> |

## 待确认项
- <缺失或有歧义的信息>
```

用户问“还有什么没完成”时，只列出明确标为未完成、待处理或待确认的条目；没有外部任务系统时，不自行判断完成状态。

## 边界

- 只使用官方 `record` 命令族，不调用旧的 `minute` 或其他纪要命令族。
- 不自动创建、分派或更新 Jira、飞书、Asana 等外部任务，不自动发消息或邮件。
- 不把待办记录表说成已创建任务，不把权限申请说成已获批。
- 本模块可独立安装；主 Skill 只按 `$tmeet-record-ledger` 名称调用，不依赖兄弟模块目录。
