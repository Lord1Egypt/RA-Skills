## Description:

Captures agent learnings, errors, corrections, and feature requests in structured markdown so future sessions can review and promote recurring lessons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record command failures, user corrections, missing capabilities, knowledge gaps, and recurring best practices. It helps teams turn useful lessons into persistent project or agent guidance after review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files may retain secrets, personal data, or customer data.

Mitigation: Keep .learnings private by default and redact sensitive data before recording or sharing entries.

Risk: Hook-based reminders can become broad always-on context that affects normal agent behavior.

Mitigation: Use hooks only where needed, avoid global always-on configuration, and keep reminder output minimal.

Risk: Promoting unreviewed learnings into agent instruction files can introduce incorrect or misleading guidance.

Mitigation: Require explicit review before promoting entries into AGENTS.md, SOUL.md, TOOLS.md, CLAUDE.md, or Copilot instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-self-improving)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append persistent .learnings files and suggest promotion into agent instruction files after review.]

## Skill Version(s):

0.1.0 (source: evidence release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
