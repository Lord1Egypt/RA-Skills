## Description:

A multi-agent self-evolution system that automatically records learnings, errors, and feature requests, supports multi-agent statistics, and promotes recurring patterns into agent guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheney87](https://clawhub.ai/user/cheney87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, and feature requests across OpenClaw agents. It helps recurring learning patterns become durable guidance through shared learning files and optional daily promotion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent hooks and daily jobs can capture conversation or tool output across sessions.

Mitigation: Install only in environments where automatic learning capture is intended, and disable the hook or cron job when that capture is not needed.

Risk: Automatic promotion can modify SOUL.md and change future agent behavior.

Mitigation: Set AUTO_PROMOTE_ENABLED=false until promoted guidance has a review process.

Risk: Shared learning directories can mix context across agents or projects.

Mitigation: Use isolated per-project SHARED_LEARNING_DIR values and avoid use where secrets or proprietary context may be recorded.

Risk: The setup workflow defaults to root-oriented OpenClaw paths.

Mitigation: Avoid running setup as root unless that is the intended OpenClaw installation context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cheney87/skills/self-evolution-cn)
- [ClawHub homepage metadata](https://clawhub.ai/skills/self-evolution-cn)
- [Format reference](references/format.md)
- [Promotion reference](references/promotion.md)
- [Multi-agent reference](references/multi-agent.md)
- [OpenClaw integration reference](references/openclaw-integration.md)
- [Hook setup reference](references/hooks-setup.md)
- [Examples reference](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated learning, error, feature request, and agent guidance files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append records to shared learning files and, when automatic promotion is enabled, update SOUL.md based on recurring patterns.]

## Skill Version(s):

2.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
