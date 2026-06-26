---
name: qq-mail-manager
description: QQ邮箱管理技能，支持收取、搜索、删除和发送邮件；当用户需要查看邮箱、查找邮件、管理邮件或发送邮件时使用
metadata: {"openclaw":{"requires":{"env":["QQ_EMAIL","QQ_EMAIL_AUTH_CODE"]},"primaryEnv":"QQ_EMAIL","envVars":[{"name":"QQ_EMAIL","required":true,"description":"QQ邮箱地址，例如 123456@qq.com"},{"name":"QQ_EMAIL_AUTH_CODE","required":true,"description":"QQ邮箱 IMAP/SMTP 授权码，不是 QQ 登录密码"}]}}
---

# QQ邮箱管理器

## 关键约束（必须遵守）

以下规则在每次操作中均不可违反，优先级高于所有其他指导：

1. **唯一定位**：所有操作必须使用 `folder + mail_id` 定位邮件。mail_id 仅在单个文件夹内唯一，禁止仅按 mail_id 定位、去重或操作
2. **操作确认**：删除/移动邮件必须先预览（不加 `--confirm`）并展示给用户，用户明确确认后才执行；发送邮件必须先展示收件人、主题、正文摘要，确认后才发送
3. **分页展示**：每次只调用一次 search_emails.py，将返回结果展示给用户。当 `has_more=true` 时，在末尾提示"还有更多邮件，需要查看下一页吗？"后停止——无论用户要求多少封、还差几封凑齐，都不得自行发起第二次调用，必须等用户明确要求翻页后才可使用 `--offset`
4. **表格模板**：向用户展示邮件信息时一律使用以下表格，即使只有一封邮件也必须使用，禁止自由叙述：

| folder | mail_id | 主题 | 发件人 | 日期 |
|--------|---------|------|--------|------|

5. **错误阻断**：脚本返回 `error` 或 `partial` 状态时，必须告知用户，不得继续执行删除/移动/发送等破坏性操作

## 任务目标
- 本 Skill 用于：管理QQ邮箱，实现邮件的收取、搜索、删除和发送
- 能力包含：列出文件夹、浏览/搜索邮件、查看邮件详情、下载附件、标记已读/未读、移动/删除邮件、发送邮件
- 触发条件：用户表达"查看邮件"、"搜索邮件"、"删除邮件"、"移动邮件"、"发送邮件"、"有哪些文件夹"等意图

## 前置准备
- 用户需在QQ邮箱中开启IMAP/SMTP服务并获取授权码（非QQ登录密码）
- OpenClaw 环境变量：`QQ_EMAIL`（邮箱地址）和 `QQ_EMAIL_AUTH_CODE`（QQ邮箱授权码）
- 脚本仍兼容旧 Coze 环境变量，但 OpenClaw 中优先使用上述通用变量
- 详细配置步骤见 [references/qq-email-config.md](references/qq-email-config.md)

## 操作步骤

### 1. 列出文件夹
```bash
python "{baseDir}/scripts/list_folders.py"
```
返回的 `name` 字段即为其他脚本 `--folder` 参数的可选值。

### 2. 浏览/搜索邮件
统一入口，无搜索条件时浏览邮件列表，有条件时搜索邮件。

**与 get_email 的边界**：
- `search_emails.py`：浏览/搜索邮件，返回摘要（编号、主题、发件人、日期）
- `get_email.py`：获取邮件完整内容（正文、附件列表），需先通过 search 找到 mail_id 后再调用
- 用户说"读取/查看某封邮件"时，应使用 get_email

**搜索模式选择规则**：
- 只有用户明确表达"语义搜索"意图时（如"帮我语义搜索"、"语义分析邮件"），才调用 `semantic_search.py`
- 其余所有情况一律使用 `search_emails.py`，包括浏览、关键词搜索、按字段搜索、按日期筛选
- 不要自行判断用户需求是否"需要语义理解"而擅自调用 semantic_search

**搜索词扩展规则**：
- 用户输入中文关键词时，自动补充对应英文/常用同义词，分别调用 `search_emails.py` 后按 `folder + mail_id` 合并去重
- 常见扩展："验证码"→`"验证码"+"verification code"`；"账单"→`"账单"+"bill"+"order"`；"会议"→`"会议"+"meeting"`；"通知"→`"通知"+"notification"+"notice"`

