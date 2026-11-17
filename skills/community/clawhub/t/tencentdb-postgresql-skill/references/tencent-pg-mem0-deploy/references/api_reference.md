# One-sentence mem0 service control OpenAPI reference

## Scope

This reference supports one goal only: turn a single natural-language mem0 service-control request into either a ready-to-use TencentDB for PostgreSQL mem0 service or a confirmed mem0 shutdown whenever the target and runtime prerequisites are sufficient.

## Direct OpenAPI baseline

- Endpoint: `https://postgres.tencentcloudapi.com`
- Version: `2017-03-12`
- Auth: `TC3-HMAC-SHA256`
- Preferred call path: official Tencent Cloud SDK; fallback: locally generated TC3-signed HTTPS request
- Credentials: read from runtime environment only
- Never hardcode secrets, never write them into repository files, and never ask the user to paste them into chat when runtime environment is the intended source

## Aligned action set for this skill

### Read-only actions
- `DescribeDBInstances` — optional discovery when the request does not specify an instance and region is already known
- `DescribeDBInstanceAttribute` — confirm the instance exists and collect suitability facts
- `DescribeMem0Service` — confirm the current mem0 state, endpoint, and whether opening or closing is needed
- `DescribeTasks` — optional only when the instance appears to be in an ongoing task or transition state and task evidence is needed

### Write actions
- `OpenMem0Service` — open mem0 service for the target instance
- `CloseMem0Service` — close mem0 service for the target instance

## Operation success definitions

### Open success
Treat the service as ready to use only when both conditions are true:

1. `DescribeMem0Service` shows a ready state such as `running` or another clearly usable success state
2. a usable endpoint field such as `InnerAddress` is present and non-empty

### Close success
Treat the close action as complete only when `DescribeMem0Service` shows a closed / not-opened / unavailable state, or the service is otherwise no longer usable. If the API shape keeps stale endpoint fields for a short time, prioritize the explicit closed-state signal over field cleanup timing.

If the service is still provisioning, opening, or deleting, return the current state rather than claiming success.

## Runtime slot sources and precedence

Resolve slots in the following order.

### 1. Region
1. explicit region from the user's sentence
2. normalized Chinese alias by following `@references/common/region_normalization.md`
3. runtime default `TENCENTCLOUD_REGION`

If none is available, stop with a direct region-acquisition block instead of a vague reminder. Always include the PostgreSQL console entry [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres), tell the user to check the region switcher in the top-right corner or inspect the target instance row directly, and end with one copyable example such as `export TENCENTCLOUD_REGION="ap-guangzhou"`. If current credentials are already usable, also offer to query PostgreSQL supported regions on the user's behalf instead of only asking the user to check links.

### 2. DBInstanceId
1. explicit `postgres-xxxxxxxx` instance ID from the user's sentence
2. runtime default `PG_MEM0_INSTANCE_ID`
3. runtime default `MEM0_INSTANCE_ID`
4. auto-discovery through `DescribeDBInstances` only when the region is known and the result narrows safely to exactly one suitable instance

If multiple instances remain, stop and ask the user to reply with `region + instance ID`. When the region is already resolved and read-only discovery is still safe, also offer to list the candidate instances for the user instead of only sending them back to the console.

### 3. AgenticBaseId
Required only for the **open** path.

1. explicit value from the user's sentence
2. runtime default `PG_MEM0_AGENTIC_BASE_ID`
3. runtime default `MEM0_AGENTIC_BASE_ID`

If still missing, stop with a direct acquisition block instead of a generic reminder. Always include the PostgreSQL console entry [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres) so the user can click through immediately. Tell the user the shortest console path `AI 应用 → 选择地域 → AgenticBase`, then explain: if a Base already exists, open its detail page and copy `AgenticBaseId`; if no Base exists yet, click `新建`. Make it explicit that `AgenticBaseId` is not a secret. After obtaining it, the user may either reply in chat with `AgenticBaseId 用 xxx` or place it into runtime environment with `PG_MEM0_AGENTIC_BASE_ID`. Because the current aligned action set does not include a safe AgenticBase inventory API, do not promise to fetch `AgenticBaseId` on the user's behalf in this skill.

