---
name: tencent-pg-mem0-deploy
description: Open or close TencentDB for PostgreSQL mem0 service from one natural-language sentence. Resolve the target instance and mem0 slots, read secrets from runtime environment only, run read-only preflight with direct OpenAPI actions, execute OpenMem0Service or CloseMem0Service when the request is explicit, and keep polling until the service becomes ready to use or fully closed.
description_zh: PostgreSQL 一句话开通 / 关闭 mem0 服务
description_en: One-sentence mem0 service open / close for PostgreSQL
disable: false
agent_created: true
---

# tencent-pg-mem0-deploy

## When to use
- Need one natural-language entry to **open or close** mem0 for an existing Tencent Cloud PostgreSQL instance and get back the final service state.
- Need the skill to auto-fill non-secret defaults from runtime environment, reduce follow-up questions, and finish the full mem0 open / close flow in one pass.
- Need a specialized mem0 service-control workflow instead of the broader `tencent-pg-management` router.

## Steps
1. Detect explicit mem0 intent first. Accept open verbs such as `开通`、`部署`、`启用`、`拉起`、`打开`, and close verbs such as `关闭`、`停用`、`下线`、`关掉`, when they clearly target `mem0` or `长期记忆服务`. If the request is only about explanation, comparison, or generic status lookup, stop and continue with normal answering or `tencent-pg-management` instead of forcing this skill.
2. Extract the target action and slot set. Always resolve region and `DBInstanceId`. For the **open** path, also resolve `AgenticBaseId` and optional `LLMModel` by following `@references/api_reference.md`. Prefer the built-in `auto` model default when the user does not care about a specific model. Never source secrets from repository files, chat history, screenshots, or user-pasted plaintext unless the user explicitly states the value is already present in runtime environment.
3. Normalize region before any API call by following `@references/common/region_normalization.md`. Accept standard region codes and supported Chinese aliases. If the region cannot be normalized safely, stop and use the `invalid-region` template in `@references/common/error_handling.md`.
4. Check runtime prerequisites in a strict order by following `@references/api_reference.md`: Tencent Cloud credentials first, action-specific runtime defaults second. For the **open** path, missing open-only slots must stop the workflow with direct official links, one copyable runtime-configuration example, client-aware setup guidance when applicable, and one explicit follow-up sentence the user can send to continue. For the **close** path, only keep the minimal required runtime scope and never ask the user for open-only parameters such as `AgenticBaseId` or `EmbeddingApiKey`.
5. Resolve the target instance with the smallest safe path. Prefer explicit `DBInstanceId`. Otherwise use a runtime default if present. Only fall back to `DescribeDBInstances` discovery when region is known and the result can be narrowed to exactly one suitable instance. If multiple candidates remain, stop and ask for `region + instance ID` in one direct sentence.
6. Run read-only preflight first by following `@references/api_reference.md`. Use only the aligned read-only actions for this skill. Confirm the instance exists, is suitable for mem0 service control, and capture the current mem0 state before any write call.
7. Interpret current mem0 state based on the requested action. If the user wants to **open** mem0 and the service is already ready, return the current endpoint and usage facts instead of reopening. If the user wants to **close** mem0 and the service is already closed or not opened, return the current state instead of calling `CloseMem0Service`. If mem0 is in a transition state such as creating or deleting, stop and report the current blocker rather than stacking another write request.
8. Treat a fully specified imperative open / close sentence as the user's explicit approval for this dedicated skill. When the user clearly asks to open or close mem0 and the target scope is unambiguous, execute the matching write action directly without adding a second confirmation turn. If the request is ambiguous or preflight reveals a material blocker, stop and explain the blocker first.
9. Execute the matching write action from `@references/api_reference.md`: use `OpenMem0Service` for open requests, and `CloseMem0Service` for close requests. Read `EmbeddingApiKey` from runtime environment only, and only on the open path.
10. Poll `DescribeMem0Service` with the bounded retry policy defined in `@references/api_reference.md` until the service reaches the expected terminal state for the requested action, a terminal API error appears, or the wait budget is exhausted. Never call the opposite direction action automatically as a recovery step.
11. Summarize as a final service-control result: target scope, requested action, resolved slots and their sources, preflight facts, executed actions, current mem0 status, usable endpoint on open success or closed-state confirmation on close success, and the next copyable step.

## Pitfalls
- Do not ask the user to paste `EmbeddingApiKey` or any other secret into the conversation.
- Do not tell the user only `自己去控制台找`; always provide the direct official console / product-site entry links plus the shortest click path documented in `@references/api_reference.md` when a required mem0 slot is missing, and add an agent-assisted lookup option whenever the missing slot is non-secret and the current toolchain can fetch it safely.
- Do not run `OpenMem0Service` or `CloseMem0Service` on an ambiguous target or when multiple candidate instances remain.
- Do not reopen an already running mem0 service, and do not close a service that is already confirmed closed.
- Do not silently change `AgenticBaseId` or `LLMModel` for an existing running mem0 service.
- Do not auto-call `CloseMem0Service` after an open failure, or `OpenMem0Service` after a close failure.
- Do not keep polling forever; follow the bounded retry policy and return the current provisioning state when the platform is still applying the change.

## Verification
- Include region, instance ID, requested action, and final mem0 status in the final answer.
- State which slots came from the user and which came from runtime defaults.
- State which read-only actions were used before the write action.
- If opening succeeds, include `InnerAddress` or equivalent endpoint plus one minimal next-step example.
- If closing succeeds, clearly state that mem0 is now closed or no longer usable, and mention any latest observed status returned by `DescribeMem0Service`.
- If execution is blocked by missing runtime values, clearly state the blocker, provide the official clickable acquisition links, and include the exact environment-variable fix needed next.
