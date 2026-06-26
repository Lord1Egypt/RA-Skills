# Real Examples

Use these examples to see how rough requests should be compiled into higher-signal implementation briefs.

## Example 1: Multi-Product Isolation Architecture

### Raw request

```text
我们现在有一套测试系统，前端 React，后端 FastAPI，数据库是本地 SQLite。想支持两个被测产品，功能完全一样，但数据必须完全隔离，怎么设计？
```

### Best task type

`architecture-review`

### Why

- The core problem is not a page, API, or CRUD flow.
- The request is about boundaries, isolation, scaling, rollout, and trade-offs.

### Better compiled direction

```text
Goal:
Design a practical multi-product architecture for an existing React + FastAPI + SQLite testing system.

Current Task:
Recommend the smallest robust architecture that supports two products with fully isolated data and identical features.

Known Context:
- frontend: React
- backend: FastAPI
- database: local SQLite
- current system: single product
- target: two products, same functionality, isolated data

Assumptions:
- prefer one codebase with multiple deployments over two divergent codebases
- current priority is correctness and isolation, not large-scale tenant abstraction

Scope:
- product boundary design
- deployment topology
- data isolation model
- config strategy
- migration path from current single-system setup

Out of Scope:
- full rewrite
- microservices without clear need
- speculative multi-region design

Acceptance Criteria:
- recommended architecture is implementable on the current stack
- trade-offs are explicit
- rollout can happen incrementally
```

### Good extra instruction for coding tools

```text
Recommend the smallest robust path for the current stack. Compare 2-3 options, then choose one and give a phased rollout plan.
```

## Example 2: Vague Bugfix

### Raw request

```text
登录这里老是报 500，你帮我修一下。
```

### Best task type

`bugfix`

### Why

- The request mentions a concrete failure mode.
- The right move is root-cause analysis plus the smallest safe fix.

### Better compiled direction

```text
Goal:
Diagnose and minimally fix the login 500 error.

Current Task:
Identify the root cause of the failure and apply the smallest safe fix.

Known Context:
- symptom: login returns 500
- expected behavior: login succeeds or returns a clear auth error
- actual behavior: server error

Assumptions:
- preserve existing login behavior outside the fix
- start from logs, handler logic, validation, and database interaction

Scope:
- root-cause analysis
- targeted fix
- verification steps

Out of Scope:
- unrelated auth redesign
- refactoring the whole login module
```

### Good extra instruction for coding tools

```text
Start with root-cause analysis. Preserve existing behavior outside the fix and keep the patch surgical.
```

## Example 3: CRUD Feature from a One-Liner

### Raw request

```text
给后台加一个设备管理功能。
```

### Best task type

`crud-feature`

### Why

- "管理功能" usually implies entity lifecycle: create, list, edit, delete.
- The request is broad but still centered on one business entity.

### Better compiled direction

```text
Goal:
Build the smallest useful device management CRUD workflow.

Current Task:
Implement the first vertical slice for device management.

Known Context:
- entity: device
- likely operations: create, list, edit, disable/delete
- audience: admin users

Assumptions:
- device records need a minimal schema first
- build list + create first before adding broader management actions

Scope:
- minimal schema
- backend endpoints
- admin list view
- create flow with validation

Out of Scope:
- advanced permissions
- analytics dashboards
- bulk import unless requested
```

## Example 4: Third-Party Integration

### Raw request

```text
把我们的系统和企业微信审批打通，审批通过后自动回写状态。
```

### Best task type

`integration`

### Why

- The core problem is external-system interaction.
- Auth, callbacks, retries, and idempotency are central.

### Better compiled direction

```text
Goal:
Integrate the system with WeCom approval and sync status changes back reliably.

Current Task:
Design and implement the smallest safe integration slice.

Known Context:
- source system: our app
- target system: WeCom approval
- primary flow: approval result should update internal status

Assumptions:
- webhook or callback-based integration is available
- duplicate callbacks must be handled safely

Scope:
- auth flow
- callback/webhook handling
- status mapping
- retry and idempotency behavior

Out of Scope:
- unrelated workflow redesign
- all future approval types
```