### 4. LLMModel
Required only for the **open** path.

1. explicit value from the user's sentence
2. runtime default `PG_MEM0_LLM_MODEL`
3. runtime default `MEM0_LLM_MODEL`
4. built-in default `auto`

Prefer continuing with `auto` when the user does not care about a fixed model. Only pass values that are allowed by the mem0 tool surface. If the chosen value is outside the allowlist and the user explicitly wants a fixed model, stop and include the Hunyuan console entry [腾讯混元控制台](https://console.cloud.tencent.com/hunyuan), then tell the user to check the currently available model list there. If the user has no special preference, explicitly tell them that no extra action is needed and the skill can continue with `auto`.

### 5. EmbeddingApiKey
Required only for the **open** path.

1. runtime default `PG_MEM0_EMBEDDING_API_KEY`
2. runtime default `MEM0_EMBEDDING_API_KEY`
3. runtime default `HUNYUAN_API_KEY`

Treat this slot as runtime-secret only. Do not ask the user to paste it into chat. If none of these variables exists, stop with a direct acquisition block that includes the Hunyuan console entry [腾讯混元控制台](https://console.cloud.tencent.com/hunyuan), the shortest action path `立即接入管理 → API Key 管理 → 创建 API KEY`, and one copyable environment-variable example. Make it explicit that after creation the key must be placed into runtime environment, then the user should simply say `继续开通 mem0` or equivalent instead of pasting the secret back. Do not promise to retrieve `EmbeddingApiKey` on the user's behalf.

## Minimum runtime prerequisites

### Tencent Cloud credentials
Require all of the following before any API call:

- `TENCENTCLOUD_SECRET_ID`
- `TENCENTCLOUD_SECRET_KEY`
- region from the slot-resolution rules above
- optional `TENCENTCLOUD_SESSION_TOKEN`
- if the host stores credentials under custom variable names, map them into these standard `TENCENTCLOUD_*` variables before the skill runs

How to obtain them safely:

1. open [Tencent Cloud API Key Management](https://console.cloud.tencent.com/cam/capi)
2. create a key if no usable key exists yet
3. prefer a least-privilege CAM sub-account instead of a long-lived high-privilege account key
4. save `SecretId` and `SecretKey` immediately; `SecretKey` is usually shown in full only once
5. open [PostgreSQL Console](https://console.cloud.tencent.com/postgres) and confirm the target region such as `ap-guangzhou`

### Open-path runtime defaults
Require the following before `OpenMem0Service`:

- resolved `DBInstanceId`
- resolved `AgenticBaseId`
- resolved `EmbeddingApiKey`
- resolved `LLMModel`

### Close-path runtime defaults
Require the following before `CloseMem0Service`:

- resolved `DBInstanceId`

Recommended runtime template for the open path:

```bash
export TENCENTCLOUD_SECRET_ID="your SecretId"
export TENCENTCLOUD_SECRET_KEY="your SecretKey"
export TENCENTCLOUD_REGION="ap-guangzhou"
export PG_MEM0_INSTANCE_ID="postgres-abc12345"
export PG_MEM0_AGENTIC_BASE_ID="ab-xxxxx"
export PG_MEM0_LLM_MODEL="auto"
export PG_MEM0_EMBEDDING_API_KEY="hunyuan-xxxxx"
```

Important runtime note:

- if you are using CLI, run the `export` commands immediately before the launch command, then verify with `echo $TENCENTCLOUD_SECRET_ID` and `echo $TENCENTCLOUD_REGION`
- if you are using WorkBuddy or another desktop client on macOS, prefer `launchctl setenv ...` plus `launchctl getenv ...`, then fully quit and reopen the client
- if you prefer editing a file for future Terminal sessions, open `~/.zshrc` with `open ~/.zshrc` or `nano ~/.zshrc`, save the exports there, and run `source ~/.zshrc`

## One-click parameter acquisition links

Use this table whenever an **open-path** mem0 slot is missing. Do not replace it with a vague `请自行前往控制台查看` sentence.

| Slot | How to get it quickly | Official entry |
|---|---|---|
| `Region` | 打开 PostgreSQL 控制台，看右上角地域选择器；如果已有实例，也可以直接看实例所属地域。如果当前凭证可用，skill 也可以先代查 PostgreSQL 支持地域 | [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres) |
| `AgenticBaseId` | 打开 PostgreSQL 控制台，进入 `AI 应用 → AgenticBase`；已有 Base 时进详情复制 `AgenticBaseId`，没有就点 `新建` | [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres) |
| `EmbeddingApiKey` | 打开混元控制台，进入 `立即接入管理 → API Key 管理`，点击 `创建 API KEY` | [腾讯混元控制台](https://console.cloud.tencent.com/hunyuan) |
| `LLMModel` | 不确定时直接用默认 `auto`；只有想固定模型时才去混元控制台确认当前可接入模型 | [腾讯混元控制台](https://console.cloud.tencent.com/hunyuan) |

## Missing-parameter reply template

When a mem0 **open** request is blocked only because open-path required slots are missing, the reply must close the loop instead of only listing links. The answer should contain all four parts below:

1. what is missing right now
2. where to obtain each value
3. how to place the value into runtime environment for the current client type
4. exactly what the user can say next so the skill can continue

Prefer a direct reply like this:

```text
继续开通 mem0 之前，当前还缺 2 个运行时参数。你按下面补齐后，直接回复“继续开通 mem0”即可；如果 `AgenticBaseId` 想直接告诉我，也可以直接回在聊天里。

1. AgenticBaseId（非密钥，可以回在聊天里，也可以写到运行时环境）
   - 控制台入口：PostgreSQL 控制台 https://console.cloud.tencent.com/postgres
   - 最短路径：AI 应用 → 选择地域 → AgenticBase
   - 如果已有 Base：进入详情复制 `AgenticBaseId`
   - 如果还没有 Base：点击 `新建`
   - 你有两种补齐方式，任选一种：
     - 方式 A：直接回复我：`AgenticBaseId 用 agenticbase-xxxxx`
     - 方式 B：配到运行时环境：`PG_MEM0_AGENTIC_BASE_ID=agenticbase-xxxxx`

2. EmbeddingApiKey（敏感值，只能放到运行时环境，不要发到聊天里）
   - 控制台入口：腾讯混元控制台 https://console.cloud.tencent.com/hunyuan
   - 最短路径：立即接入管理 → API Key 管理 → 创建 API KEY
   - 创建后放到运行时环境：`PG_MEM0_EMBEDDING_API_KEY=你的混元 API KEY`

3. LLMModel
   - 如无特殊要求，可直接使用默认值 `auto`
   - 只有你想固定模型时，才需要额外告诉我 `LLMModel 用 xxx`

如果你当前是在终端 / CLI 里执行，可直接先设置：
export PG_MEM0_AGENTIC_BASE_ID="agenticbase-xxxxx"
export PG_MEM0_EMBEDDING_API_KEY="你的混元 API KEY"
export PG_MEM0_LLM_MODEL="auto"

如果你当前是在 macOS 桌面版 WorkBuddy 里执行，优先这样设置，然后**完全退出并重新打开客户端**：
launchctl setenv PG_MEM0_AGENTIC_BASE_ID "agenticbase-xxxxx"
launchctl setenv PG_MEM0_EMBEDDING_API_KEY "你的混元 API KEY"
launchctl setenv PG_MEM0_LLM_MODEL "auto"

配好后你可以直接回复以下任一一句：
- `继续开通 mem0`
- `AgenticBaseId 用 agenticbase-xxxxx，继续开通 mem0`
- `我已经把 mem0 运行时参数配好了，继续给这个实例开通`
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
If discovery returns zero candidates or more than one reasonable candidate, stop and send one direct clarification line, for example:

```text
我可以继续处理 mem0 服务，但当前目标实例还不唯一。请直接回复：ap-guangzhou postgres-abc12345
```

## Read-only preflight workflow

Run the preflight in this order.

### Step 1: instance existence and scope
- use `DescribeDBInstances` only if instance discovery is needed
- otherwise go straight to `DescribeDBInstanceAttribute`

### Step 2: instance suitability
Use `DescribeDBInstanceAttribute` to confirm at least the following when the fields are available in the current API shape:

- instance exists in the resolved region
- instance is a primary instance rather than a readonly child
- instance is in a usable lifecycle state such as running
- any returned version or kernel facts do not obviously contradict mem0 service control prerequisites

If the current API shape does not expose a definitive kernel field, continue and let the server-side write action perform the final validation. Report the exact API error if the server rejects the request.

### Step 3: current mem0 state
Use `DescribeMem0Service` to classify the current mem0 state according to the requested action:

For an **open** request:
1. **ready** — mem0 is already usable; return endpoint and stop
2. **transitioning** — mem0 is being created or deleted; return current blocker and stop
3. **not opened yet** — continue to `OpenMem0Service`

For a **close** request:
1. **already closed** — mem0 is already closed or not opened; return current state and stop
2. **transitioning** — mem0 is being created or deleted; return current blocker and stop
3. **closable** — mem0 is currently usable or otherwise open; continue to `CloseMem0Service`

### Optional Step 4: task evidence
Use `DescribeTasks` only when the instance looks busy or a current task may explain a blocker.

## Write-execution rule

Treat the user's original sentence as sufficient approval only when the matching action conditions are satisfied.

### Open path
1. the sentence explicitly asks to open, deploy, enable, or bring up mem0
2. region and target instance are unambiguous
3. `AgenticBaseId`, `LLMModel`, and `EmbeddingApiKey` are all resolved
4. read-only preflight found no material blocker

### Close path
1. the sentence explicitly asks to close, disable, stop, or take down mem0
2. region and target instance are unambiguous
3. read-only preflight shows the service is currently closable
4. read-only preflight found no material blocker

If any condition fails, do not execute the write action.

## Call shapes

### OpenMem0Service

```json
{
  "DBInstanceId": "postgres-abc12345",
  "AgenticBaseId": "ab-xxxxx",
  "LLMModel": "auto",
  "EmbeddingApiKey": "<runtime secret>"
}
```

### CloseMem0Service

```json
{
  "DBInstanceId": "postgres-abc12345"
}
```

Do not add unrelated fields. Do not echo the raw `EmbeddingApiKey` in the result.

## Polling policy after write

After a successful `OpenMem0Service` or `CloseMem0Service` call:

- poll `DescribeMem0Service` every 10 seconds
- stop after 18 attempts at most
- for **open**, stop earlier if a ready state plus endpoint appears
- for **close**, stop earlier if a closed / unavailable state appears and the service is no longer usable
- stop earlier on a terminal API error

If the wait budget is exhausted and the service is still applying the change, return a truthful partial result that includes the latest observed status and says whether the platform still appears to be opening or closing the service.

## Final output schema

### 1. Target scope
- region
- instance ID

### 2. Requested action
- `open` or `close`

### 3. Resolved slots
- include only the slots actually used for the requested action
- source of each slot: user sentence, runtime default, or built-in default

### 4. Preflight facts
- instance existence
- suitability facts gathered from read-only actions
- previous mem0 state before the write decision

### 5. Executed actions
- read-only actions used
- whether `OpenMem0Service` or `CloseMem0Service` was executed
- polling attempts and latest observed state

### 6. Final result
- final mem0 status
- endpoint such as `InnerAddress` on open success
- closed-state confirmation on close success
- one minimal next-step example

## Guardrails

- Never read secrets from repository files or ask the user to paste them into chat.
- Never call `OpenMem0Service` or `CloseMem0Service` twice for the same request.
- Never auto-call the opposite direction action as a rollback or retry strategy.
- Never claim open success without both a ready state and a usable endpoint.
- Never claim close success while the service still looks usable.
- Keep every summary tightly scoped to the one target instance.
