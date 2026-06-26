# Session Setup and Operations

Use this reference for the **published V1 default model**.
The goal is not to bootstrap two permanent UI-visible worker sessions.
The goal is to let the main session reliably orchestrate:
- one `xiaoma` execution agent
- one `xiaoniu` QA agent
- a clean execute -> review loop
- without blocking the user chat by default

## Table of contents
- 1. Default backend choice
- 2. V1 workflow
- 3. Recommended command pattern
- 4. Role packets
- 5. Smoke test
- 6. Failure handling
- 7. Advanced/persistent note

## 1. Default backend choice

Default to **real-agent CLI routing** for published V1.
Use:
- `openclaw agent --agent xiaoma --message ...`
- `openclaw agent --agent xiaoniu --message ...`

Why:
- this path is locally validated end-to-end
- it uses real local agents instead of role-only dispatch
- it avoids the incorrect assumption that `sessions_send` is the default route
- it keeps the workflow reproducible for first-time operators
- it does not require visible dedicated worker chat cards

Practical default:
- one Xiaoma task, then one Xiaoniu QA task
- keep task packets narrow and explicit
- return the main session to the user immediately instead of blocking while workers run

Optional note:
- if you need to reuse existing worker context, add `--session-id <existing-session-id>`
- this is an advanced refinement, not the published default teaching path

## 2. V1 workflow

### 2.1 Main session receives task
The main session owns:
- task decomposition
- dispatch decision
- risk control
- user-facing summary

### 2.2 Run 小马
Dispatch one Xiaoma execution turn for the current task.
Do not require a persistent visible worker chat card.
Do not block the main session unless debugging or smoke testing requires it.

### 2.3 Get 小马 result
Expect structured execution output:
- 已完成
- 未完成
- 风险/阻塞
- 建议下一步

### 2.4 Run 小牛 if QA is needed
Dispatch one Xiaoniu QA turn with a compact acceptance packet.
Do not dump giant transcripts.
Send only:
- original goal
- acceptance criteria
- concise Xiaoma result summary
- key files/risks to inspect

### 2.5 Summarize back in main session
Main session reports:
- what 小马 finished
- whether 小牛 passed
- if failed, only the concrete issues

## 3. Recommended command pattern

Use the published local pattern for both roles:

```powershell
openclaw agent --agent xiaoma --message "<task packet>"
openclaw agent --agent xiaoniu --message "<qa packet>"
```

If existing worker context is valuable, extend the command with:

```powershell
openclaw agent --agent xiaoma --session-id <existing-session-id> --message "<task packet>"
```

Do not teach session-id-only routing as the default published path.

## 4. Role packets

### 4.1 小马 packet
Use a task packet like:

```text
你是小马（执行位）。请按以下要求执行。

目标：<一句话目标>
范围：<允许改动的文件/模块/边界>
约束：<禁止项、兼容性、风格要求>
验收标准：<如何算完成>
补充要求：<是否跑测试 / 是否更新文档 / 是否给补丁>

输出格式固定为：
1. 已完成
2. 未完成
3. 风险/阻塞
4. 建议下一步
```

### 4.2 小牛 packet
Use a QA packet like:

```text
你是小牛（验收位）。请只做验收，不重做主体工作。

任务目标：<一句话>
验收标准：<完成定义>
小马产出摘要：<简要总结>
重点检查：<文件、行为、测试、风险点>

输出规则：
- 通过：只回复“验收没问题”
- 不通过：只列具体问题或未完成项
```

## 5. Smoke test

After editing or installing the skill, do not claim V1 works unless this minimal loop passes:

### Step 1 — xiaoma ping
Run Xiaoma with a tiny ping or tiny read-only task.

Pass conditions:
- command returns successfully
- Xiaoma stays in execution role
- response is concrete

### Step 2 — xiaoniu ping
Run Xiaoniu with a tiny ping or compact QA packet.

Pass conditions:
- command returns successfully
- Xiaoniu stays in QA role
- response is `验收没问题` or a short concrete issue list

### Step 3 — real loop
Run one tiny real execute -> review task.

If all three steps pass, the published V1 route is operational enough for real tasks.

## 6. Failure handling

### If Xiaoma command fails
1. retry once with a smaller cleaner packet
2. if still failing, classify it as backend/dispatch failure, not task failure
3. if urgent, do the work in main session as temporary degradation

### If Xiaoniu command fails
1. retry once
2. if still failing, do manual acceptance in main session
3. do not block the whole workflow forever on QA worker availability

### If the runtime layer is flaky
Prefer:
- smaller tasks
- one worker at a time
- published CLI agent routing over historical wrapper assumptions
- asynchronous user-facing orchestration

## 7. Advanced/persistent note

Persistent Xiaoma / Xiaoniu may still be explored later, but they are **not required** for published V1 success.
Do not make V1 depend on:
- visible dedicated WebChat worker sessions
- persistent session bootstrap
- thread-bound worker cards
- long-lived worker recovery logic
- `sessions_spawn(runtime="subagent")` as the default local route

Those belong to a later enhancement path, not the published V1 operating path.
