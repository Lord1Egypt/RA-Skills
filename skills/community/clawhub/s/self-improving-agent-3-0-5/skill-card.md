## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can document recurring issues and promote validated knowledge into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mutsunico](https://clawhub.ai/user/mutsunico)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, and reusable workflow improvements in structured Markdown logs. It also guides review and promotion of broadly useful learnings into agent instruction or workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs may capture secrets, personal data, or sensitive project details from conversations and command output.

Mitigation: Redact secrets and user data before logging, and keep .learnings ignored by default unless the team intentionally reviews and shares those files.

Risk: Promoting conversation-derived learnings into future instruction files can make incorrect or misleading guidance persistent.

Mitigation: Require human review before promoting any learning into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or copilot instruction files.

Risk: Broad hook triggers can add persistent reminders or logging pressure across many sessions.

Mitigation: Prefer project-local setup over global hooks and avoid empty hook matchers where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mutsunico/skills/self-improving-agent-3-0-5)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, hook snippets, and structured log templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local .learnings Markdown logs and suggest promotion into agent instruction files after human review.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 3.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
