---
name: tencent-pg-slowquery-diagnosis
description: Query operations-plane slow SQL facts for Tencent Cloud PostgreSQL by calling direct read-only OpenAPI actions. This operations-plane skill currently returns basic slow SQL facts only and does not perform cause analysis or tuning recommendations.
description_zh: PostgreSQL 运维面慢 SQL 查询
description_en: PostgreSQL operations slow SQL lookup
disable: false
agent_created: true
---

# tencent-pg-slowquery-diagnosis

## When to use
- Need to view operations-plane slow SQL information for one PostgreSQL instance.
- Need a fixed-scope slow SQL observation workflow for a specific time window.
- Need direct slow-query facts rather than diagnosis, root-cause analysis, or tuning guidance.

## Steps
1. Confirm the target scope first: region, instance ID, and optional time window. Optional filters may include database name or SQL fingerprint. If region or instance ID is missing, stop and use the `missing-target-scope` template in `@references/common/error_handling.md`.
2. Normalize region input by following `@references/common/region_normalization.md`. If the input cannot be normalized safely, stop and use the `invalid-region` template.
3. Check runtime prerequisites. Read credentials only from runtime environment variables. If required values are missing, stop and use the `missing-credentials` template.
4. Use only the read-only slow-query actions listed in `@references/api_reference.md`.
5. Return only basic slow SQL facts such as SQL text, database, user, client, duration, count, total cost, and execution time. Do not expand into management-plane actions or broader troubleshooting workflows.
6. Summarize the result in a fixed structure: query scope and slow SQL basic list.

## Pitfalls
- Do not rank likely causes.
- Do not infer root cause from slow-query records.
- Do not recommend tuning, parameter changes, scaling, or topology changes.
- Do not pull unrelated modules such as backup, network, SSL, or error-log context unless the user explicitly asks for another skill.

## Verification
- Include region, instance ID, time window, sorting basis, and a short query summary in the final answer.
- State which read-only slow-query actions were used.
- Organize the reply as a report, not as a loose row dump.
- Show only fields that come directly from the API response.
- If a field is unavailable, summarized-only, or missing, say so explicitly in the report body.
