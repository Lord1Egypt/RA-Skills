---
name: skill-c-fetch-minutes
description: "【会后纪要抓取与issue草稿生成】每10分钟由 OpenClaw cron 触发一次。负责在会议结束后从腾讯会议拉取转录与AI智能纪要，由 OpenClaw 做两阶段issue抽取，生成 draft_issue.md 等四个文件并提交到 Gitea，最后通知组织者审核。不处理会议创建、会前简报、issue落地等场景。"
author: mayidan
---

# Skill-C: fetch_minutes — 会后纪要抓取与 issue 草稿生成

## 定位

本技能是 **cron 每 10 分钟触发的会后处理流程总控**。

职责分工：

- **OpenClaw（本次对话/cron 任务）**
  - 触发 scan，获取三类待处理会议
  - 对 A 类会议，只在 `ready_for_postprocess == true` 时才调用 `set-waiting`
  - 调用 tencent-meeting-skill 拉取转录与 AI 智能纪要（三层降级）
  - 对 C 类会议，从 Gitea 读取已有 transcript.md 内容
  - **作为 AI 完成两阶段 issue 抽取**，生成四个文件的完整内容
  - 调用本技能各命令执行 Gitea 侧状态更新与文件提交
  - 调用 imap-smtp-email 向组织者发送审核通知邮件

- **Skill-C（本技能）**
  - `scan`：扫描所有仓库，按 A / B / C 三类分组返回待处理会议
  - `set-waiting`：将 scheduled / brief-sent → waiting-transcript，但必须满足“会议结束超过 20 分钟”
  - `set-failed`：将 waiting-transcript → transcript-failed，返回通知邮件参数
  - `commit-content`：将四个文件写入 Gitea 会议目录，status → draft-pending-review，写日志，返回审核通知邮件参数

- **tencent-meeting-skill**
  - 拉取录制列表（`get_records_list`）获取 `record_file_id`
  - Layer 1：`get_smart_summary` + `get_transcripts_details`
  - Layer 2：`get_transcripts_details` 单独拉取
  - Layer 3：均失败则跳过，下次 cron 重试

- **imap-smtp-email**
  - 发送 transcript-failed 通知给组织者（附手动上传说明）
  - 发送 draft-pending-review 通知给组织者（附两种确认方式说明）

---

## 配置要求

配置文件：`~/.config/skill-c-fetch-minutes/.env`

首次使用前运行：

```bash
bash setup.sh
```

---

## 严格工作流（每次 cron 触发必须按顺序执行）

---

### 第一步：scan，获取三类待处理会议

```bash
node main.js scan
```

返回 JSON，包含三个字段：

- `class_a`：`status ∈ {scheduled, brief-sent}` 且**已结束超过 20 分钟**的会议
- `class_b`：`status == waiting-transcript` 的会议（需拉取转录内容，或判断超时）
- `class_c`：`status == transcript-failed` 且 `transcript.md` 已存在的会议（组织者已手动上传）

每条记录包含：
- `repo`
- `meeting_dir`
- `topic`
- `organizer`
- `organizer_email`
- `scheduled_time`
- `duration_minutes`
- `meeting_id`
- `meeting_code`
- `attendees`
- `attendee_emails`
- `category`
- `status`

其中：

- A 类额外包含：
  - `meeting_end_time`
  - `ready_after_time`
  - `ready_for_postprocess`
  - `postprocess_grace_minutes`

- B 类额外包含：
  - `transcript_started_at`
  - `transcript_poll_count`

- C 类额外包含：
  - `transcript_content`

**关键兼容逻辑：**

即使某场会议因为时间太近而没来得及发送会前简报，只要它仍处于 `scheduled` 状态，Skill-C 也会在会后将其纳入 A 类继续处理，避免整个会后流程中断。  
但为了避免误判，**只有会议结束后再额外等待 20 分钟**，才允许进入会后流程。

**如果三类均为空，本次 cron 无需继续。**