**分页规则**：
- `--limit`：期望返回的总结果数，不指定则返回全部
- `limit <= 15`：不分页，一次返回
- `limit > 15` 且 `total_matched > 15`：按15分页，用 `--offset` 翻页
- `total_matched <= 15`：无论 limit 多少，均一次返回
- **重要**：`--limit` 是搜索范围，不是"必须凑齐的数量"。每次只调一次脚本，展示当页结果，has_more=true 时等用户确认再翻页

```bash
# 浏览收件箱（不指定limit则返回全部，超过15封自动分页）
python "{baseDir}/scripts/search_emails.py" --folder INBOX

# 限定返回3封
python "{baseDir}/scripts/search_emails.py" --folder INBOX --limit 3

# 模糊搜索（匹配发件人、主题、收件人）
python "{baseDir}/scripts/search_emails.py" --query "会议" --folder INBOX

# 精确按字段搜索
python "{baseDir}/scripts/search_emails.py" --from "zhangsan@qq.com" --subject "通知"

# 日期范围筛选
python "{baseDir}/scripts/search_emails.py" --query "*" --since 2025-01-01 --before 2025-03-01

# 最近2小时的未读邮件
python "{baseDir}/scripts/search_emails.py" --query "*" --recent 2h --unseen

# 跨文件夹搜索
python "{baseDir}/scripts/search_emails.py" --query "验证码" --all-folders

# 翻页
python "{baseDir}/scripts/search_emails.py" --query "会议" --offset 15
```

### 3. 语义搜索
仅在用户明确触发时使用。拉取指定文件夹的邮件元数据+正文摘要，供智能体做语义判断。

**分类展示格式**：每组标题标注分类名+数量，禁止编号范围缩写（如"#12-51"），必须逐封列出：
```
验证码邮件（3封）：
- #12 您的验证码是123456 — noreply@example.com
- #37 验证码通知 — security@bank.com

订阅邮件（2封）：
- #8 本周技术周刊 — newsletter@tech.com
```

```bash
# 拉取收件箱最新100封邮件（默认）
python "{baseDir}/scripts/semantic_search.py" --folder INBOX

# 自定义拉取数量
python "{baseDir}/scripts/semantic_search.py" --folder INBOX --limit 50
```

### 4. 查看邮件详情
```bash
python "{baseDir}/scripts/get_email.py" --mail_ids <邮件编号> --folder INBOX
python "{baseDir}/scripts/get_email.py" --mail_ids 1,2,3 --folder INBOX
```
`--mail_ids` 和 `--folder` 均为必填，来自搜索结果中的字段。

### 5. 下载附件
```bash
python "{baseDir}/scripts/download_attachment.py" --mail_ids <编号> --folder INBOX --dir ./downloads
python "{baseDir}/scripts/download_attachment.py" --mail_ids <编号> --folder INBOX --file "报告.pdf"
```

### 6. 标记已读/未读
```bash
python "{baseDir}/scripts/mark_email.py" --mail_ids 123 --action read --folder INBOX
python "{baseDir}/scripts/mark_email.py" --mail_ids 1,2,3 --action unread --folder INBOX
```
`--action`：`read`=已读，`unread`=未读。

### 7. 移动/删除邮件
删除=移至垃圾箱，不支持永久删除。**必须先预览再确认**（见关键约束第2条）。

```bash
# 预览删除
python "{baseDir}/scripts/move_email.py" --mail_ids 1,2,3 --src_folder INBOX --delete
# 确认删除
python "{baseDir}/scripts/move_email.py" --mail_ids 1,2,3 --src_folder INBOX --delete --confirm

# 预览移动
python "{baseDir}/scripts/move_email.py" --mail_ids 5 --src_folder INBOX --dst_folder "Sent Messages"
# 确认移动
python "{baseDir}/scripts/move_email.py" --mail_ids 5 --src_folder INBOX --dst_folder "Sent Messages" --confirm
```

### 8. 发送/回复邮件
**发送前必须展示收件人、主题、正文摘要并确认**（见关键约束第2条）。

```bash
# 发送纯文本邮件
python "{baseDir}/scripts/send_email.py" --to <收件人> --subject "<主题>" --body "<正文>"

# 发送HTML邮件
python "{baseDir}/scripts/send_email.py" --to <收件人> --subject "<主题>" --body "<h1>Hello</h1>" --html

# 从文件读取正文（正文含换行/引号/HTML或超过200字符时优先使用）
python "{baseDir}/scripts/send_email.py" --to <收件人> --subject "<主题>" --body-file ./content.html --html

# 回复邮件
python "{baseDir}/scripts/send_email.py" --reply-to-id <邮件编号> --reply-folder INBOX --body "<回复内容>"

# 回复并引用原文
python "{baseDir}/scripts/send_email.py" --reply-to-id <邮件编号> --reply-folder INBOX --reply-quote --body "<回复内容>"

# 测试SMTP连接
python "{baseDir}/scripts/send_email.py" --test
```

