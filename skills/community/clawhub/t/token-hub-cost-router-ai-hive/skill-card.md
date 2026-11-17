## Description:

Token Hub 成本路由中心｜AI-HIVE helps Token Hub, model-routing, API aggregation, and high-volume content teams turn model requirements, quality thresholds, budgets, timelines, and failure tolerance into cost-first, speed-first, and success-rate-first routing plans with fallback workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content production teams use this skill to plan AI-HIVE model routing, API aggregation, media-generation jobs, cost and latency tradeoffs, task queues, and fallback handling. The skill is especially oriented toward e-commerce, advertising, marketing, social, short-video, and product-content workflows that need reviewable plans before potentially paid generation calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent API credentials and a configurable base URL could expose credentials to an unintended endpoint.

Mitigation: Use a limited AI_HIVE_API_KEY, keep the base URL at the documented AI-HIVE endpoint, avoid inherited AI_HIVE_BASE_URL values, and review local configuration before generation.

Risk: AI-HIVE generation, polling, and downloads may create cost or file-handling risk if run without review.

Mitigation: Confirm prompts, routing mode, budget, and output paths before paid calls; start with a small sample before expanding batches.

Risk: Commercial content workflows can produce unsupported claims or over-close copies of protected reference material.

Mitigation: Require authorized source material and source-backed claims, avoid impersonation or unverifiable endorsements, and use only abstract structure guidance when rights are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/token-hub-cost-router-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with runnable command examples and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce routing plans, prompts, task records, AI-HIVE API calls, local blueprint JSON, and media-processing commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
