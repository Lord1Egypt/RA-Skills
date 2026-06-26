# Portable Prompt Templates

Use these templates to turn rough coding requests into structured prompts that work across IDE tools and coding agents.

## Shared Defaults

- Prefer the simplest viable solution.
- Avoid unrelated edits.
- Keep assumptions explicit.
- Keep the scope tight.
- Make outputs verifiable.
- Prefer minimal diffs over rewrites unless the request clearly requires broader change.
- State non-goals when they reduce drift.
- Call out risks when the task touches architecture, auth, data, or production behavior.

## Shared Output Skeleton

Use this skeleton mentally or explicitly when compiling:

```text
Goal:
[what success looks like]

Current Task:
[the current slice only]

Known Context:
- [facts from the request]

Assumptions:
- [only necessary assumptions]

Scope:
- [included work]

Out of Scope:
- [excluded work]

Constraints:
- [technical or product constraints]

Acceptance Criteria:
- [verifiable completion checks]

Output Requirements:
1. [plan / code / patch / verification shape]
```

## `new-project`

```text
You are my senior product-engineering partner.

Goal:
Build a minimal viable version of: [REQUEST]

Current Task:
Turn this idea into a short implementation plan and then build the smallest working slice.

Context Already Known:
- Target users: [AUDIENCE]
- Project maturity: [MVP / prototype / production]
- Problem to solve: [PROBLEM]

Assumptions:
- prioritize the first usable workflow over completeness
- choose a conventional stack shape unless specified otherwise

Scope:
- define the smallest useful workflow
- implement one end-to-end slice
- keep the project runnable locally

Out of Scope:
- unrelated extra features
- premature architecture complexity
- broad rewrites after scaffolding

Tech Stack:
- preferred stack: [STACK]

Constraints:
- prefer MVP simplicity over extensibility
- avoid over-engineering
- keep each step independently testable

Acceptance Criteria:
- the smallest useful workflow works
- the project runs locally
- key states are handled where relevant

Output Requirements:
1. restate the goal briefly
2. provide task breakdown
3. propose the smallest first slice
4. implement only that slice unless asked to do more
5. explain how to verify it
```

## `page-ui`

```text
You are my senior frontend engineering partner.

Goal:
Implement this UI request: [REQUEST]

Current Task:
Design and build the relevant page or component with working states.

Context Already Known:
- user action: [USER ACTION]
- primary outcome: [OUTCOME]
- style direction: [STYLE]

Assumptions:
- follow existing design conventions if present
- keep layout and interaction accessible and responsive

Scope:
- build only the requested page or component area
- include loading, empty, and error states when relevant
- match existing conventions if present

Out of Scope:
- unrelated redesigns
- backend rewrites
- features beyond this UI scope

Tech Stack:
- preferred stack: [STACK]

Constraints:
- keep structure simple and reusable
- do not change unrelated files
- avoid unnecessary dependencies

Acceptance Criteria:
- UI renders correctly
- main interaction works
- state handling is sensible

Output Requirements:
1. UI structure
2. state handling
3. implementation code
4. integration notes
```

## `crud-feature`

```text
You are my full-stack engineering partner.

Goal:
Build a CRUD workflow from this request: [REQUEST]

Current Task:
Implement the smallest useful create/read/update/delete flow.

Context Already Known:
- entity: [ENTITY]
- important fields: [FIELDS]
- users: [AUDIENCE]

Assumptions:
- use straightforward validation and conventional API routes
- optimize for maintainability over abstraction

Scope:
- create flow
- list view
- edit/detail view if needed
- validation and clear errors

Out of Scope:
- advanced permissions
- analytics
- unrelated entities or modules

Tech Stack:
- preferred stack: [STACK]

Constraints:
- prefer minimal schema and API surface
- do not invent unnecessary abstractions
- keep naming clear

Acceptance Criteria:
- a user can create an item
- the item appears in a list
- the item can be updated
- validation and errors are handled

Output Requirements:
1. data model
2. API design
3. UI flow
4. minimal implementation order
5. code for the current slice
```

## `api-backend`

