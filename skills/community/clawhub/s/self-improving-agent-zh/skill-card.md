## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuxian-upup](https://clawhub.ai/user/wuxian-upup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture corrections, command failures, knowledge gaps, feature requests, and recurring workflow lessons in structured markdown files. They can review those logs later and promote broadly useful learnings into agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation-derived details may be saved into long-lived learning or memory files.

Mitigation: Keep .learnings local and ignored by default, redact secrets and personal or customer data before logging, and review entries before sharing or committing them.

Risk: Global hooks can inject self-improvement reminders across sessions and increase persistent prompting behavior.

Mitigation: Enable hooks only when the reminder workflow is desired, prefer project-level configuration, and review hook scripts before enabling them.

Risk: Promoting unreviewed learnings can introduce incorrect or sensitive guidance into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or Copilot instructions.

Mitigation: Require human review before promoting learnings into long-lived agent memory or instruction files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wuxian-upup/skills/self-improving-agent-zh)
- [Hook Setup Guide](references/hooks-setup.md)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Entry Examples](references/examples.md)
- [Learning Template](assets/LEARNINGS.md)
- [Skill Template](assets/SKILL-TEMPLATE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and structured learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create or update local .learnings files and promote reviewed entries into long-lived agent memory files.]

## Skill Version(s):

1.0.0 (source: evidence target metadata, release.version, package.json, and package-lock.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
