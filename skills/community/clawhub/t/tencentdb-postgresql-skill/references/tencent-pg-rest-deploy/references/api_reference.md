# One-sentence REST service control, invocation, and troubleshooting reference

## Scope

This reference supports three closely related goals for TencentDB for PostgreSQL REST / PostgREST:

1. **service control** — open or close REST service for one target instance
2. **read-only REST invocation** — execute safe public GET requests against the current PostgREST service on the user's behalf
3. **REST troubleshooting** — diagnose gateway or connectivity failures such as `502`, missing address exposure, or likely security-group blockers

## Baseline capability model

### Control-plane OpenAPI baseline
- Endpoint: `https://postgres.tencentcloudapi.com`
- Version: `2017-03-12`
- Auth: `TC3-HMAC-SHA256`
- Preferred call path: official Tencent Cloud SDK or locally generated TC3-signed HTTPS request
- Credentials: read from runtime environment only
- Optional raw-action endpoint overrides already supported by the repository: `POSTGRES_POSTGREST_ENDPOINT`, `POSTGRES_POSTGREST_DESCRIBE_ENDPOINT`

### PostgREST runtime-call baseline
- Preferred runtime-call path inside this repository: `QueryPostgRESTService`
- Current execution scope: **public PostgREST endpoint only**, **read-only GET only**
- Default safety posture: use `OpenPostgRESTService` with `EnableWanNet=false` unless the user explicitly needs public / external exposure and gives a second explicit confirmation for opening it
- Do not auto-issue internal/private-address HTTP requests in this skill
- Do not hardcode secrets or inject JWT-like material from repository files or chat history

## Recognized lanes

### 1. `service-control`
Use when the user clearly asks to open, enable, deploy, bring up, close, disable, stop, or take down REST / PostgREST service itself.

### 2. `rest-readonly-call`
Use when the user is clearly trying to call the REST endpoint, inspect the current OpenAPI description, list exposed resources, or query an already exposed REST path with a safe read-only GET request.

### 3. `rest-troubleshooting`
Use when the user reports a symptom such as `502`, timeout, gateway failure, endpoint unreachable, or asks why REST is not working.

Keep exactly one primary lane per execution step.

## Aligned tool set for this skill

### Read-only control-plane actions
- `DescribeRegions` — optional when region input is missing, or when the current region is blocked and candidate regions must be returned
- `DescribeDBInstances` — optional discovery when the request does not specify an instance and region is already known
- `DescribeDBInstanceAttribute` — confirm the instance exists and collect suitability facts
- `DescribePostgRESTService` — confirm current REST status, returned access addresses, and whether opening / closing / invocation is feasible
- `DescribeTasks` — optional only when the instance appears to be in an ongoing task or transition state and task evidence is needed
- `DescribeDBInstanceSecurityGroups` — query the currently bound security-group set when troubleshooting network or gateway symptoms

### Read-only runtime-call action
- `QueryPostgRESTService` — issue one read-only GET request through the instance's **public** PostgREST address and return structured HTTP results

### Write actions
- `OpenPostgRESTService` — open REST service for the target instance
- `ClosePostgRESTService` — close REST service for the target instance
- `ModifyDBInstanceSecurityGroups` — replace the instance's bound security-group set **only when the user explicitly wants that binding change and the target set is already known**

## Important safety boundary for security groups

`ModifyDBInstanceSecurityGroups` only replaces which security groups are attached to the PostgreSQL instance. It does **not** edit ingress or egress rules inside an existing security group.

Therefore:
- if the actual fix is to add an internal-port rule such as the required backend port exposure inside the current security group, this skill must tell the user to change the rule manually in the console
- only when the intended fix is to switch the instance to another already-prepared security-group set may the skill proceed to confirmation and then execute `ModifyDBInstanceSecurityGroups`

## Operation success definitions

### Open success
Treat the service as opened successfully when:

1. `DescribePostgRESTService` shows a ready state such as `running` or another clearly usable success state
2. if the open call used `EnableWanNet=true`, a usable public access address field returned by the API is present and non-empty
3. if the open call used `EnableWanNet=false`, the absence of a public access address does **not** mean the open action failed; it means the service is enabled while public exposure remains closed

### Close success
Treat the close action as complete only when `DescribePostgRESTService` shows a closed / not-opened / unavailable state, or the service is otherwise no longer usable.

