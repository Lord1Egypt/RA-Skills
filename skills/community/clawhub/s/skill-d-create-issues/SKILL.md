---
name: skill-d-create-issues
description: "【issue 落地总控】当组织者确认 issue 草稿后触发。触发方式：(A) 组织者在 Gitea 把 draft_issue.md 改名为 confirmed_issue.md，由 webhook 通知 OpenClaw；(B) 组织者在 OpenClaw 中说"确认 YYYY-MM-DD-HHMM 的 issue"。触发关键词：确认issue、创建issue、落地issue、confirmed_issue、批量建issue。不处理会议创建、会前简报、会后纪要等场景。"
author: mayidan
---

# Skill-D: create_issues — issue 落地总控

## 定位

本技能是 **事件驱动的 issue 落地流程总控**。由组织者确认 issue 草稿后触发，非 cron。

职责分工：

- **OpenClaw**
  - 被 webhook 或对话触发后，调用 `check` 验证前置条件
  - 读取 `confirmed_issue.md` 内容，解析出每条 action item 的结构化字段
  - 判断 `meeting_category`（single / cross-project）
  - 单项目：调用 `create-issues` 批量建 Gitea issue
  - 调用 `finish` 收尾，获取邮件参数
  - 调用 imap-smtp-email 发送正式纪要邮件（全员）+ 个人任务通知（各 assignee）
  - 跨项目：调用 `finish`（跳过建 issue），调用 imap-smtp-email 向组织者发建议邮件

- **Skill-D（本技能）**
  - `check`：校验 meta.yaml status 和 confirmed_issue.md 存在性，返回内容与元信息
  - `create-issues`：接收 OpenClaw 解析好的 JSON，批量在 Gitea 建 issue + 依赖回填
  - `finish`：meta.yaml → minutes-published，写 created_issues 字段，写日志，返回邮件参数
  - `webhook.py`：独立常驻进程，监听 Gitea push webhook，检测到 confirmed_issue.md 时向 OpenClaw 发送触发信号

- **imap-smtp-email**
  - 发送正式纪要邮件（全体参会人）
  - 发送个人任务通知邮件（各 assignee 单独一封）
  - 发送跨项目 issue 建议邮件（组织者）

---

## 配置要求

配置文件：`~/.config/skill-d-create-issues/.env`

首次使用前运行：

```bash
bash setup.sh
```

---

## 触发方式

### 方式 A：Gitea Webhook（推荐）

组织者在 Gitea 网页将 `draft_issue.md` 改名为 `confirmed_issue.md`，触发 push webhook。

**Webhook 配置步骤：**
1. 在每个受管仓库（包括 aifusion-meta）的 Settings → Webhooks → Add Webhook
2. URL：`http://43.156.243.152:<WEBHOOK_PORT>/gitea-webhook`（端口见 .env）
3. Content Type：`application/json`
4. Trigger：`Push Events`

**启动 Webhook 监听服务（后台常驻）：**

```bash
nohup python3 scripts/webhook.py > ~/.config/skill-d-create-issues/webhook.log 2>&1 &
```

### 方式 B：OpenClaw 对话

```
用户："确认 2026-04-22-1500 的 issue"
```

OpenClaw 识别后，询问用户确认的是哪个仓库（如果上下文不明确），然后进入以下工作流。

---

## 严格工作流（两种触发方式执行相同流程）

---

### 第一步：调用 check，验证前置条件

```bash
node main.js check \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500"
```

返回 JSON，关键字段：

- `valid`：true / false（false 时含 `reason` 字段，OpenClaw 直接告知用户）
- `category`：`single` | `cross-project`
- `topic`、`organizer`、`organizer_email`、`attendees`、`attendee_emails`
- `confirmed_issue_content`：confirmed_issue.md 的完整文本
- `minutes_content`：minutes.md 的完整文本（用于正式纪要邮件）
- `meeting_dir`、`repo`、`join_url`

**`valid` 为 false 时，OpenClaw 向用户说明原因，不继续执行后续步骤。**

---

### 第二步：OpenClaw 解析 confirmed_issue.md

**此步骤 OpenClaw 作为 AI 负责全部解析，不调用任何脚本。**

从 `confirmed_issue_content` 中解析每条带勾选框的 action item，输出 JSON 数组，**只输出 JSON，不加任何说明文字或 markdown 标记**：

```json
[
  {
    "local_id": "1",
    "task": "任务描述",
    "assignee": "sujinze",
    "due_date": "2026-04-29",
    "depends_on_local_ids": [],
    "quote": "原话引用"
  },
  {
    "local_id": "2",
    "task": "另一个任务",
    "assignee": "liuzhaolin",
    "due_date": "2026-05-06",
    "depends_on_local_ids": ["1"],
    "quote": "相关原话"
  }
]
```

