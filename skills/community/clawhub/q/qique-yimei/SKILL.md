---
name: 企雀医美系统-AI助手
description: Use this skill when an agent needs to answer or plan operations for QiQue business requests in pure text protocol mode (no local executable dependency). Trigger for customer/profile lookup, wallet change records, appointments, order and goods queries, SMS/card sending, delivery/verification, or create/update/cancel workflows. The skill provides a strict method catalog, credential contract, and safe read/write conversation workflow.
---

# QiQue Text Protocol

## Overview

Use this skill in text-only mode.
Do not require local PHP/Node execution. Instead, produce strict structured text:

1. Method decision
2. Normalized params JSON
3. Missing-required fields
4. Safety check (read/write)
5. User-facing next action

## Prerequisites

1. Load credentials from `config/qique.config.json` (or remembered session state).
2. Keep credentials persistent between turns.
3. Never expose sensitive variables in any user-facing text.

Required config keys:

- `app_id`
- `app_secret`
- `distribution_app_id`
- `distribution_app_secret`

## Workflow (Text Only)

0. Before any business execution, check whether `app_id` and `app_secret` are already stored.
   - If either is missing, immediately reply with:
   - `请提供你的企雀后台的 app_id 和 app_secret （这两个值可以在企雀后台的「系统管理」->「企雀API」中直接获取到），提供后我马上帮你完成操作。`
   - Wait for user to provide credentials before continuing.
1. Route Chinese business intent to method using `references/intent-routing.md`.
2. Review `missing_required` and fill missing parameters.
3. Decide operation type:

- Read operation: return planned method + params and continue.
- Write operation: require explicit user confirmation before producing final execution plan.

4. Return structured text output.
5. Interpret `errNum` when present:

- `errNum = 0`: success
- non-zero: business failure; include `errMsg` (if returned) and request context for retry.

## Output Protocol

Use this exact output frame:

```json
{
  "route": {
    "method": "<method_name>",
    "operation": "read|write",
    "confidence": 0.0,
    "reason": "<why>"
  },
  "params": {},
  "missing_required": [],
  "can_execute": true,
  "requires_write_confirmation": false,
  "next_action": "<what user should provide/confirm next>"
}
```

For write operations, add this line before final plan:

```text
该操作为写操作，请确认是否执行（回复：确认执行 / 取消）
```

## Execution Rules

1. Never invent parameters not in method signature.
2. Never continue write-operation plan without explicit user confirmation.
3. For ambiguous identity fields (`cusId` vs `telnum`, `billId` vs `useCode`), prefer the ID field when user provides both.
4. Echo the final method and params to the user before write execution.
5. Return response JSON as-is, then add a short interpretation.
6. Credential policy:
   - First-time use without stored `app_id/app_secret`: must ask with the exact reminder sentence above.
   - After user provides new `app_id/app_secret`: persist to memory/config text state and reuse later.
   - If user provides newer values later: overwrite the stored values.
   - Never expose `distribution_app_id` or `distribution_app_secret` values to customers in any response.

## Resources

- Method catalog and operation class: `references/methods.md`
- Intent routing behavior: `references/intent-routing.md`
- Local config template: `config/qique.config.example.json`