### Read-only invocation success
Treat the invocation as executed when:

1. `QueryPostgRESTService` completes an HTTP round trip through the public endpoint
2. the result clearly contains the returned `status_code`, URL, and body summary

An HTTP `404` or `400` still counts as a successful probe execution if the request reached PostgREST and returned a structured HTTP result. Do not confuse `request executed` with `resource exists`.

### Troubleshooting completion
Treat troubleshooting as complete when the current most-likely blocker is narrowed to a concrete class with evidence, for example:

- service not opened or not running
- public access address missing
- public endpoint reachable but the requested resource is absent from schema cache
- likely backend / internal-port exposure issue with supporting security-group evidence or strong indirect indicators

## Runtime slot sources and precedence

Resolve slots in the following order.

### 1. Region
1. explicit region from the user's sentence
2. normalized Chinese alias by following `@references/common/region_normalization.md`
3. runtime default `TENCENTCLOUD_REGION`

If none is available, stop with a direct region-acquisition block instead of a vague reminder. Include the PostgreSQL console entry [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres), tell the user to check the region switcher in the top-right corner or inspect the target instance row directly, and end with one copyable example such as `export TENCENTCLOUD_REGION="ap-guangzhou"`.

### 2. DBInstanceId
1. explicit `postgres-xxxxxxxx` instance ID from the user's sentence
2. runtime default `PG_REST_INSTANCE_ID`
3. runtime default `PG_POSTGREST_INSTANCE_ID`
4. runtime default `REST_INSTANCE_ID`
5. runtime default `POSTGREST_INSTANCE_ID`
6. auto-discovery through `DescribeDBInstances` only when the region is known and the result narrows safely to exactly one suitable instance

If multiple instances remain, stop and ask the user to reply with `region + instance ID`.

### 3. REST path and query for `rest-readonly-call`
1. explicit path from the user's sentence, command, or pasted URL fragment
2. when the request clearly means `show me what this service exposes`, default `Path=/`
3. optional explicit raw query string from the user's sentence, normalized to remove the leading `?`

Do not invent a resource path when the user is really asking for a specific table, function, or database object that was never provided.

## Minimum runtime prerequisites

### Tencent Cloud credentials
Require all of the following before any control-plane API call:

- `TENCENTCLOUD_SECRET_ID`
- `TENCENTCLOUD_SECRET_KEY`
- region from the slot-resolution rules above
- optional `TENCENTCLOUD_SESSION_TOKEN`

### REST-specific runtime defaults
Require the following before execution:

- resolved `DBInstanceId`
- for `rest-readonly-call`, a concrete public PostgREST address discoverable from `DescribePostgRESTService`

Recommended runtime template:

```bash
export TENCENTCLOUD_SECRET_ID="your SecretId"
export TENCENTCLOUD_SECRET_KEY="your SecretKey"
export TENCENTCLOUD_REGION="ap-guangzhou"
export PG_REST_INSTANCE_ID="postgres-abc12345"
```

## Target-resolution rules

### Preferred path
- use the explicit instance ID from the user whenever present
- keep the scope to one region and one instance only

### Safe auto-discovery path
Use `DescribeDBInstances` only when all of the following are true:

1. region is already resolved
2. the user clearly wants the current or default instance but did not specify the instance ID
3. the returned candidate set narrows safely to exactly one suitable instance

### Ambiguity stop rule
If discovery returns zero candidates or more than one reasonable candidate, stop and send one direct clarification line that explicitly says the skill is waiting for the user's clarification, for example:

```text
我可以继续处理 REST 服务，但当前目标实例还不唯一。等你确认目标后我再继续。请直接回复：ap-guangzhou postgres-abc12345
```

## Read-only preflight workflow

Run preflight in this order for every lane.

### Step 1: instance existence and scope
- use `DescribeDBInstances` only if instance discovery is needed
- otherwise go straight to `DescribeDBInstanceAttribute`

### Step 2: instance suitability
Use `DescribeDBInstanceAttribute` to confirm at least the following when the fields are available:

- instance exists in the resolved region
- instance is a primary instance rather than a readonly child when that matters for the requested action
- instance is in a usable lifecycle state such as `running`

### Step 3: current REST state
Use `DescribePostgRESTService` to gather:

- current REST status
- public address availability
- private address availability as background context only
- whether opening, closing, invocation, or troubleshooting should continue

