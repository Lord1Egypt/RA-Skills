## Description:

Captures learnings, errors, and corrections to enable continuous improvement for agent workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboincn](https://clawhub.ai/user/boboincn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to log corrections, command failures, missing capabilities, and reusable lessons into markdown files. It also provides optional hook setup and promotion guidance for turning high-value learnings into durable project or agent instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on hooks can repeatedly inject agent reminders and affect normal prompt handling.

Mitigation: Prefer project-scoped setup, avoid a global hook with an empty matcher, and narrow hook matchers to debugging or learning workflows.

Risk: Conversation-derived notes may preserve secrets, personal data, or incorrect conclusions in long-lived learning files.

Mitigation: Redact secrets and personal data before writing learnings, and review entries before they are reused.

Risk: Promoting learnings into permanent agent instructions can make incorrect or unreviewed behavior durable.

Mitigation: Require a manual diff review before promoting content into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, Copilot instructions, or a new skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboincn/skills/temp-skill-download)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs, hook configuration, project memory files, or skill scaffolds when the agent follows the guidance.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
