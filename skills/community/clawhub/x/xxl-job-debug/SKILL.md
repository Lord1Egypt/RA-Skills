---
name: xxl-job-debug
description: "Use when triggering or debugging XXL-JOB tasks."
version: 4.0.0
author: custom
license: MIT
metadata:
  hermes:
    tags: [xxl-job, scheduler, debug, java, intellij]
    related_skills: [rigorous-code-analysis]
---

# XXL-JOB Debug

## When to Use

Use when the user asks to create, update, start, stop, trigger, inspect logs of, kill, or delete an XXL-JOB task; when a task needs to run on a specific executor node (especially the local IntelliJ/JVM); or when debugging why an XXL-JOB job did not run as expected.

## Purpose

Execute and debug XXL-JOB tasks through the scheduling-center/executor APIs.

Core flow:

```text id="a1"
Request
  ↓
Resolve Task / Executor / Token
  ↓
Perform Operation
  ↓
Verify Result
  ↓
Collect Logs
```

Use `rigorous-code-analysis` for source-code analysis, modification, testing, and root-cause investigation.

---

# 1. Operation Model

Parse natural language into:

```yaml id="b1"
action: create | update | start | stop | trigger | log | kill | delete
jobId:
appName:
handler:
executorParam:
targetExecutor:
taskConfig:
```

Examples:

```text
“执行 123”
→ trigger

“任务 123 在我本地执行”
→ trigger + targetExecutor=local

“新增一个每分钟执行的任务到 xxx 执行器”
→ create

“把 123 的 cron 改成每天 2 点”
→ update

“停止 123”
→ stop

“删除刚才创建的任务”
→ delete
```

Do not invent `jobId`, `AppName`, `JobHandler`, executor address, or token.

---

# 2. Resolve XXL-JOB Connection

Determine:

```text id="c1"
Admin URL
AccessToken
AppName
```

Typical executor configuration:

```properties id="c2"
xxl.job.admin.addresses=
xxl.job.executor.appname=
xxl.job.executor.accessToken=
xxl.job.executor.address=
xxl.job.executor.ip=
xxl.job.executor.port=
```

Older deployments may use different Token property layouts. Inspect the actual project configuration and XXL-JOB version instead of assuming a fixed property name.

AccessToken must match the credentials expected by the target XXL-JOB API. Current XXL-JOB development has also changed token configuration toward executor-level isolation, so prefer the running project's actual configuration over old documentation examples.

Never print the full token.

---

# 3. Resolve Executor

For a target `AppName`, obtain registered executor nodes.

Prefer:

```text id="d1"
XXL-JOB Executor Management
↓
registered executor addresses
```

Then verify against:

```text id="d2"
xxl_job_registry
xxl.job.executor.address
xxl.job.executor.ip
xxl.job.executor.port
```

The registry uses the executor AppName and executor address to represent registered nodes.

When the user says:

```text
“本地”
“我的 IDEA”
“当前这个 JVM”
```

select the executor corresponding to the local JVM, not an arbitrary node.

---

# 4. Verify Executor

Before executor-specific operations:

```http id="e1"
POST {EXECUTOR_URL}/beat
```

Headers:

```text id="e2"
XXL-JOB-ACCESS-TOKEN: {TOKEN}
XXL-JOB-APPNAME: {APPNAME}
```

Require a successful response before continuing.

The executor API defines `/beat` as the heartbeat endpoint.

---

# 5. Create Task

Use:

```http id="f1"
POST {ADMIN_URL}/api/addJob
```

Headers:

```text id="f2"
XXL-JOB-ACCESS-TOKEN: {TOKEN}
XXL-JOB-APPNAME: {APPNAME}
Content-Type: application/json
```

Request:

```json id="f3"
{
  "jobGroup": 1,
  "name": "测试任务",
  "author": "admin",
  "alarmEmail": "",
  "scheduleType": "CRON",
  "scheduleConf": "0 0/1 * * * ?",
  "misfireStrategy": "DO_NOTHING",
  "executorRouteStrategy": "FIRST",
  "executorHandler": "demoJobHandler",
  "executorParam": "",
  "executorBlockStrategy": "SERIAL_EXECUTION",
  "executorTimeout": 0,
  "executorFailRetryCount": 0,
  "glueType": "BEAN",
  "glueSource": "",
  "glueRemark": ""
}
```

Required task fields:

```text id="f4"
jobGroup
name
author
scheduleType
scheduleConf
executorRouteStrategy
executorHandler (BEAN)
executorBlockStrategy
glueType
```

Important configurable values:

### scheduleType

```text id="f5"
NONE
CRON
FIX_RATE
```

### misfireStrategy

```text id="f6"
DO_NOTHING
FIRE_ONCE_NOW
```

### executorRouteStrategy

