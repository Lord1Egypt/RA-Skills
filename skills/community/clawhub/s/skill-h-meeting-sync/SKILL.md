---
name: skill-h-meeting-sync
description: "【会议状态同步后台守护任务】每25分钟由 OpenClaw cron 触发一次。负责同步腾讯会议与各 Gitea 仓库之间的会议状态一致性，处理会议取消、改期、新增三种场景，并定期归档过期会议目录。不处理会议创建（用 skill-a）、会前简报（用 skill-b）、会后纪要（用 skill-c）等场景。"
author: mayidan
---

# Skill-H: meeting_sync — 会议状态同步后台守护

## 定位

本技能是 **cron 每 25 分钟触发的后台守护任务**。

职责分工：

- **OpenClaw（本次对话/cron 任务）**
  - 触发 scan，获取 Gitea 侧全部活跃会议
  - 调用 tencent-meeting-skill 获取腾讯会议侧未来 7 天会议列表
  - 做三向对比分析，判断每场会议属于哪种情况（取消 / 改期 / 新增 / 已结束或已过期 / 无变化）
  - 根据分析结果，调用对应的 Skill-H 命令执行 Gitea 侧操作
  - 调用 imap-smtp-email 发送通知邮件
  - 在每次 cron 最后调用 archive 做归档清理

- **Skill-H（本技能）**
  - `scan`：汇总所有 Gitea 活跃会议（status ∈ {scheduled, brief-sent}），返回供对比的数据
  - `cancel`：将“尚未开始但腾讯会议中已不存在”的会议标记为已取消，写日志，返回取消通知邮件参数
  - `reschedule`：更新旧目录状态为 rescheduled，创建新时间目录，写日志，返回改期通知邮件参数
  - `create-pending`：在 aifusion-meta 创建 repo:pending 的会议占位记录
  - `archive`：将 cancelled/rescheduled 状态超过 30 天的目录移入 meetings/archive/

- **tencent-meeting-skill**
  - 查询腾讯会议侧未来 7 天会议列表（`get_user_meetings`）
  - 查询当天已结束会议（`get_user_ended_meetings`），用于辅助排除“其实已经开完”的情况

- **imap-smtp-email**
  - 发送取消通知、改期通知、新会议待确认通知邮件

---

## 配置要求

配置文件：`~/.config/skill-h-meeting-sync/.env`

首次使用前运行：

```bash
bash setup.sh
```

---

## 严格工作流（每次 cron 触发必须按顺序执行）

---

### 第一步：scan，获取 Gitea 侧所有活跃会议

```bash
node main.js scan
```

返回 JSON，`gitea_meetings` 字段包含所有 status ∈ {scheduled, brief-sent} 的会议，每条包含：

- `repo`：仓库全名
- `meeting_dir`：会议目录名
- `meeting_id`：腾讯会议内部 ID（用于对比）
- `meeting_code`：9 位会议号
- `topic`：会议主题
- `scheduled_time`：会议时间（ISO8601）
- `status`：当前状态
- `organizer`：组织者用户名
- `attendees`：参会人用户名列表
- `attendee_emails`：参会人邮箱列表
- `category`：single | cross-project

---

### 第二步：OpenClaw 调用 tencent-meeting-skill 获取腾讯会议列表

调用 `get_user_meetings` 获取即将开始及进行中的会议，同时调用 `get_user_ended_meetings` 补充当天已结束会议。

将结果整理为两个字典：

1. **future_meetings_by_id**
   - key：`meeting_id`
   - value：会议信息（含 `scheduled_time`）

2. **ended_meetings_by_id**
   - key：`meeting_id`
   - value：会议信息（含 `scheduled_time` 或结束标记）

> 判断"未来 7 天内"：只保留 scheduled_time 在 now ~ now+7d 范围内的腾讯会议记录用于“未来会议”对比。  
> `get_user_ended_meetings` 只用于排除“会议其实已经结束”的误判，不用于触发 cancel。

---

### 第三步：OpenClaw 做三向对比分析

以 `meeting_id` 作为唯一标识，对 Gitea 列表、腾讯未来会议列表、腾讯已结束会议列表进行对比，产生以下五种情况：

| 情况 | 判断条件 | 处理方式 |
|------|----------|----------|
| **无变化** | Gitea 有，腾讯未来会议也有，且时间差 < 1 分钟 | 跳过 |
| **已改期** | Gitea 有，腾讯未来会议也有，但时间差 ≥ 1 分钟 | → reschedule |
| **已结束或已过期** | Gitea 有，腾讯未来会议无，且（腾讯已结束列表中有该 meeting_id，或 Gitea `scheduled_time <= now`） | **跳过，不调用 cancel** |
| **已取消** | Gitea 有，腾讯未来会议无，腾讯已结束列表也无，且 Gitea `scheduled_time > now` | → cancel |
| **新增** | 腾讯未来会议有，Gitea 无对应 meeting_id | → create-pending |

> **关键修正：**
> - “腾讯会议中没有这场会” **不等于** “已取消”
> - 它也可能表示：会议已正常结束，或者会议时间已经过去
> - 因此只有“**尚未开始 + 腾讯未来列表中不存在 + 腾讯已结束列表中也不存在**”时，才允许判定为取消

