## Description:

Avalanche Analytics helps agents analyze the Avalanche ecosystem, including subnets, DeFi protocols, project evaluation, monitoring, and validator yield estimates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to get Avalanche ecosystem overviews, compare subnets and DeFi protocols, evaluate projects, monitor AVAX-related metrics, and estimate validator staking returns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid-use enforcement is under-disclosed, and wallet identifiers may be sent to SkillPay for payment verification.

Mitigation: Clearly disclose the payment check before use and avoid sending wallet identifiers unless payment verification is required.

Risk: A SkillPay API key is exposed in the artifact metadata and payment module.

Mitigation: Rotate the exposed key, remove it from distributed artifacts, and load payment credentials from a secret store or runtime environment.

Risk: Avalanche prices, TVL, APY, and validator cost estimates in the artifact may become stale.

Mitigation: Treat generated financial analysis as informational and refresh market or chain data from trusted sources before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-avalanche-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with tables, command snippets, and optional JSON output from monitoring scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled monitor script can emit JSON snapshots when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