字段说明：
- `local_id`：本次解析的临时编号（"1" "2" ...），用于 depends_on_local_ids 引用
- `assignee`：Gitea 用户名（参考 attendees 列表）
- `due_date`：YYYY-MM-DD 格式
- `depends_on_local_ids`：依赖的其他任务 local_id 列表（无依赖则为 []）
- `quote`：原话引用（来自 confirmed_issue.md 中的 > "..." 内容）

**如果解析结果为空数组（无待办），跳过第三步，直接进入第四步（finish）。**

---

### 第三步（仅单项目会议）：调用 create-issues 批量建 Gitea issue

```bash
node main.js create-issues \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500" \
  --topic "v2 设计评审" \
  --issues-json '[{"local_id":"1","task":"...","assignee":"sujinze","due_date":"2026-04-29","depends_on_local_ids":[],"quote":"..."}]'
```

本命令会：
1. 第一轮：为每条 action item 在仓库创建 Gitea issue
   - Title：任务描述
   - Labels：`meeting-action`、`meeting:YYYY-MM-DD-HHMM`
   - Assignee：指定用户名
   - Due Date：截止日期（若 Gitea 版本支持）
   - Body：包含原话引用 + 会议目录链接
2. 第二轮：回填依赖关系（在 issue body 追加 `Depends-on: #N` 行）
3. 返回 local_id → issue_number 映射，供 finish 写入 meta.yaml

返回 JSON，关键字段：
- `success`
- `created`：`[{local_id, issue_number, issue_url, assignee, task}]`
- `failed`：`[{local_id, task, error}]`（部分失败时非空）

**跨项目会议跳过此步骤，直接进入第四步。**

---

### 第四步：调用 finish 收尾

```bash
node main.js finish \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500" \
  --topic "v2 设计评审" \
  --category "single" \
  --organizer-email "organizer@163.com" \
  --attendee-emails "email1@163.com,email2@163.com" \
  [--created-issues-json '[{"local_id":"1","issue_number":42,"issue_url":"...","assignee":"sujinze","task":"..."}]'] \
  [--failed-issues-json '[...]']
```

本命令会：
1. 将 meta.yaml status → `minutes-published`，写入 `created_issues` 字段（issue 编号列表）
2. 写日志
3. 生成并返回三种邮件参数：
   - `minutes_email`：正式纪要邮件，发给全体参会人（含 minutes.md 内容摘要 + issue 列表链接）
   - `assignee_emails`：每位 assignee 的个人任务通知邮件（数组，每人一封）
   - `cross_email`：跨项目会议时，给组织者的建议邮件（含 confirmed_issue.md 完整内容）

---

### 第五步：调用 imap-smtp-email 发送邮件

**单项目会议：**

1. 发送正式纪要邮件（`minutes_email`）：
   - 收件人：全体参会人（`minutes_email.to`）
   - 主题：`minutes_email.subject`
   - 正文：`minutes_email.html`

2. 逐一发送个人任务通知（`assignee_emails` 数组，每人一封）：
   - 收件人：单人邮箱（`assignee_emails[i].to`）
   - 主题：`assignee_emails[i].subject`
   - 正文：`assignee_emails[i].html`

**跨项目会议：**

发送组织者建议邮件（`cross_email`）：
- 收件人：`cross_email.to`（组织者邮箱）
- 主题：`cross_email.subject`
- 正文：`cross_email.html`

---

## 错误处理规则

| 错误场景 | 处理方式 |
|----------|----------|
| check 发现 status 不符 | 返回 valid=false + reason，OpenClaw 告知用户 |
| check 发现 confirmed_issue.md 不存在 | 返回 valid=false，OpenClaw 提示用户先改文件名 |
| confirmed_issue.md 解析结果为空 | 跳过 create-issues，finish 时 created_issues=[] |
| 某条 issue 创建失败 | 继续创建其他，failed 列表记录，finish 后邮件提醒组织者 |
| 依赖回填失败 | 不影响 issue 本身，日志警告 |
| finish 写 Gitea 失败 | 报错，OpenClaw 提示用户重试（可再次调用 confirm 触发） |
| 邮件发送失败 | 状态已更新为 minutes-published，日志标注 email_failed |

---

## 幂等性说明

- `check`：只读，天然幂等
- `create-issues`：若 meta.yaml 已是 minutes-published，拒绝执行（避免重复建 issue）
- `finish`：若 meta.yaml 已是 minutes-published，返回幂等成功（不重复写）
- webhook：同一次 push 若重复触发，check 的状态校验会拦截