```text id="f7"
FIRST
LAST
ROUND
RANDOM
CONSISTENT_HASH
LEAST_FREQUENTLY_USED
LEAST_RECENTLY_USED
FAILOVER
BUSYOVER
SHARDING_BROADCAST
```

### executorBlockStrategy

```text id="f8"
SERIAL_EXECUTION
DISCARD_LATER
COVER_EARLY
```

### glueType

```text id="f9"
BEAN
GLUE_GROOVY
GLUE_SHELL
GLUE_PYTHON
GLUE_NODEJS
GLUE_POWERSHELL
GLUE_PHP
```

The task fields and route/block/glue options are defined in the uploaded XXL-JOB documentation.

When creating a debugging task, prefer:

```text
simple Cron
BEAN mode
known JobHandler
safe executorParam
```

Do not create a persistent production-like schedule unless requested.

Capture the returned `jobId`.

---

# 6. Update Task

Use:

```http id="g1"
POST {ADMIN_URL}/api/updateJob
```

Request:

```json id="g2"
{
  "id": 123,
  "name": "测试任务",
  "author": "admin",
  "alarmEmail": "",
  "scheduleType": "CRON",
  "scheduleConf": "0 0/5 * * * ?",
  "misfireStrategy": "DO_NOTHING",
  "executorRouteStrategy": "FIRST",
  "executorHandler": "demoJobHandler",
  "executorParam": "test",
  "executorBlockStrategy": "SERIAL_EXECUTION",
  "executorTimeout": 0,
  "executorFailRetryCount": 0,
  "glueType": "BEAN",
  "glueSource": "",
  "glueRemark": ""
}
```

The update operation requires the existing `jobId`.

When updating, change only fields required by the request.

---

# 7. Start / Stop Task

Start:

```http id="h1"
POST {ADMIN_URL}/api/startJob
```

```json id="h2"
{
  "id": 123
}
```

Stop:

```http id="h3"
POST {ADMIN_URL}/api/stopJob
```

```json id="h4"
{
  "id": 123
}
```

## `startJob` enables subsequent scheduling; `stopJob` disables subsequent scheduling. Neither should be treated as terminating an already-running execution.

# 8. Trigger One Execution

Use:

```http id="i1"
POST {ADMIN_URL}/api/triggerJob
```

Request:

```json id="i2"
{
  "id": 123,
  "executorParam": "debug",
  "addressList": "http://127.0.0.1:9999/"
}
```

### Default

When executor selection does not matter:

```json id="i3"
{
  "id": 123,
  "executorParam": "debug",
  "addressList": ""
}
```

The scheduler resolves registered executors.

### Local debugging

When the user requests a specific node:

```json id="i4"
{
  "id": 123,
  "executorParam": "debug",
  "addressList": "http://127.0.0.1:9999/"
}
```

`addressList` is the preferred mechanism for one-shot targeting and does not require changing the task's persistent routing strategy.

---

# 9. Local IntelliJ Debug Flow

For:

```text id="j1"
“在我本地 IDEA 执行任务 123”
```

perform:

```text id="j2"
resolve Job 123
      ↓
resolve AppName
      ↓
resolve local executor
      ↓
/beat
      ↓
/api/triggerJob
      ↓
addressList = local executor
      ↓
capture logId
      ↓
/log
      ↓
result
```

Before triggering, the user should be able to place a breakpoint in:

```java id="j3"
@XxlJob("handlerName")
public void execute() {
    ...
}
```

Verify:

```text id="j4"
@XxlJob value
==
executorHandler
```

---

# 10. Executor Direct Trigger

Use executor `/trigger` only when the user explicitly wants executor-local testing and the executor/task metadata is already known.

```http id="k1"
POST {EXECUTOR_URL}/trigger
```

Payload:

```json id="k2"
{
  "jobId": 123,
  "executorHandler": "demoJobHandler",
  "executorParams": "debug",
  "executorBlockStrategy": "SERIAL_EXECUTION",
  "executorTimeout": 0,
  "logId": 0,
  "logDateTime": 0,
  "glueType": "BEAN",
  "glueSource": "",
  "glueUpdatetime": 0,
  "broadcastIndex": 0,
  "broadcastTotal": 0
}
```

Prefer `/api/triggerJob` when the scheduler-side execution path is part of the test.

The executor API provides `/trigger` specifically for triggering a task on the executor.

---

# 11. Get Execution Log

After obtaining:

```text id="l1"
logId
logDateTime
```

call:

```http id="l2"
POST {EXECUTOR_URL}/log
```

Request:

```json id="l3"
{
  "logId": 12345,
  "logDateTime": 1586629003729,
  "fromLineNum": 0
}
```

Response:

