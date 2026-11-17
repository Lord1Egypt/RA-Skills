## Description:

Captures learnings, errors, and corrections so coding agents can log failures, user feedback, missing capabilities, outdated knowledge, and recurring best practices for later review and promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buradly](https://clawhub.ai/user/buradly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture corrections, command failures, feature requests, knowledge gaps, and useful recurring patterns in structured Markdown logs. Teams can later review those logs and promote durable guidance into agent memory or project instruction files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent self-improvement memory and promotion into agent or project instruction files.

Mitigation: Require explicit human approval before writing conversation-derived content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instruction files.

Risk: Always-on hooks can inject reminders into future agent sessions.

Mitigation: Prefer project-local hook setup, avoid user-global hooks, narrow hook matchers, and review the shell and OpenClaw hook code before enabling hooks.

Risk: Learning logs may capture sensitive project details, personal data, raw transcripts, credentials, or secrets.

Mitigation: Redact sensitive content before writing to .learnings and do not store secrets, credentials, personal data, or raw transcripts in persistent logs.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured log templates, shell commands, hook configuration examples, and optional helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning, error, and feature-request records that may be promoted to project or agent memory files after review.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