### Step 3.5: unsupported-region fallback
Trigger this branch when `DescribePostgRESTService`, `OpenPostgRESTService`, or `ClosePostgRESTService` returns a clear signal that the instance region does not support REST / PostgREST service control.

When triggered:
1. record the current instance region and the exact blocker evidence returned by the API
2. call `DescribeRegions` to fetch the current PostgreSQL supported-region list
3. present that region list to the user as the next-region candidate set for REST follow-up
4. stop the normal write or polling path for the unsupported region

#### Latest scanned candidate record
As of `2026-07-20T06:40:56Z`, this repository has a live scan artifact at `tmp/postgrest-region-scan.json`.

Scan method:
- fetch PostgreSQL regions through `DescribeRegions`
- run `DescribeDBInstances(Limit=1)` in each region first
- when the current account has a real instance in that region, probe that real instance with `DescribePostgRESTService`
- when the region currently has no instance in this account, fall back to `DescribePostgRESTService(DBInstanceId=postgres-00000000)` only as a **placeholder control-path probe**
- **do not** treat `ResourceNotFound.InstanceNotFoundError` from the placeholder probe as full feature support; it only shows that the request reached instance validation
- if `DescribeRegions` marks a region as `UNAVAILABLE`, do **not** present it as a normal candidate even when the raw API does not reject it early

Current regions with **real-instance verification and still allowed as automatic follow-up candidates** (`DescribeDBInstances` found an instance and `DescribePostgRESTService` returned success, and this repository has not manually downgraded them for execution policy reasons):
- `ap-shanghai`

Current regions that are only **placeholder-probe accepted** (`DescribeRegions.RegionState=AVAILABLE` and the placeholder probe reached instance validation, but this repository does not currently have a same-region instance proving full support):
- `ap-beijing`
- `ap-guangzhou`
- `ap-hongkong`
- `ap-seoul`
- `ap-shanghai-fsi`
- `ap-shenzhen`
- `ap-singapore`
- `ap-tianjin`
- `eu-frankfurt`
- `na-siliconvalley`

Regions currently returned by `DescribeRegions` as `UNAVAILABLE`, so they should not be offered as normal REST follow-up candidates:
- `ap-guangzhou-open`
- `ap-shenzhen-fsi`
- `na-ashburn`
- `na-toronto`

Important note for Chengdu:
- this repository rechecked `ap-chengdu` with a **real instance probe** on `2026-07-20`
- `DescribePostgRESTService` returned success with `Status=not_open`
- however, until a later `OpenPostgRESTService`-level verification confirms the write path, this skill should **temporarily treat Chengdu as unsupported for automatic candidate recommendation and follow-up routing**
- keep the raw scan artifact unchanged, but do not offer Chengdu as a default next-region candidate in the skill narrative for now

### Step 4: lane-specific evidence
- for `service-control`: no extra evidence unless the instance appears busy and `DescribeTasks` is needed
- for `rest-readonly-call`: run `QueryPostgRESTService` against the resolved path
- for `rest-troubleshooting`: run one minimal public probe such as `Path=/`; when the symptom looks network-related or gateway-related, also call `DescribeDBInstanceSecurityGroups`

## Lane-specific execution rules

### `service-control`

#### Open path
Do **not** equate `open REST service` with `open public exposure`.

Safe default path:
- when the user asks to open, deploy, enable, or bring up REST / PostgREST service without explicitly asking for public / external exposure, call `OpenPostgRESTService` with `EnableWanNet=false`
- this means the skill enables REST service while keeping public access closed by default

Exposure-changing path:
- only when the user explicitly asks to expose the service on the public / external network, or otherwise requests `EnableWanNet=true`, should the skill enter the confirmation-waiting branch
- in that branch, explain the public-exposure risk first and wait for the user's second explicit confirmation

Execute `OpenPostgRESTService` when all of the following are true:
1. the sentence explicitly asks to open, deploy, enable, or bring up REST / PostgREST service
2. region and target instance are unambiguous
3. read-only preflight found no material blocker
4. REST is not already ready
5. if the call would use `EnableWanNet=true`, the user has already provided a second explicit confirmation after the risk explanation

#### Close path
Execute `ClosePostgRESTService` only when all of the following are true:
1. the sentence explicitly asks to close, disable, stop, or take down REST / PostgREST service
2. region and target instance are unambiguous
3. read-only preflight shows the service is currently closable
4. read-only preflight found no material blocker