---

### 第二步：处理 A 类会议（status ∈ {scheduled, brief-sent}）

对每条 A 类会议：

#### 2a. 判断会议是否已达到会后处理条件

根据 `scheduled_time` 和 `duration_minutes` 计算：

```text
meeting_end_time = scheduled_time + duration_minutes
ready_after_time = meeting_end_time + 20 分钟
ready_for_postprocess = 当前时间 > ready_after_time
```

只有当 `ready_for_postprocess == true` 时，才允许进入会后流程。

**未达到条件 → 跳过，等待下次 cron。**

**达到条件 → 调用 set-waiting：**

```bash
node main.js set-waiting   --repo "HKU-AIFusion/dexterous-hand"   --meeting-dir "2026-04-22-1500"
```

返回成功后，将该会议加入本次 cron 的 B 类处理队列（立即继续处理，无需等待下次 cron）。

> 注意：
> - `set-waiting` 同时接受 `scheduled` 和 `brief-sent` 两种旧状态
> - 但即使 OpenClaw 误调用，本脚本也会二次校验“结束后 20 分钟缓冲”是否满足
> - 未满足时会返回 `skipped=true`，不会推进状态

---

### 第三步：处理 B 类会议（status == waiting-transcript）

**注意：本步骤同时处理原 B 类和第二步刚转入的会议。**

对每条会议：

#### 3a. 判断是否超时

从 scan（或 set-waiting 返回）取 `transcript_started_at`，计算已等待时长：

```text
已等待 = 当前时间 - transcript_started_at
超时 = 已等待 > 60 分钟
```

**超时 → 调用 set-failed，然后调用 imap-smtp-email 发送手动上传通知：**

```bash
node main.js set-failed   --repo "HKU-AIFusion/dexterous-hand"   --meeting-dir "2026-04-22-1500"   --organizer-email "organizer@163.com"
```

返回 `fail_email.to / .subject / .html`，OpenClaw 调用 imap-smtp-email 发送。**跳过后续步骤。**

#### 3b. 三层降级拉取转录内容

**先调用 tencent-meeting-skill 获取 `record_file_id`：**

```text
调用 get_records_list，传入 meeting_id
→ 从返回结果中取第一条录制的 record_file_id
```

若 `get_records_list` 失败或返回空，整条跳过（Layer 3，等下次 cron）。

**Layer 1：AI 智能纪要 + 转录全文**

```text
调用 get_smart_summary，传入 record_file_id → 得到 ai_summary 文本
调用 get_transcripts_details，传入 record_file_id → 得到 transcript 文本
```

两者都成功 → `source = "ai_summary"`，继续第四步。

**Layer 2：仅转录全文**

Layer 1 失败 → 只调用 `get_transcripts_details`：

```text
调用 get_transcripts_details，传入 record_file_id → 得到 transcript 文本
```

成功 → `source = "transcript_only"`，`ai_summary` 置空，继续第四步。

**Layer 3：均失败**

Layer 2 也失败 → 整条跳过，等下次 cron（不修改 Gitea 状态，下次仍为 `waiting-transcript`）。

---

### 第四步：处理 C 类会议（transcript-failed，transcript.md 已存在）

对每条 C 类会议：

从 Gitea 会议目录读取 `transcript.md` 内容（scan 已确认文件存在）：

```text
source = "manual_upload"
transcript = transcript.md 内容
ai_summary = 空（无 AI 智能纪要）
```

直接进入第五步，OpenClaw 做 AI 抽取。

---

### 第五步：OpenClaw 完成两阶段 AI 抽取

**此步骤 OpenClaw 作为 AI 负责全部生成，不调用任何 skill 脚本。**

输入：
- `transcript`
- `ai_summary`（可能为空）
- `source`
- 会议基本信息（`topic / meeting_dir / attendees / scheduled_time`）

#### 阶段一：结构化抽取