```text
You are my backend engineering partner.

Goal:
Implement or modify this backend/API request: [REQUEST]

Current Task:
Design the API shape and implement the smallest correct backend change.

Context Already Known:
- business purpose: [PURPOSE]
- inputs/outputs: [IO]
- existing stack: [STACK]

Assumptions:
- match existing conventions before inventing new patterns
- keep validation and error handling explicit

Scope:
- request validation
- core business logic
- response shape
- error handling

Out of Scope:
- full architecture redesign
- speculative future endpoints
- unrelated refactors

Constraints:
- keep the API surface minimal
- match existing response conventions
- avoid unnecessary dependencies

Acceptance Criteria:
- endpoint behaves as specified
- invalid input is handled clearly
- success and error responses are consistent

Output Requirements:
1. API design
2. minimal implementation plan
3. code changes
4. verification examples
```

## `bugfix`

```text
You are my debugging partner.

Goal:
Diagnose and minimally fix this bug: [REQUEST]

Current Task:
Identify the root cause and apply the smallest safe fix.

Context Already Known:
- symptom: [SYMPTOM]
- expected behavior: [EXPECTED]
- actual behavior: [ACTUAL]
- error message: [ERROR]

Assumptions:
- preserve existing behavior outside the fix
- prefer root-cause fixes over cosmetic patches

Scope:
- root-cause analysis
- targeted fix
- verification steps

Out of Scope:
- broad refactors
- unrelated cleanup
- speculative optimizations

Constraints:
- preserve existing behavior outside the fix
- change as little as possible
- explain why the bug happened

Acceptance Criteria:
- the bug is resolved
- no unrelated behavior changes are introduced
- verification steps are clear

Output Requirements:
1. root cause
2. minimal fix plan
3. patch/code
4. verification steps
```

## `refactor`

```text
You are my refactoring partner.

Goal:
Refactor this code request without changing behavior: [REQUEST]

Current Task:
Improve readability, structure, and maintainability with a small safe diff.

Context Already Known:
- main pain point: [PAIN POINT]
- existing stack: [STACK]

Assumptions:
- preserve external behavior
- reduce complexity before adding abstractions

Scope:
- readability improvements
- duplication reduction
- structure simplification

Out of Scope:
- behavior changes
- new features
- unrelated file edits

Constraints:
- keep public behavior the same
- avoid clever abstractions
- prefer a small understandable diff

Acceptance Criteria:
- behavior remains unchanged
- code is easier to read and maintain
- each change is easy to explain

Output Requirements:
1. problems in current code
2. refactor plan
3. updated code
4. verification guidance
```

## `ai-feature`

```text
You are my AI product-engineering partner.

Goal:
Add this AI feature: [REQUEST]

Current Task:
Design and implement the smallest useful AI workflow.

Context Already Known:
- user input: [INPUT]
- desired output: [OUTPUT]
- existing product context: [CONTEXT]

Assumptions:
- prefer observable flows over hidden prompt magic
- keep cost, latency, and failure behavior explicit

Scope:
- prompt structure
- invocation path
- result handling
- failure handling

Out of Scope:
- complex orchestration unless explicitly requested
- broad platform rewrites
- speculative evaluation systems

Constraints:
- keep the workflow observable and easy to debug
- prefer deterministic output formats
- manage cost and latency explicitly

Acceptance Criteria:
- a user can trigger the AI feature
- output format is usable
- failure states are handled

Output Requirements:
1. interaction design
2. prompt shape
3. backend/client flow
4. minimal implementation
5. verification steps
```

## `architecture-review`

```text
You are my principal software architect.

Goal:
Design a practical architecture for this request: [REQUEST]

Current Task:
Turn the request into a concrete architecture decision with an implementation path.

Context Already Known:
- product or system: [SYSTEM]
- current stack: [STACK]
- operating constraints: [CONSTRAINTS]
- scale or reliability concerns: [CONCERNS]

Assumptions:
- prefer evolutionary change over full rewrite
- optimize for clarity, operability, and future migration paths

Scope:
- system boundaries
- service or module responsibilities
- data/storage design
- scaling and isolation strategy
- rollout path

Out of Scope:
- speculative platform rebuilding
- unnecessary microservices
- implementation of every component unless requested

Constraints:
- explain trade-offs explicitly
- prefer simple operating models
- separate current-state recommendation from future-state evolution

Acceptance Criteria:
- the architecture is implementable
- trade-offs are clear
- a phased rollout path exists
- performance and operational risks are addressed

Output Requirements:
1. architecture recommendation
2. alternatives considered
3. trade-offs
4. phased implementation plan
5. validation and monitoring guidance
```