### `rest-readonly-call`
Execute `QueryPostgRESTService` only when all of the following are true:
1. the request is a safe read-only GET intent
2. the instance and region are unambiguous
3. the public PostgREST address is available
4. the path is concrete or safely defaulted to `/`

If the user is trying to do a write-style REST mutation such as POST/PUT/PATCH/DELETE data changes, do not pretend this skill can silently execute it through the same read-only path. Explain that the current repository-side runtime tool is read-only GET, and keep any risky follow-up behind explicit confirmation or a copyable manual command.

### `rest-troubleshooting`
Use the following narrowing order:
1. service not running or not opened
2. public access address missing
3. public endpoint reachable but requested resource absent or schema-cache limited
4. public endpoint still fails with gateway-style symptom and the current security-group evidence suggests missing internal-port exposure or another backend-network blocker

When the security-group branch is selected:
- state whether the current evidence is **confirmed** or only **high-probability**
- explicitly state that direct rule editing is not supported by this repository
- only offer `ModifyDBInstanceSecurityGroups` when the intended fix is to switch to another already-known security-group set
- otherwise tell the user to modify the security-group rule manually in the console

## Confirmation-waiting response rule

Use this response shape whenever the next step still needs user confirmation, clarification, or an explicit go-ahead before a risky or scope-changing action.

The reply must include all of the following:
1. an explicit waiting phrase such as `等你确认`、`确认后我再继续`
2. the exact pending action that will happen after confirmation
3. why that pending action matters
4. the main risk, impact, or scope change
5. for a public-exposure `OpenPostgRESTService` branch, an explicit statement that **public / external access stays closed by default for security** until the second confirmation arrives
6. one minimal copyable reply example when possible

Apply this rule to:
- `OpenPostgRESTService` when the pending call would use `EnableWanNet=true`
- `ClosePostgRESTService` when the user did not clearly ask for close
- `ModifyDBInstanceSecurityGroups`
- any attempted follow-up that would change exposure or traffic path instead of just diagnosing

## Polling policy after write

After a successful `OpenPostgRESTService` or `ClosePostgRESTService` call:
- poll `DescribePostgRESTService` every 10 seconds
- stop after 18 attempts at most
- for **open** with `EnableWanNet=true`, stop earlier if a ready state plus usable public address appears
- for **open** with `EnableWanNet=false`, stop earlier if a ready state appears even when no public address is returned
- for **close**, stop earlier if a closed / unavailable state appears and the service is no longer usable
- stop earlier on a terminal API error

If the wait budget is exhausted and the service is still applying the change, return a truthful partial result with the latest observed status.

## Final output schema

### 1. Target scope
- region
- instance ID

### 2. Recognized lane
- `service-control`
- `rest-readonly-call`
- `rest-troubleshooting`
- routing reason

### 3. Resolved slots
- `DBInstanceId`
- relevant path and raw query when applicable
- source of each slot: user sentence or runtime default

### 4. Preflight facts
- instance existence
- current REST state
- current public-address availability
- current security-group evidence when checked

### 5. Executed actions
- read-only actions used
- whether `OpenPostgRESTService` or `ClosePostgRESTService` was executed
- whether `QueryPostgRESTService` was executed and against which URL/path
- whether `ModifyDBInstanceSecurityGroups` is only being proposed or was actually executed after confirmation

### 6. Final result
- final REST status
- returned access address or endpoint on open success
- direct HTTP result for read-only invocation
- troubleshooting conclusion and evidence class
- whether the repository can auto-fix the blocker or only guide manual remediation
- explicit confirmation-waiting wording when the next step still needs user approval
- one minimal next-step example

## Guardrails

- Never read secrets from repository files or ask the user to paste them into chat.
- Never auto-issue private-address HTTP probes in this skill.
- Never claim that a `400` or `404` means the endpoint is down if PostgREST actually returned a structured HTTP response.
- Never claim a security-group rule was modified if only the instance binding was changed.
- Never call `OpenPostgRESTService` or `ClosePostgRESTService` twice for the same request.
- Never auto-call the opposite direction action as a rollback or retry strategy.
- Never claim open success without both a ready state and a usable public access address.
- Keep every summary tightly scoped to one target instance.