### Good extra instruction for coding tools

```text
Make auth, callback verification, retries, and idempotency explicit. Prefer a narrow first slice for one approval flow.
```

## Example 5: Automation Workflow

### Raw request

```text
做一个自动化流程，定时扫描目录里的文件，解析后入库，失败就提醒我。
```

### Best task type

`automation-workflow`

### Why

- Trigger, background execution, failure handling, and alerting are the core concerns.
- This is not just an API change.

### Better compiled direction

```text
Goal:
Design a reliable workflow that scans files on a schedule, parses them, stores records, and alerts on failures.

Current Task:
Define the minimal reliable workflow and implement the first slice.

Known Context:
- trigger: scheduled scan
- input: files in a watched directory
- output: parsed records in a database
- failure path: alert the operator

Assumptions:
- file parsing can partially fail
- runs should be restartable and observable

Scope:
- trigger and execution states
- parse/store flow
- retries and idempotency
- alert conditions

Out of Scope:
- generic workflow platform abstraction
- advanced orchestration before the main path works
```

## Example 6: AI Feature with Product Context

### Raw request

```text
给知识库问答加一个自动总结和推荐下一步操作的功能。
```

### Best task type

`ai-feature`

### Why

- The request is about model-driven output and interaction design.
- Prompt shape, failure handling, and output structure matter.

### Better compiled direction

```text
Goal:
Add an AI feature that summarizes the answer and recommends next actions.

Current Task:
Design the smallest useful workflow for generating summary plus suggested actions.

Known Context:
- existing product: knowledge-base QA
- new output: summary + next-step suggestions
- user value: faster decision-making after reading answers

Assumptions:
- suggestions should be structured and bounded
- output should degrade gracefully when confidence is low

Scope:
- prompt shape
- backend invocation path
- output structure
- failure and empty-result handling

Out of Scope:
- agent orchestration
- evaluation framework unless explicitly requested
```

## Example 7: Deployment Request

### Raw request

```text
帮我把这个 React + FastAPI 项目部署到 Windows 机器上，最好后面也方便迁移。
```

### Best task type

`deployment`

### Why

- The primary task is environment setup and rollout strategy.
- The migration hint means trade-offs matter, but deployment is still the main job.

### Better compiled direction

```text
Goal:
Prepare a reliable Windows deployment path for a React + FastAPI project with a future migration path.

Current Task:
Recommend the simplest deployment setup that works now and does not block later migration.

Known Context:
- frontend: React
- backend: FastAPI
- current target: Windows
- future concern: easier migration later

Assumptions:
- prefer explicit config and simple service management
- avoid platform-specific lock-in where easy to prevent

Scope:
- process model
- config and env vars
- deployment steps
- verification and rollback

Out of Scope:
- full cloud redesign
- unrelated application changes
```

## Example 8: Turning a Rough Request into a Codex Handoff

### Raw request

```text
把用户列表页改得更好看一点，顺便支持搜索和分页。
```

### Best task type

`page-ui` or `crud-feature`

### Routing note

- If the core ask is UX and layout, choose `page-ui`.
- If the core ask is list interactions around an entity workflow, `crud-feature` is also reasonable.
- In this case, prefer `page-ui` if the backend already supports search/pagination. Prefer `crud-feature` if the feature requires end-to-end API changes.

### Example handoff wrapper

```text
Use this brief as the source of truth. First clarify whether search and pagination already exist in the backend. If they do, implement only the UI slice. If not, propose the smallest end-to-end slice and keep the diff minimal.
```

## Practical Heuristic

When choosing between templates:

- if the user is really asking "what should we build" -> `new-project`
- if they are asking "why is this broken" -> `bugfix`
- if they are asking "how should this system be shaped" -> `architecture-review`
- if they are asking "how do we connect to that system" -> `integration`
- if they are asking "how should this recurring/background flow work" -> `automation-workflow`
- if they are asking "how do we add this model-powered behavior" -> `ai-feature`
