## Description:

Adaptive local skill scheduler for OpenClaw that helps an agent decide when to use one or more installed skills for multi-step or cross-domain tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spikesubingrui-design](https://clawhub.ai/user/spikesubingrui-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route multi-step or cross-domain OpenClaw tasks to relevant installed skills, ask before combining skills when needed, and record routing outcomes for feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent routing logs may save full task text, including secrets, personal data, proprietary code, or sensitive business context.

Mitigation: Do not use the skill with sensitive task text unless logging is removed, minimized, redacted, or made explicitly opt-in with retention and deletion controls.

Risk: The helper scripts read and write fixed local workspace paths, which may not match the installing user's intended storage location.

Mitigation: Review and configure local paths before use, and run the skill only in a workspace where those reads and writes are expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spikesubingrui-design/skills/spike-skill-orchestrator)
- [Artifact README](artifact/README.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, JSON, text]

**Output Format:** [Text or Markdown guidance with optional shell commands and JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked skill candidates, skill-combination suggestions, and concise rationale for whether to ask, directly use a skill, or skip orchestration.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
