---
name: yoooclaw-work-report-en
description: Automatically extract the work progress, communication points and to-dos of the day or week from work-related message notifications, and generate a daily or weekly work report. Trigger: daily report/weekly report/work report/what you did today/what you did this week/help me write my daily report/help me organize my weekly report/work briefing/work summary.
---

# Work Report

## Target

Before getting off work or before the weekend, automatically extract "what happened at work today (or this week)" from mobile phone notifications, and generate a briefing that can be sent directly to the leader or posted on the workbench.

Users don’t need to remember what they did today—notifications include everything: Feishu messages, DingTalk approvals, corporate WeChat discussions, email exchanges, calendar reminders, and project management tool notifications. This skill distills these scattered work signals into a structured brief.

User settings through the installation pop-up window:
- What (`{{what}}`): Report type - daily, weekly or both.
- Which groups and applications to follow (`{{where}}`): Work-related applications and groups, such as Feishu, DingTalk, Enterprise WeChat, Outlook, Jira, GitHub, Notion, etc. Automatically identify work apps from notifications if not set.

## Data loading strategy

- **First get the notification storage directory through `openclaw ntf storage-path`** (use the Bash tool to run this command, stdout is the absolute path of the directory). All subsequent notification files are directly in this directory and named `YYYY-MM-DD.json`.
- **File naming**: `YYYY-MM-DD.json`, one file per day, including all App notifications on that day
- **Loading priority**: ① The path specified by the user in the prompt > ② `<storage-path>/<YYYY-MM-DD>.json`
- **Time window (determined by report type)**:
  - Daily → Today only
  - Weekly report → From 00:00 this Monday to the present
  - User specifies "last N days" → last N days
  - The user specifies a specific date period → strictly as specified
- Skip non-existent files without reporting errors
- If `openclaw ntf storage-path` is not available, prompt the user to provide the data path

## Input data schema

JSON array, each item:
```json{"appName":"com.bytedance.ee.lark","title":"Group name or contact name","content":"Message content","timestamp":"2026-05-13T14:30:00.000+08:00","appDisplayName":"Feishu"}
```

## Core logic

### 1. Working signal identification

Identify work-related content from notifications. Working signal source:

| Source Type | Typical App/Signal |
|---|---|
| Office IM | Feishu, DingTalk, Enterprise WeChat, Slack, Teams |
| Email | Outlook, Gmail, NetEase mailbox (work email) |
| Project Management | Jira, Notion, Feishu Multidimensional Form, Teambition, Linear |
| Code collaboration | GitHub, GitLab (PR/Issue/CI notification) |
| Schedule meeting | Calendar reminder, Feishu calendar, meeting minutes |
| Approval process | OA approval, leave, reimbursement, printing, purchasing |
| Document collaboration | Feishu Documents, Notion, Google Docs comment notifications |

If the user specifies specific applications (such as "Feishu, GitHub") in "Which groups and applications to follow", priority will be extracted from these applications; if not specified, the above types will be automatically identified.

### 2. Noise filtering

The following content does not belong to the work output and is discarded directly:

- **Lifestyle**: takeout, express delivery, taxi hailing, shopping, payment, family group messaging
- **Marketing Push**: App operation notifications, promotions, live broadcast previews
- **Pure chat**: emoticons, "received", "+1", replies without substance
- **System Noise**: App update reminder, storage space warning, security verification code
- **Consumption/Finance**: Bank SMS, payment notification → Belongs to expense-tracker

### 3. Information classification

Group work signals into the following categories:

- **Things to be promoted**: project progress, task completion, document delivery, code merging, plan confirmation
- **Communication and Alignment**: meeting discussion points, cross-team collaboration, requirements alignment, feedback collection
- **Approval and Process**: Initiated/completed approval, signature, reimbursement, and process node advancement
- **To-do and follow-up**: Assigned tasks, @required to reply, things promised but not yet done, things that need to be continued tomorrow
- **Risks and Blockages**: postponement, rejection, unresponsiveness of relying parties, insufficient resources, scheduling conflicts

### 4. Merge and refine

- Multiple messages on the same matter are merged into one, and the final conclusion/latest status shall prevail.- Summarize the core progress of each matter in one sentence, do not copy the original text
- Keep key entities: project name, document name, meeting name, person name, deadline
- Sort by timeline to give the briefing a "rhythm of the day"

## Output requirements

The output is session text, no file is generated.

### A. Daily mode

```
📋Work Daily (YYYY-MM-DD)

One-sentence overview: Use 1 sentence to summarize today’s work focus and main outputs.

━━ Today’s progress ━━

  1. <Item name>: <Summary of progress in one sentence>
     Involving: <project/document/meeting name>
  2. <Item name>: <Summary of progress in one sentence>
     Involving: <project/document/meeting name>
  ...

━━ Communication and Alignment ━━

  1. <Meeting/Discussion Topic>: <Conclusion or Points>
     Participants: <name/team>
  ...

━━ Approval and process ━━ (if any)

  1. <Approval items>: <Status (passed/pending approval/rejected)>
  ...

━━ To-do list for tomorrow ━━

  □ <To-do items> (Deadline: <if any>)
  □ <To-do items>
  ...

━━Risks and Blockages ━━(if any)

  ⚠️ <Risk Description>
  ...
```

### B. Weekly report mode

```
📋 Weekly work report (MM/DD ~ MM/DD)

One Sentence Overview: Use 1 sentence to summarize the core outputs and key developments of the week.

━━ Completed this week ━━

  1. <Item name>: <Achievements summary>
  2. <Item name>: <Achievements summary>
  ...

━━ In progress ━━

  1. <Item name>: <Current status and progress>
  2. <Item name>: <Current status and progress>
  ...

━━ Critical communication ━━ (if any)

  1. <Meeting/Discussion>: <Conclusion>
  ...

━━ Plan for next week ━━

  □ <Plan items>
  □ <Plan items>
  ...

━━Risks and Blockages ━━(if any)

  ⚠️ <Risk Description>
  ...
```

### C. Cover-up mode

If no work-related notifications are recognized that day (or this week), output:

```
📋Work Daily (YYYY-MM-DD)

There are no work updates recorded today.
```

### D. Simplified mode

If the number of job notifications is very small (less than 3 valid signals), downgrade to the simplified version:

```
📋Work Daily (YYYY-MM-DD)

Less work updates today:

  1. <Matter>: <Summary>
  2. <Matter>: <Summary>

To-do list tomorrow:
  □ <If there are to-dos identified from the notification>
```## Decision Criteria

- Don’t keep a running account, give priority to matters with substantial output and advancement
- The meeting only records the conclusions and decisions, not the process
- "Received", "OK", "+1", etc. do not constitute work output and are discarded.
- Those who have been @ but have not yet replied will be classified into "Tomorrow's to-do"
- If the approval is rejected, it will be classified into "Risk and Obstruction"
- Do not make up content that is not in the notice; when there is insufficient information, prefer to output a simplified version or covert copy
- Daily reports should be limited to 800 words, and weekly reports should be limited to 1,500 words.
- The tone is professional and concise, and the produced briefing can be sent directly to the leader or posted on the workbench

## Output style

- High information density, suitable for scanning in 1 minute before leaving get off work.
- Summarize the matter in one sentence without going into the background.
- Key entities (project name, person name, deadline) retain the original text and are not blurred.
- Only session text is generated, no file is written.
