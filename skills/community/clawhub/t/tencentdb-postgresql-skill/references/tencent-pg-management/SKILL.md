---
name: tencent-pg-management
description: Route one-sentence Tencent Cloud PostgreSQL management-plane requests to the smallest direct OpenAPI action set for instance overview, instance changes, backup and recovery, and access security. Infer the real task goal from natural language, extract target slots, gather read-only evidence first, and require explicit confirmation before any write, fee-impacting, or high-risk operation.
description_zh: PostgreSQL 管控面统一入口
description_en: PostgreSQL management-plane router
disable: false
agent_created: true
---

# tencent-pg-management

## When to use
- Need one natural-language entry for TencentDB for PostgreSQL management-plane tasks instead of manually choosing separate management skills.
- Need the skill to infer whether the real goal is instance overview, instance change, backup recovery, or access security.
- Need safe management execution with slot extraction, smallest-action routing, read-only evidence first, and explicit confirmation gates.

## Steps
1. Determine the primary management goal from the user's sentence before any API call. Prioritize the requested outcome over surface keywords. Route into exactly one primary lane: `overview`, `instance-change`, `backup-recovery`, or `access-security`.
2. Extract the minimum slot set for the routed lane. Always identify region, target scope, and task goal. When present, also capture optional objects such as account, database, target spec, recovery window, security group, public-access intent, or SSL.
3. If the request clearly belongs to operations-plane inspection or operations-plane slow-SQL observation, stop and tell the user to continue with `tencent-pg-inspection` or `tencent-pg-slowquery-diagnosis` instead of forcing the request through this skill.
4. Confirm target scope before execution. For existing-instance requests, require region and instance ID. For new-instance creation requests, require region plus the minimum creation fields that matter for the requested action. If required scope is missing, immediately reply with a direct message (no interactive prompt or choice menu) that includes: (a) the console link https://console.cloud.tencent.com/postgres where the user can find the region and instance ID, (b) one concrete reply example such as `ap-guangzhou postgres-abc12345`, and (c) when the missing field is non-secret and current credentials are already available, one agent-assisted option such as `如果你不想自己查，我也可以先帮你列支持地域 / 列该地域下的实例`.
5. Normalize region input before any OpenAPI call by following `@references/common/region_normalization.md`. Accept standard region codes such as `ap-guangzhou` and common aliases such as `广州`, `上海`, `成都`, and `北京`. If the input cannot be normalized safely, stop and use the `invalid-region` template in `@references/common/error_handling.md`, including the official region links plus the option to query supported regions on the user's behalf when the current path allows it.
6. Check runtime prerequisites using a foolproof order. Use standard Tencent Cloud runtime variables only: `TENCENTCLOUD_SECRET_ID`, `TENCENTCLOUD_SECRET_KEY`, `TENCENTCLOUD_REGION`, and optional `TENCENTCLOUD_SESSION_TOKEN`. If the host keeps credentials under custom names, map them into these standard variables before the skill runs. If required values are missing, stop and use the `missing-credentials` template in `@references/common/error_handling.md`, including one copyable example plus the official API key and region links. For non-secret fields such as region, also offer an agent-assisted lookup path when current credentials already exist; never promise to retrieve secrets on the user's behalf.
7. Build a minimal action plan by following `@references/api_reference.md`. Split the plan into a read-only evidence phase and an optional write or high-risk phase. Never include unrelated actions just because they are available in the same lane.
8. Execute only the read-only evidence phase first. Summarize current facts, blockers, compatibility notes, and whether the requested outcome appears feasible.
9. For the `backup-recovery` lane, if the current request is read-only evidence such as backup overview or recovery-time-window lookup, still add an explicit downstream risk reminder. Clearly tell the user that follow-up actions such as restore / clone recovery, backup download-link retrieval, or manual backup creation are not being executed now, must stay in `待确认`, and may carry data overwrite risk, access exposure risk, or fee impact depending on the action.
10. If the next step is a write, fee-impacting, security-impacting, or other high-risk action, do not execute it yet. Switch to the confirmation-waiting response shape in `@references/api_reference.md`. Explicitly say the skill is waiting, using wording such as `等你确认` or `确认后我再继续`, and state the exact pending action, why it matters, the expected impact, prerequisites, and the main risk before stopping. Keep the action status as `待确认` until the user explicitly approves it.
11. If the sentence spans multiple management lanes, split the work into staged results. Keep one primary lane per execution step and never batch multiple write actions behind one implicit approval.
12. Summarize as a structured management result: target scope, recognized intent and routing reason, extracted slots, APIs inspected, current facts, pending or executed actions, risks, and the safest next step.

## Pitfalls
- Do not classify by keyword alone when the user's actual goal points to a different management lane.
- Do not skip slot extraction for account, database, target spec, recovery window, security group, or other lane-specific objects that materially affect API choice.
- Do not execute any write, fee-impacting, or high-risk action before collecting read-only evidence.
- Do not stop a confirmation-required branch with vague wording such as `要继续吗` or `是否处理`; explicitly say `等你确认` or equivalent, and explain the pending action's meaning and main risk.
- Do not return a recovery-time-window or backup-readiness result without also warning that restore / clone / backup download-link retrieval remain `待确认` high-risk follow-up actions.
- Do not mix unrelated management lanes into one uncontrolled execution flow. If the request spans multiple lanes, split it into staged results and keep each write action behind its own confirmation gate.
- Do not route operations-plane inspection or slow-query requests into this skill.
- Do not expose passwords, secrets, or backup download links in summaries.

## Verification
- Include region, target scope, recognized lane, and routing reason in the final answer.
- State the extracted slots that materially affected API selection.
- State which OpenAPI actions were inspected and why they matched the detected intent.
- Show read-only evidence before any action recommendation or execution.
- For recovery-time-window or backup-readiness queries, explicitly remind the user that follow-up restore / clone / backup download actions are not being executed now and remain `待确认` because they are high-risk, sensitive, or fee-impacting.
- When the next step requires confirmation, explicitly say `等你确认` or an equally direct waiting phrase, state what action will happen after confirmation, explain why that action matters, and summarize the main risk or impact.
- Clearly mark every write, fee-impacting, or high-risk action as `待确认` until the user explicitly approves it.
