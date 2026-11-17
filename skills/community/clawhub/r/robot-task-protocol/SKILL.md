---
name: robot-task-protocol
description: >-
  Dispatch paid tasks to physical robots via the Robot Task Protocol (RTP)
  on the Spraay x402 gateway — with payment held in escrow until the robot
  completes the work. Also register your own robot to earn from tasks, free.
  Use when the user asks to find robots, dispatch a robot task, hire a robot,
  pay a robot for work, check a robot task status, or register/update/remove
  their own robot on the RTP network.
version: 1.0.2
homepage: https://spraay.app
metadata:
  openclaw:
    emoji: "💧"
    requires:
      bins:
        - curl
        - jq
      env:
        - SPRAAY_GATEWAY_URL
    primaryEnv: SPRAAY_GATEWAY_URL
    envVars:
      - name: SPRAAY_GATEWAY_URL
        required: true
        description: >-
          Spraay x402 gateway base URL (https://gateway.spraay.app).
          All API calls go exclusively to this endpoint.
---

# Robot Task Protocol 💧

Dispatch tasks to physical robots and pay per task — with escrow-protected
payment — using the open Robot Task Protocol (RTP) via the Spraay x402
gateway. Robot operators can register and earn for free.

All requests in this skill go exclusively to the user's configured
`SPRAAY_GATEWAY_URL`. No data is sent to any other external endpoint.

## Important Warnings

**Dispatched tasks command real hardware.** A dispatched task may cause a
physical robot to move, actuate, or perform work in the real world. Always
confirm the following with the user before dispatching:

- The target robot and task parameters are correct
- The task is safe to execute in the robot's environment
- The user understands the task fee and x402 micropayment costs

**Built-in escrow protection.** Task payment is held in escrow by the
gateway and released to the robot operator only on reported completion —
the buyer is not paying blind.

**Operator actions are permanent.** Updating a robot's payment address,
pricing, or status takes effect immediately. Deregistering a robot removes
it from the network — it will no longer appear in discovery or accept tasks
until re-registered. Always confirm the robot ID and intended change with
the user before executing any operator mutation.

## Setup

The gateway URL must be set in your environment or `openclaw.json`:

```
SPRAAY_GATEWAY_URL=https://gateway.spraay.app
```

No standalone API key is needed for buyer-side calls — payments are made
per-request via the x402 HTTP payment protocol (HTTP 402 → pay → retry).
An x402-compatible wallet (Coinbase CDP or similar) handles this
automatically.

## Authorization model

**Buyer-side endpoints** (list, profile, dispatch, status) are authorized
by x402 payment — if you can pay, you can call.

**Operator-side endpoints** (register, update, complete, deregister) are
mutation operations that modify robots and release escrow. The gateway
enforces ownership server-side: each robot is bound to the identity that
registered it, and each task is bound to its assigned robot. The curl
examples below are simplified for readability — the gateway rejects
mutation requests that do not come from the authorized owner.

> **Note for skill consumers:** this skill documents the API surface. It
> does not bypass or weaken whatever authorization the gateway enforces.
> If the gateway's ownership enforcement changes or the skill examples
> diverge from the live API's auth requirements, follow the gateway's
> requirements. When in doubt, consult the
> [RTP spec](https://github.com/plagtech/rtp-spec).

## What is RTP?

The Robot Task Protocol is an open standard for describing, dispatching, and
paying for robot tasks. Spec and SDKs:

- Spec: https://github.com/plagtech/rtp-spec
- SDKs: https://github.com/plagtech/rtp-sdk (TypeScript),
  https://github.com/plagtech/rtp-python-sdk (Python)

## Buyer Workflows (hiring robots)

### Discover Robots — $0.005

Find registered robots filtered by capability, chain, price, or status.
Always list first to get valid robot IDs before dispatching.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/robots/list?capability=move"
```

### Robot Profile — $0.002

Full capability profile of one robot: supported tasks, pricing, reputation,
history, location.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/robots/profile?id=ROBOT_ID"
```

### Dispatch a Task — $0.05 + task fee

Dispatches a paid task to a robot. The x402 payment is held in escrow and
released to the operator on completion.

**Always confirm robot, task, parameters, and fee with the user before
dispatching.**

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/v1/robots/task" \
  -H "Content-Type: application/json" \
  -d '{
    "robot_id": "ROBOT_ID",
    "task": {
      "type": "move",
      "params": {"angle": 90}
    }
  }'
```

If you receive HTTP 402, the response body contains payment instructions. Pay
the facilitator, then retry with the `X-PAYMENT` header containing the proof.

Save the task ID from the response for status polling.

### Poll Task Status — $0.002

Status of an in-flight task (pending, in-progress, complete) and results.

```bash
curl "$SPRAAY_GATEWAY_URL/api/v1/robots/status?id=TASK_ID"
```

### Recommended Buyer Flow

1. List robots to find a capability match.
2. Fetch the robot's profile to confirm pricing and reputation.
3. Confirm robot, task, and fee with the user.
4. Dispatch and save the task ID.
5. Poll status until complete — payment auto-releases on completion.

## Operator Workflows (earning with your robot) — FREE

Registering and managing a robot on the RTP network costs nothing. Operators
get paid per completed task via escrow release.

> **All operator mutations require user confirmation.** Before calling
> register, update, complete, or deregister, confirm the robot ID,
> intended change, and consequences with the user. These actions take
> effect immediately on the gateway.

### Register a Robot — FREE

Required fields: `name`, `capabilities`, `payment_address`, `connection`.
Optional: `description`, `price_per_task`, `currency`, `chain`, `tags`,
`metadata`. Connection types: `webhook`, `xmtp`, `wifi`, `websocket`.

Save the returned `robot_id` — it is needed for all subsequent management
calls and is bound to your operator identity.

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/v1/robots/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "WarehouseBot-01",
    "capabilities": ["pick", "place", "scan"],
    "price_per_task": "0.05",
    "payment_address": "0xYOUR...WALLET",
    "connection": {
      "type": "webhook",
      "webhookUrl": "https://yourserver.com/rtp/task"
    }
  }'
```

### Report Task Completion — FREE (called by the robot)

Reports a task done and triggers escrow release to the operator wallet.
Only the robot assigned to the task can report completion.

Required: `task_id` and `status` (`COMPLETED` or `FAILED`). Optional:
`result`.

**Confirm the task ID and status with the user before reporting.** A
`COMPLETED` report triggers immediate escrow release.

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/v1/robots/complete" \
  -H "Content-Type: application/json" \
  -d '{"task_id": "TASK_ID", "status": "COMPLETED", "result": {"items": 3}}'
```

### Update a Robot — FREE

Requires `robot_id`. Updatable: `name`, `description`, `capabilities`,
`price_per_task`, `currency`, `chain`, `payment_address`, `connection`,
`tags`, `status`, `metadata`.

**Confirm changes with the user before updating**, especially
`payment_address` (changes where earnings are sent) and `status` (can
take the robot offline). Changes take effect immediately.

```bash
curl -X PATCH "$SPRAAY_GATEWAY_URL/api/v1/robots/update" \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "ROBOT_ID", "price_per_task": "0.30", "status": "available"}'
```

### Deregister a Robot — FREE

> **Destructive action.** Deregistration removes the robot from the RTP
> network immediately. It will no longer appear in discovery results or
> accept new tasks. Any in-flight tasks may be affected. The robot must
> be re-registered from scratch to rejoin. Always confirm the robot ID
> with the user and verify there are no active tasks before proceeding.

```bash
curl -X POST "$SPRAAY_GATEWAY_URL/api/v1/robots/deregister" \
  -H "Content-Type: application/json" \
  -d '{"robot_id": "ROBOT_ID"}'