## 资源索引
- 脚本: [scripts/list_folders.py](scripts/list_folders.py) — 列出所有邮箱文件夹，参数:无
- 脚本: [scripts/search_emails.py](scripts/search_emails.py) — 浏览/搜索邮件，支持跨文件夹。参数:
  - `--query` 模糊搜索（匹配发件人、主题、收件人），`*` 表示不限关键词
  - `--from` 精确按发件人搜索（优先于 --query）
  - `--subject` 精确按主题搜索（可与 --from 组合）
  - `--folder` 邮箱文件夹，默认 INBOX
  - `--all-folders` 搜索所有文件夹
  - `--since` 起始日期，含当天（YYYY-MM-DD）
  - `--before` 截止日期，不含当天（YYYY-MM-DD）
  - `--recent` 最近时间段（30m/2h/7d/1w），分钟/小时级别做二次精确过滤
  - `--seen`/`--unseen` 仅已读/未读（互斥）
  - `--limit` 期望总结果数，不指定返回全部，≤15不分页，>15按15分页
  - `--offset` 分页偏移量，默认0
- 脚本: [scripts/semantic_search.py](scripts/semantic_search.py) — 语义搜索，拉取邮件供智能体分析。参数: `--folder`(必填), `--limit`(默认100, 最大100)
- 脚本: [scripts/get_email.py](scripts/get_email.py) — 获取邮件详情。参数: `--mail_ids`(必填, 逗号分隔), `--folder`(必填)
- 脚本: [scripts/download_attachment.py](scripts/download_attachment.py) — 下载附件。参数: `--mail_ids`(必填, 逗号分隔), `--folder`(必填), `--dir`(输出目录, 默认当前目录), `--file`(仅下载指定附件名)
- 脚本: [scripts/mark_email.py](scripts/mark_email.py) — 标记已读/未读。参数: `--mail_ids`(必填), `--action`(read/unread), `--folder`(必填)
- 脚本: [scripts/move_email.py](scripts/move_email.py) — 移动或删除邮件。参数: `--mail_ids`(必填), `--src_folder`(必填), `--dst_folder`(与--delete二选一), `--delete`(移至垃圾箱, 与--dst_folder二选一), `--confirm`(确认执行, 不加则仅预览)
- 脚本: [scripts/send_email.py](scripts/send_email.py) — 发送/回复邮件。参数: `--to`(收件人, 回复模式可省略), `--subject`(主题, 与--subject-file二选一, 回复模式可省略), `--subject-file`(从文件读主题), `--body`(正文, 与--body-file二选一), `--body-file`(从文件读正文, 优先于--body), `--html`(HTML格式), `--cc`(抄送), `--bcc`(密送), `--attachments`(附件路径), `--reply-to-id`(回复邮件编号), `--reply-folder`(回复时必填), `--reply-quote`(引用原文), `--test`(测试SMTP)
- 参考: [references/qq-email-config.md](references/qq-email-config.md) — 凭证配置引导、授权码获取、服务器信息、常见问题

## 注意事项

### 展示细节
- **禁止编号范围缩写**：展示邮件列表时禁止使用"1-5"等范围缩写，必须逐封列出
- **删除预览**：除表格外还需显示收件时间
- **确认操作**：确认删除/移动/回复时也必须用表格展示 folder + mail_id
- **分组明确**：语义分类结果按类别分组，每组标题标注分类名+数量，编号不得跨组产生歧义

### 跨文件夹操作
- 跨文件夹搜索合并结果时，按 `folder + mail_id` 组合去重，不同文件夹中相同 mail_id 视为不同邮件
- 跨文件夹搜索（`--all-folders`）会遍历所有文件夹，文件夹较多时耗时较长

### 发送规范
- 正文含换行、引号、HTML 或超过200字符时，优先使用 `--body-file` 从文件读取，避免命令行转义问题
- 复杂主题使用 `--subject-file`

### 其他
- 不确定文件夹名称时，先调用 list_folders 获取可用值
- 删除邮件实际是移至垃圾箱，不支持永久删除
