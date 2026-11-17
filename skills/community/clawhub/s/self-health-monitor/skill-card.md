## Description:

Monitors an agent's own PCEC execution, memory usage, sub-agent activity, response quality, and skill inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde)

### License/Terms of Use:


## Use Case:

Agent operators and developers use this skill to periodically summarize an agent's operational health, including scheduled PCEC activity, memory metadata, sub-agent status, response quality, and skill load health. It can produce abnormal-state alerts when configured thresholds are crossed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to periodically inspect sensitive internal state such as memory metadata, task or sub-agent status, and skill inventory.

Mitigation: Limit reporting to aggregate telemetry and avoid reading memory contents or task payloads.

Risk: The skill describes automatic self-repair without defining clear limits.

Mitigation: Define alert recipients and require explicit approval before any repair action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/skills/self-health-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown health report with status summaries and alerts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should be limited to aggregate telemetry and avoid exposing memory contents or task payloads.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
