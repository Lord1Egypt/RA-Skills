## Description:

Captures learnings, errors, and corrections so coding agents can preserve useful context, track failures, and promote recurring lessons into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fardeenkarim](https://clawhub.ai/user/fardeenkarim)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to capture errors, user corrections, feature requests, knowledge gaps, and repeatable best practices in structured markdown files. It also guides review and promotion of broadly useful learnings into agent memory files or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent local memory that may capture sensitive conversation, error, or workspace details.

Mitigation: Keep .learnings local by default, redact secrets and personal data before logging, and avoid committing learning logs unless they have been reviewed.

Risk: Promoting unreviewed learnings into agent memory files can spread incorrect or misleading guidance across future sessions.

Mitigation: Require manual review before promoting entries into CLAUDE.md, AGENTS.md, Copilot instructions, SOUL.md, or TOOLS.md.

Risk: Optional hooks add reminders during agent workflows and may increase exposure of captured context if enabled globally.

Mitigation: Review hook scripts before enabling them, prefer workspace-scoped hook configuration, and avoid global hooks unless the behavior is explicitly desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fardeenkarim/skills/self-improvement-ai)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, TypeScript, and template snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured local learning entries, optional hook reminders, setup snippets, and skill-scaffold guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