```

## Free Endpoints

These require no x402 payment (but are subject to gateway ownership
enforcement for mutation operations):

- `POST /api/v1/robots/register` — Register a robot
- `POST /api/v1/robots/complete` — Report task completion (robot-side, authorized to assigned robot only)
- `PATCH /api/v1/robots/update` — Update robot profile/pricing (authorized to registering owner only)
- `POST /api/v1/robots/deregister` — Remove a robot (authorized to registering owner only)
- `GET /health` — Gateway health check

## x402 Payment Flow

1. Call any paid endpoint.
2. Receive HTTP 402 with payment details (`accepts` array with amount,
   asset, and payment address).
3. Agent wallet sends the micropayment.
4. Retry the request with the `X-PAYMENT` proof header.
5. Receive the response.

Buyer-side costs: list $0.005, profile $0.002, dispatch $0.05 + task fee,
status $0.002 — in USDC on Base. Task fees vary per robot and are shown in
listings and profiles.

## Error Handling

- `402` — Payment required. Follow instructions in response body.
- `400` — Bad request. Validate the task payload against the robot's
  capability profile.
- `401` / `403` — Unauthorized. The caller does not own the target robot
  or task. Verify the correct operator identity is being used.
- `404` — Robot or task ID not found. Re-list robots.
- `500` — Server error. Retry after a moment.

## Tips

- Always confirm with the user before dispatching to hardware.
- Fetch the robot profile before dispatch to validate task type and price.
- Dispatch payment is escrow-protected — released only on completion.
- Operators: registration is free; you earn per completed task.
- Pair with `spraay-trust` to check an operator's trust score before
  high-value tasks.

## Links

- RTP Spec: https://github.com/plagtech/rtp-spec
- App: https://spraay.app
- Docs: https://docs.spraay.app
- GitHub: https://github.com/plagtech
