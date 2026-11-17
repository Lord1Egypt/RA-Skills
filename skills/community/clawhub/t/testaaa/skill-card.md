## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaotec](https://clawhub.ai/user/chaotec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture corrections, command failures, knowledge gaps, and feature requests as structured markdown learnings that can be reviewed and promoted into project or agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learnings can carry conversation-derived guidance into future agent behavior without enough approval gates.

Mitigation: Use project-local learning logs, review entries before promotion, and require explicit user approval before changing AGENTS.md, CLAUDE.md, Copilot instructions, SOUL.md, or TOOLS.md.

Risk: Always-on hooks can inject reminders broadly across future sessions.

Mitigation: Review hook scripts before enabling them and avoid global hook setup unless the environment is trusted and the behavior is explicitly desired.

## Reference(s):

- [Examples](artifact/references/examples.md)
- [Hooks Setup](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/chaotec/skills/testaaa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local learning logs and optional agent guidance or hook configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
