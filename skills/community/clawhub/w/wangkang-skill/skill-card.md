## Description:

Captures learnings, errors, corrections, and feature requests so agents can record reusable knowledge and promote high-value patterns into project or workspace memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangkang5](https://clawhub.ai/user/wangkang5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture command failures, user corrections, knowledge gaps, and recurring best practices as structured Markdown logs. It also provides optional hook reminders and a helper for scaffolding a reusable skill from a promoted learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs and promoted memory can preserve private data, secrets, or incorrect guidance.

Mitigation: Keep logs local when possible, redact sensitive content, and review entries before promoting them into CLAUDE.md, AGENTS.md, SOUL.md, TOOLS.md, or other future agent context.

Risk: Always-on hooks can repeatedly inject guidance into sessions and may broaden the skill's influence beyond the intended workspace.

Mitigation: Enable hooks only with explicit consent, prefer workspace-scoped or minimal hook configuration, avoid global hooks unless necessary, and disable or narrow matchers if reminders become intrusive.

Risk: Promoting untrusted user text into future instructions can change agent behavior in later sessions.

Mitigation: Treat captured learnings as reviewable notes, not authoritative instructions, and approve only concise, verified patterns for long-term memory.

Risk: The extraction helper can create new skill scaffold files in the workspace.

Mitigation: Use dry-run mode first, keep output directories relative and scoped, and review generated files before relying on or publishing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangkang5/skills/wangkang-skill)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands, templates, and optional hook code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learning logs, workspace memory files, hook configuration, or skill scaffold files when the user chooses to apply the guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