> **时间对比说明：**
> - 腾讯会议返回的是秒级时间戳，需先转为北京时间再与 Gitea 的 `scheduled_time` 对比
> - 时间差 **小于 1 分钟** 视为无变化（仅用于避免秒级精度误差）
> - 时间差 **大于等于 1 分钟** 视为改期，应触发 `reschedule`

---

### 第四步：对"已取消"的会议，调用 cancel

```bash
node main.js cancel \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500" \
  --attendee-emails "email1@163.com,email2@163.com" \
  [--cancel-reason "腾讯会议中已不存在，且会议时间尚未到达"]
```

返回 JSON，可能有两种结果：

#### 结果 A：真正取消成功
- `success: true`
- `new_status: "cancelled"`
- `cancel_email.to` / `.subject` / `.html`

此时 OpenClaw 调用 imap-smtp-email 发送取消通知给全体参会人。

#### 结果 B：被 Skill-H 安全拦截
- `success: true`
- `skipped: true`
- `skip_reason: "meeting_time_passed"`

表示：
- 会议时间已过
- Skill-H 判断它可能是“已经正常开完”或“已过期未清理”
- **不会写 cancelled**
- **不会返回取消邮件参数**
- OpenClaw 应记录日志后直接跳过

---

### 第五步：对"已改期"的会议，调用 reschedule

```bash
node main.js reschedule \
  --repo "HKU-AIFusion/dexterous-hand" \
  --old-meeting-dir "2026-04-22-1500" \
  --new-time "2026-04-23T15:00:00+08:00" \
  --new-meeting-id "yyy" \
  --new-meeting-code "987654321" \
  --new-join-url "https://meeting.tencent.com/..." \
  --attendee-emails "email1@163.com,email2@163.com"
```

本命令会：
1. 将旧目录 `meta.yaml` status → `rescheduled`，写入 `rescheduled_to` 字段
2. 在同仓库创建新目录 `meetings/YYYY-MM-DD-HHMM/`，继承旧会议的 topic / attendees / organizer / category，写入 `rescheduled_from` 字段，status = `scheduled`
3. 在新目录创建 `agenda.md`（注明"本次会议由 YYYY-MM-DD-HHMM 改期而来"）

返回 JSON，关键字段：
- `success`
- `new_meeting_dir`：新目录名
- `reschedule_email.to` / `.subject` / `.html`：改期通知邮件参数

**收到返回后，OpenClaw 调用 imap-smtp-email 发送改期通知给全体参会人。**

---

### 第六步：对"新增"的会议（腾讯有，Gitea 无），调用 create-pending

```bash
node main.js create-pending \
  --meeting-id "zzz" \
  --meeting-code "111222333" \
  --topic "未知主题" \
  --time "2026-04-24T10:00:00+08:00" \
  --join-url "https://meeting.tencent.com/..." \
  [--duration 60]
```

本命令会：
1. 在 `aifusion-meta/meetings/YYYY-MM-DD-HHMM/` 创建占位目录
2. 写入 `meta.yaml`（status=scheduled，repo=pending）

返回 JSON，关键字段：
- `success`
- `meeting_dir`：创建的目录名
- `notify_email.to` / `.subject` / `.html`：发给组织者（ADVISOR）的待确认通知邮件参数

**收到返回后，OpenClaw 调用 imap-smtp-email 向组织者发送待确认通知。**

> 通知内容应说明："腾讯会议中发现一场新会议，尚未关联到 Gitea 仓库，请在 aifusion-meta 中修改 repo 字段或在 OpenClaw 中说明归属仓库。"

---

### 第七步：archive 归档清理（每次 cron 最后执行）

```bash
node main.js archive
```

本命令会：
1. 遍历所有受管仓库（包括 aifusion-meta）
2. 找出 status ∈ {cancelled, rescheduled} 且 scheduled_time 距今超过 30 天的会议目录
3. 将这些目录下所有文件复制到同仓库的 `meetings/archive/YYYY-MM-DD-HHMM/`
4. 删除原目录下所有文件（Gitea API 逐文件删除）
5. 写日志，返回归档摘要

---

## 错误处理规则

| 错误场景 | 处理方式 |
|----------|----------|
| scan 失败 | 打印错误，本次 cron 中止 |
| tencent-meeting-skill 调用失败 | 跳过本次同步，不修改任何 Gitea 状态 |
| cancel / reschedule 写 Gitea 失败 | 记录错误，下次 cron 重试 |
| create-pending 失败 | 记录错误，下次 cron 检测到同一会议时重试 |
| 邮件发送失败 | 记录错误，不影响 Gitea 状态更新 |
| archive 单个文件迁移失败 | 跳过该文件，继续处理其他文件，日志记录警告 |

---

## 幂等性说明

- scan 只返回 status ∈ {scheduled, brief-sent} 的会议
- cancel 成功后 status → cancelled，下次 cron 不再扫描到
- 若会议时间已过，cancel 会返回 `skipped=true`，不会误写为 cancelled
- reschedule 成功后旧目录 status → rescheduled，新目录 status=scheduled；下次 cron 只处理新目录
- create-pending 用 meeting_id 作为 meta.yaml 的唯一标识；下次 cron 的 scan 会包含它（repo=pending 的目录也被 scan 返回以便追踪）；待组织者确认归属后人工处理
- archive 只处理超过 30 天的目录，不会误归档活跃会议
