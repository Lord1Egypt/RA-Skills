## Description:

Captures learnings, errors, corrections, and recurring improvements so coding agents can log, review, and promote useful context into project memory or reusable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiongyj625](https://clawhub.ai/user/xiongyj625)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture command failures, user corrections, knowledge gaps, missing capability requests, and better recurring workflows as structured markdown records. The skill also guides promotion of durable guidance into files such as AGENTS.md, CLAUDE.md, copilot-instructions.md, SOUL.md, TOOLS.md, or a reusable skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save chat-derived details into persistent learning and memory files.

Mitigation: Use project-local .learnings storage when possible, redact secrets and private context before logging, and review entries before sharing or promotion.

Risk: Promoting lessons into agent instruction files can make incorrect or overly broad guidance persistent.

Mitigation: Require explicit human approval before promotion into CLAUDE.md, AGENTS.md, .github/copilot-instructions.md, SOUL.md, TOOLS.md, or a new skill.

Risk: Always-on hooks can inject reminders into many sessions and increase persistent memory behavior.

Mitigation: Keep hook setup optional, prefer minimal project-level activation, and review hook scripts before enabling them.

## Reference(s):

- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, hook configuration snippets, and reusable entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update .learnings entries and optional skill scaffolds; hook activation is opt-in.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata; artifact _meta.json reports 3.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
