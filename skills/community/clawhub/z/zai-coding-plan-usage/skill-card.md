## Description:

Query Z.ai Coding Plan usage and quota limits, including token consumption, MCP usage, and subscription status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyizhou](https://clawhub.ai/user/hyizhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Z.ai Coding Plan users use this skill to check recent account usage, quota consumption, MCP usage, and subscription status from their configured Z.ai credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends authenticated requests to Z.ai usage endpoints and displays account usage details.

Mitigation: Install and run it only in environments where the configured Z.ai credential is intended for usage monitoring.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hyizhou/skills/zai-coding-plan-usage)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with quota, model usage, and tool usage summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Z.ai API key configured in OpenClaw or provided through ZAI_API_KEY or ZHIPU_API_KEY.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