```json id="l4"
{
  "code": 200,
  "content": {
    "fromLineNum": 0,
    "toLineNum": 100,
    "logContent": "...",
    "isEnd": true
  }
}
```

For rolling logs:

```text id="l5"
fromLineNum
→ next fromLineNum
→ ...
→ isEnd=true
```

The executor API defines `fromLineNum` and `isEnd` for rolling log retrieval.

---

# 12. Determine Actual Result

Always distinguish:

```text id="m1"
Trigger accepted
≠
Executor started
≠
Task completed
≠
Task succeeded
```

Determine:

```yaml id="m2"
triggerResult:
executionStatus:
jobResult:
log:
```

Possible states:

```text id="m3"
TRIGGER_FAILED
RUNNING
SUCCESS
FAILED
UNKNOWN
```

Use execution logs and executor/scheduler results as evidence.

---

# 13. Busy Check

When a task may already be running:

```http id="n1"
POST {EXECUTOR_URL}/idleBeat
```

```json id="n2"
{
  "jobId": 123
}
```

Use this before retriggering a long-running or serial task.

The executor API defines `/idleBeat` for checking whether a specified task is busy.

---

# 14. Kill Running Task

For a running local/debug task:

```http id="o1"
POST {EXECUTOR_URL}/kill
```

```json id="o2"
{
  "jobId": 123
}
```

Use only for:

```text
explicit user request
or
clearly isolated local debugging
```

The kill API terminates the executor-side task.

---

# 15. Delete Task

Use:

```http id="p1"
POST {ADMIN_URL}/api/removeJob
```

```json id="p2"
{
  "id": 123
}
```

Delete temporary debug tasks after testing when requested or when they were created solely for the debugging workflow.

Do not delete an existing task merely because the debug run failed.

The management API defines `removeJob` for deleting a specified task.

---

# 16. Common Debug Workflows

## A. Existing task → local execution

```text id="q1"
resolve task
→ resolve local executor
→ /beat
→ triggerJob(addressList=local)
→ log
→ result
```

## B. Create temporary debug task

```text id="q2"
resolve executor
→ create task
→ capture jobId
→ start task
→ trigger once
→ log
→ result
→ delete task
```

## C. Modify existing task for debugging

```text id="q3"
resolve job
→ update executorParam / schedule configuration
→ trigger once
→ inspect log
→ restore original configuration when necessary
```

Prefer avoiding persistent changes when `triggerJob.executorParam` can solve the test.

## D. Debug a stuck task

```text id="q4"
resolve executor
→ idleBeat
→ log
→ determine running state
→ kill if appropriate
```

---

# 17. Task Creation Parameter Rules

When creating a task, explicitly resolve:

```text id="r1"
executor
task name
author
schedule type
schedule configuration
route strategy
handler
executor param
block strategy
timeout
retry count
glue type
```

For normal Bean debugging:

```text id="r2"
scheduleType = NONE or CRON
glueType = BEAN
executorHandler = actual @XxlJob value
```

For one-shot debugging, prefer:

```text id="r3"
scheduleType = NONE
```

and invoke:

```text id="r4"
triggerJob
```

instead of creating a recurring schedule unnecessarily.

The task management API supports `NONE`, `CRON`, and `FIX_RATE` scheduling.

---

# 18. Error Classification

Classify failures by operation:

```text id="s1"
Configuration
→ cannot resolve Admin / Token / AppName

Executor
→ /beat failed

Task
→ invalid Job ID / Handler / task configuration

Trigger
→ triggerJob failed

Execution
→ handler/business code failed

Log
→ log retrieval failed

Termination
→ kill failed
```

Once evidence shows that the problem is in business code, hand off to:

```text id="s2"
rigorous-code-analysis
```

---

# 19. Output

### Trigger

```text id="t1"
Job:
AppName:
Executor:
Handler:
Param:
LogId:
Status:
Result:
```

### Create

```text id="t2"
Task created
JobId:
Executor:
Handler:
Schedule:
Status:
```

### Update

```text id="t3"
Task updated
JobId:
Changed:
Status:
```

### Failure

```text id="t4"
XXL-JOB operation failed

Action:
JobId:
Executor:
Stage:
Error:
Evidence:
```

Keep output focused on the operation and evidence.

---

# 20. Core Execution Protocol

```text id="u1"
1. Parse request
2. Resolve Admin URL / AccessToken / AppName
3. Resolve Job / Handler
4. Resolve executor
5. /beat
6. Execute requested API
7. Capture JobId / LogId
8. /log when applicable
9. Determine actual result
10. Hand off code problems to rigorous-code-analysis
```

For local debugging:

```text id="u2"
Task
 ↓
Local Executor
 ↓
/beat
 ↓
triggerJob + addressList
 ↓
IntelliJ breakpoint
 ↓
logId
 ↓
/log
 ↓
result
```
