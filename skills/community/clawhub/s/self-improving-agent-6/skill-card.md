## Description:

Captures learnings, errors, corrections, and feature requests so coding agents can turn recurring discoveries into durable project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallersoup](https://clawhub.ai/user/smallersoup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, knowledge gaps, and feature requests during coding-agent work. The logged entries help future sessions identify recurring issues and promote broadly useful guidance into project memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learning logs can persist sensitive session details, command output, or project context.

Mitigation: Keep .learnings local by default and redact secrets, credentials, and raw command output before storing entries.

Risk: Global hooks or empty matchers can inject reminders broadly across sessions.

Mitigation: Prefer project-local, opt-in hook setup and use narrower matchers when broad activation is not needed.

Risk: Promoted learnings can alter future agent behavior through CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Mitigation: Require manual review before promoting entries into durable agent instruction files.

## Reference(s):

- [Self Improvement Skill on ClawHub](https://clawhub.ai/smallersoup/skills/self-improving-agent-6)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update .learnings/*.md entries and recommend reviewed promotion into agent instruction files.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