基于 ai_summary（优先）和 transcript，严格按以下 JSON 格式输出，**只输出 JSON，不加任何说明文字或 markdown 标记**：

```json
{
  "decisions": [
    { "content": "决策内容", "owner": "负责人（Gitea 用户名或姓名）" }
  ],
  "action_items": [
    {
      "task": "任务描述",
      "assignee_hint": "提到的人名或用户名",
      "due_date_hint": "截止时间表述，如'下周五'",
      "depends_on_hint": "依赖描述，如'等 sujinze 出图后'",
      "quote": "转录中最相关的原话片段"
    }
  ],
  "open_questions": [
    { "content": "待讨论问题" }
  ],
  "notes": "其他补充说明"
}
```

**严格约束：严禁编造转录中没有的内容。任务描述含糊时宁可跳过，不写。**

#### 阶段二：映射与回填

基于阶段一结果：

- `assignee_hint` → 映射为 Gitea 用户名（参考 attendees 列表）
- `due_date_hint` → 转换为 `YYYY-MM-DD` 格式（基于会议日期推算）
- `quote` → 在 transcript 中搜索最相近的原话，若找不到则置空
- `depends_on_hint` → 只有原文出现明确依赖表述时才保留，否则置空

---

### 第六步：生成四个文件内容

OpenClaw 根据两阶段抽取结果，生成以下四个文件的完整文本内容，**分别写入临时文件**：

#### transcript.md
#### ai_summary.md（仅 source=ai_summary 时生成）
#### minutes.md
#### draft_issue.md

文件格式与原工作流保持一致。

---

### 第七步：调用 commit-content 提交文件并更新状态

```bash
node main.js commit-content   --repo "HKU-AIFusion/dexterous-hand"   --meeting-dir "2026-04-22-1500"   --topic "v2 设计评审"   --organizer-email "organizer@163.com"   --transcript-file "/tmp/transcript_2026-04-22-1500.md"   --minutes-file "/tmp/minutes_2026-04-22-1500.md"   --draft-issue-file "/tmp/draft_issue_2026-04-22-1500.md"   [--ai-summary-file "/tmp/ai_summary_2026-04-22-1500.md"]   [--source "ai_summary"]
```

返回 JSON，关键字段：
- `success`
- `review_email.to / .subject / .html`
- `gitea_dir_url`

---

### 第八步：调用 imap-smtp-email 发送审核通知

使用 `review_email` 字段：

- 收件人：组织者
- 主题：审核通知
- 正文：HTML

---

## 错误处理规则

| 错误场景 | 处理方式 |
|----------|----------|
| scan 失败 | 打印错误，本次 cron 中止 |
| 会议尚未结束超过 20 分钟 | 跳过，等待下次 cron |
| OpenClaw 误调用 set-waiting | set-waiting 返回 skipped=true，不推进状态 |
| get_records_list 失败 | Layer 3，整条跳过 |
| Layer 1 失败，Layer 2 成功 | 继续，source=transcript_only |
| Layer 1/2 均失败 | Layer 3，整条跳过，状态保持 waiting-transcript |
| AI 抽取失败 | 跳过本条，记录错误，下次 cron B 类重试 |
| commit-content 写 Gitea 失败 | 不发邮件，下次 cron 重试（状态未变） |
| 邮件发送失败 | 记录错误，但 status 已更新 |
| 超时 60 分钟 | set-failed，发手动上传说明邮件 |

---

## 幂等性说明

- scan 只把“已结束超过 20 分钟”的 `scheduled / brief-sent` 会议放入 A 类
- set-waiting 接受 `scheduled` 和 `brief-sent` 两种旧状态，重复调用安全
- set-waiting 对未满足“结束后 20 分钟”的会议会返回 `skipped=true`
- set-failed 仍只处理 `waiting-transcript`
- commit-content 成功后 status → `draft-pending-review`，下次 cron 不再扫描到
- commit-content 对已存在的文件执行 update（而非 create），避免重复提交报错
