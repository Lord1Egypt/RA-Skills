---
name: tencent-pg-inspection
description: Run an operations-plane PostgreSQL inspection by querying Tencent Cloud monitor metrics. This operations-plane skill currently returns basic inspection facts only and does not perform remediation, management actions, or expanded diagnosis.
description_zh: PostgreSQL 运维面巡检
description_en: PostgreSQL operations inspection
disable: false
agent_created: true
---

# tencent-pg-inspection

## When to use
- Need an operations-plane routine inspection result for one PostgreSQL instance.
- Need to check basic resource and runtime indicators for one instance.
- Need a fixed-scope operations-plane workflow that currently stays read-only.

## Steps
1. Confirm the target scope first: region, instance ID, and optional time window. If the region, instance ID, or both are missing, stop and use the `missing-target-scope` template in `@references/common/error_handling.md`.
2. Normalize region input by following `@references/common/region_normalization.md`. If the input cannot be normalized safely, stop and use the `invalid-region` template.
3. Check runtime prerequisites. Read credentials only from runtime environment variables. If required values are missing, stop and use the `missing-credentials` template.
4. Use the monitor actions listed in `@references/api_reference.md`. Start with `DescribeBaseMetrics` to confirm which PostgreSQL metrics are supported for the target product or instance.
5. Pull only the fixed basic inspection metrics that are available for the target instance. Do not expand into backup, parameter, account, network, SSL, slow-query, remediation, or management-plane workflows.
6. Summarize the result in a fixed structure: inspection target, metric results, and simple risk prompts.

## Pitfalls
- Do not invent metric names that are not returned by the monitor API.
- Do not infer root causes from metric values.
- Do not automatically expand into troubleshooting or management-plane change actions.
- Do not mix values from different regions, instances, or time windows.

## Verification
- Include region, instance ID, time window, and an overall inspection status in the final answer.
- State which monitor actions were used.
- Organize the reply as a report, not as a loose metric dump.
- Show only directly returned metric facts plus conservative observation labels such as `normal`, `attention`, `abnormal`, or `manual review needed`.
- If a metric is unsupported, unavailable, or has no data, say so explicitly in the report body.
