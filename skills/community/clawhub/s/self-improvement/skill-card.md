## Description:

Captures learnings, errors, and corrections to enable continuous improvement for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike5230odense](https://clawhub.ai/user/mike5230odense)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to capture command failures, user corrections, feature requests, knowledge gaps, and recurring best practices in reusable markdown logs. The skill can also guide promotion of broadly useful learnings into future agent instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist conversation-derived notes, which can capture secrets, personal data, or sensitive project information if used without review.

Mitigation: Redact secrets and personal data before logging and keep learning logs project-local unless they are intentionally shared.

Risk: The skill promotes learnings into future instruction files, which can preserve incorrect or misleading guidance across sessions.

Mitigation: Require human review before adding any learning to CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or copilot instruction files.

Risk: Optional hooks can broaden when reminder or detection scripts run.

Mitigation: Prefer project-local setup, narrow hook matchers, and review hook scripts before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike5230odense/skills/self-improvement)
- [Publisher profile](https://clawhub.ai/user/mike5230odense)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local markdown learning logs and, when enabled, inject reminder text through agent hooks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
