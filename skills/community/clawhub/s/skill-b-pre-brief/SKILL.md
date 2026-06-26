---
name: skill-b-pre-brief
description: "【会前简报定时任务】每15分钟由 OpenClaw cron 触发一次。负责在会议开始前15分钟至6小时内自动生成并发送会前进度简报。不处理会议创建、会议修改、取消会议、会后纪要等场景。触发关键词：会前简报、pre_brief、发简报、会前准备报告。cron 场景下自动触发，无需用户主动输入。"
author: mayidan
---

# Skill-B: pre_brief — 会前简报自动发送

## 定位

本技能是 **cron 定时执行的会前简报流程总控**。

职责分工：

- **OpenClaw（本次对话/cron 任务）**
  - 触发本技能 scan 脚本
  - 读取 scan 返回的会议列表
  - 对每场会议：调用 gitea-routine-report 拉取 Gitea 活动数据
  - 作为 AI 生成 ai_overview / ai_suggestion / member_summaries / risk_notes
  - 调用 gitea-routine-report 的 render_email.py 渲染 HTML
  - 调用本技能 commit 脚本保存文件并更新状态
  - 调用 imap-smtp-email 向全体参会人发送简报邮件

- **Skill-B（本技能）**
  - scan：遍历所有受管仓库，找出需要发简报的会议，计算时间窗口
  - commit：将简报存入 Gitea 会议目录，更新 meta.yaml 状态，写日志，返回邮件参数

- **gitea-routine-report**
  - 只做数据拉取 + HTML 渲染
  - 不直接触发其自带邮件发送逻辑（由 OpenClaw 决定发给谁）

- **imap-smtp-email**
  - 发送最终简报邮件给全体参会人

---

## 配置要求

配置文件：`~/.config/skill-b-pre-brief/.env`

首次使用前运行：

```bash
bash setup.sh
```

---

## 严格工作流（每次 cron 触发必须按顺序执行）

---

### 第一步：运行 scan，获取待发简报会议列表

```bash
node main.js scan
```

返回 JSON，`meetings` 字段包含所有需要处理的会议，每条有以下字段：

- `action`：`"generate_brief"` = 正常发简报；`"mark_only"` = 改期会议只改状态不发邮件
- `repo`：仓库全名，如 `HKU-AIFusion/dexterous-hand`
- `meeting_dir`：会议目录名，如 `2026-04-22-1500`
- `topic`：会议主题
- `scheduled_time`：会议时间（ISO8601）
- `organizer`：组织者 Gitea 用户名
- `attendees`：参会人 Gitea 用户名列表
- `attendee_emails`：参会人邮箱列表
- `since`：Gitea 活动统计开始时间（ISO8601）
- `until`：Gitea 活动统计结束时间（ISO8601）
- `report_params`：传给 gitea-routine-report 的参数 `{repo, since, until}`

**只有会议时间落在“开始前 15 分钟到 6 小时”这个窗口内，才会被 scan 命中。**

**如果 `meetings` 为空，本次 cron 无需继续执行。**

---

### 第二步：对 `action == "mark_only"` 的会议，直接更新状态

对每条 `action == "mark_only"` 的会议，运行：

```bash
node main.js commit \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500" \
  --mark-only
```

这会直接将 meta.yaml status 改为 `brief-sent`，不生成简报、不发邮件。

---

### 第三步：对 `action == "generate_brief"` 的会议，逐条生成并发送简报

对每条 `action == "generate_brief"` 的会议，按以下子步骤处理：

#### 3a. 调用 gitea-routine-report 拉取 Gitea 活动数据

使用 scan 返回的 `report_params`：

```bash
python <gitea-routine-report路径>/scripts/generate_report.py \
  --repo "HKU-AIFusion/dexterous-hand" \
  --since "2026-04-15" \
  --until "2026-04-22"
```

输出是 JSON 数组，取 `[0]` 元素作为本次会议仓库的数据。

> **注意**：`since` / `until` 日期格式为 `YYYY-MM-DD`，从 scan 返回的 `report_params.since` / `report_params.until` 字段取值（已格式化为此格式）。

#### 3b. OpenClaw 作为 AI 生成纯文字内容

**严格按照 gitea-routine-report 的 SKILL.md 第三步格式输出**，对上一步的数据生成：

```json
{
  "ai_overview": "...",
  "ai_suggestion": "...",
  "member_summaries": { "成员名": "一句话摘要" },
  "risk_notes": "..."
}
```

规则同 gitea-routine-report：
- 只输出 JSON，不加任何 markdown 代码块标记
- `member_summaries` 键名必须与数据中成员用户名完全一致
- 严禁编造数据中没有的内容
- `risk_notes` 无风险时填空字符串 `""`

#### 3c. 将 AI JSON 保存到临时文件

将上一步 JSON 内容存入 `/tmp/ai_brief_{meeting_dir}.json`（`meeting_dir` 中 `/` 替换为 `_`）：

```bash
echo '{"ai_overview": "...", ...}' > /tmp/ai_brief_2026-04-22-1500.json
```

#### 3d. 调用 gitea-routine-report 渲染 HTML

```bash
python -c "
import json, sys, os
sys.path.insert(0, '<gitea-routine-report路径>/scripts')
from render_email import render
data = json.loads(open('/tmp/report_data.json').read())
ai_content = json.loads(open('/tmp/ai_brief_MEETING_DIR.json').read())
repo_data = data[0]
html = render(repo_data, ai_content)
open('/tmp/brief_body_MEETING_DIR.html', 'w').write(html)
print('HTML 已生成，长度：', len(html))
"
```

> 注意：`generate_report.py` 的输出需要先保存到 `/tmp/report_data.json`，再供 render 使用。`MEETING_DIR` 替换为实际目录名（如 `2026-04-22-1500`）。

#### 3e. 调用本技能 commit，保存简报文件并更新状态

```bash
node main.js commit \
  --repo "HKU-AIFusion/dexterous-hand" \
  --meeting-dir "2026-04-22-1500" \
  --topic "v2 设计评审" \
  --html-file "/tmp/brief_body_2026-04-22-1500.html" \
  --attendee-emails "email1@163.com,email2@163.com" \
  --since "2026-04-15" \
  --until "2026-04-22"
```

返回 JSON，关键字段：
- `success`：是否成功
- `brief_email.to`：收件人邮箱列表
- `brief_email.subject`：邮件主题
- `brief_email.html`：邮件 HTML 正文

#### 3f. 调用 imap-smtp-email 发送简报邮件

使用 commit 返回的 `brief_email` 字段，调用 imap-smtp-email 发送。

收件人：`brief_email.to`（全体参会人邮箱）
主题：`brief_email.subject`
正文：`brief_email.html`（HTML 格式）

---

## 错误处理规则

| 错误场景 | 处理方式 |
|----------|----------|
| scan 无结果 | 正常退出，本次 cron 结束 |
| generate_report.py 失败 | 记录错误，跳过本条会议，继续处理下一条 |
| AI 内容生成失败 | 记录错误，跳过本条会议 |
| render_email 失败 | 记录错误，跳过本条会议 |
| commit 写 Gitea 失败 | 记录错误，不发邮件，下次 cron 重试（status 未变，仍为 scheduled） |
| 邮件发送失败 | 记录错误，但 status 已更新为 brief-sent（日志标注 email_failed） |

---

## 幂等性说明

- scan 只返回 `status == scheduled` 且不含 `rescheduled_from` 的会议
- commit 成功后 status → `brief-sent`
- 下次 cron 不会再次命中同一场会议
- commit 失败时 status 不变，下次 cron 自动重试
