## Description:

Monitors LLM usage and costs across cloud and local providers, with balance checks, scheduled alerts, cross-session tracking, and cost-saving recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelegele](https://clawhub.ai/user/kelegele)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use it to estimate token costs, check supported provider balances, track usage across sessions, and generate alerts and cost-saving guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that token estimation may send supplied text to an external provider despite local-only assurances; script inspection was incomplete.

Mitigation: Review provider and token-estimation behavior before use, and avoid sending sensitive text until its data handling is understood.

Risk: Passing an API key with --api-key can expose it in shell history or process listings.

Mitigation: Use the provider's environment variable for routine use and reserve --api-key for temporary debugging.

## Reference(s):

- [Token Manager on ClawHub](https://clawhub.ai/kelegele/skills/token-manager)
- [Moonshot pricing documentation](https://platform.kimi.com/docs/pricing/chat)
- [DeepSeek pricing documentation](https://api-docs.deepseek.com/zh-cn/quick_start/pricing)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON reports and alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes usage and cost summaries, balance alerts, and recommendations; costs are grouped by currency.]

## Skill Version(s):

1.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
