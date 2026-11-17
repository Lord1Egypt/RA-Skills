## Description:

Self-improving agent system that analyzes conversation quality, identifies improvement opportunities, and continuously optimizes response strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiucheng](https://clawhub.ai/user/xiucheng)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to track conversation quality, record improvement insights, generate weekly progress reports, and suggest response-strategy updates for OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-quality logs and improvement insights may persist private prompts, customer data, credentials, or other sensitive content in the local workspace.

Mitigation: Do not log secrets or sensitive conversation content, and review where the OpenClaw workspace stores improvement_log.md before use.

Risk: Automatic-analysis behavior may be unclear to users and operators.

Mitigation: Confirm when analysis runs, what content is analyzed, and whether automatic analysis is enabled before using the skill in shared or sensitive environments.

## Reference(s):

- [Project homepage](https://github.com/xiucheng/self-improving-agent)
- [ClawHub skill page](https://clawhub.ai/xiucheng/skills/xiucheng-self-improving-agent)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance, Files]

**Output Format:** [Text, Markdown reports, JSON-like analysis and statistics, and local Markdown log entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append improvement insights to improvement_log.md in the configured OpenClaw workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.yaml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