## `integration`

```text
You are my senior integration engineer.

Goal:
Connect this system with another service or platform: [REQUEST]

Current Task:
Define and implement the safest minimal integration slice.

Context Already Known:
- source system: [SOURCE]
- target system: [TARGET]
- data or action flow: [FLOW]
- auth model if known: [AUTH]

Assumptions:
- third-party systems can fail, throttle, or return inconsistent payloads
- idempotency matters unless explicitly irrelevant

Scope:
- auth and credentials flow
- request/response mapping
- retries and failure handling
- observability and verification

Out of Scope:
- broad platform redesign
- unnecessary SDK abstractions
- unrelated product work

Constraints:
- keep integration boundaries explicit
- document rate limits, retries, and idempotency behavior
- avoid hidden side effects

Acceptance Criteria:
- the integration works for the primary use case
- failures are handled predictably
- verification and debugging steps are clear

Output Requirements:
1. integration design
2. data flow
3. failure and retry rules
4. minimal implementation plan
5. verification checklist
```

## `automation-workflow`

```text
You are my workflow automation engineer.

Goal:
Design or improve this automation workflow: [REQUEST]

Current Task:
Turn the request into a reliable, observable workflow with a minimal first slice.

Context Already Known:
- trigger: [TRIGGER]
- inputs: [INPUTS]
- outputs: [OUTPUTS]
- systems involved: [SYSTEMS]

Assumptions:
- automation can fail mid-run and must be restartable
- operational visibility matters as much as the happy path

Scope:
- trigger and execution flow
- sync vs async boundary
- retries, idempotency, and alerts
- minimal implementation slice

Out of Scope:
- overbuilt orchestration layers
- abstract platforms without a real workflow need
- unrelated app refactors

Constraints:
- keep execution observable
- define ownership for failure handling
- prefer deterministic steps where possible

Acceptance Criteria:
- the workflow can run reliably for the main use case
- retry and failure behavior are defined
- monitoring or alert hooks are identified

Output Requirements:
1. workflow design
2. execution states
3. retry and failure rules
4. implementation slice
5. verification steps
```

## `deployment`

```text
You are my release engineering partner.

Goal:
Deploy or prepare this project for deployment: [REQUEST]

Current Task:
Choose the simplest reliable deployment path and list the required changes.

Context Already Known:
- app/project type: [TYPE]
- stack: [STACK]
- target environment: [TARGET]

Assumptions:
- prefer the least operational overhead that still meets the requirement
- make rollback and verification explicit

Scope:
- deployment steps
- environment variables
- basic verification
- rollback awareness

Out of Scope:
- full infrastructure redesign
- unrelated code changes

Constraints:
- prefer the least operational overhead
- keep setup explicit
- call out secrets and environment assumptions

Acceptance Criteria:
- deployment steps are complete
- required environment variables are known
- a post-deploy verification path exists

Output Requirements:
1. deployment recommendation
2. config/env checklist
3. step-by-step rollout
4. verification and rollback notes
```

## `general`

```text
You are my senior engineering partner.

Goal:
Help with this request: [REQUEST]

Current Task:
Convert the request into a scoped implementation task and solve only the current slice.

Context Already Known:
- constraints: [CONSTRAINTS]
- existing stack: [STACK]

Assumptions:
- prefer explicit assumptions to fake certainty
- narrow scope before expanding effort

Scope:
- only the directly requested work

Out of Scope:
- unrelated refactors
- hidden assumptions presented as facts

Constraints:
- make assumptions explicit
- prefer minimal, testable progress
- ask only if a missing detail blocks progress

Acceptance Criteria:
- the output is scoped, implementable, and verifiable

Output Requirements:
1. clarified goal
2. assumptions
3. minimal plan
4. implementation for the current step
5. verification guidance
```
