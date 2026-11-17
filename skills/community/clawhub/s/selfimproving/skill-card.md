## Description:

Captures learnings, errors, corrections, and missing capabilities so agents can log them, review them later, and promote durable guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richardan01](https://clawhub.ai/user/richardan01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture corrections, command failures, feature requests, knowledge gaps, and recurring workflow discoveries in learning logs. Teams can review those logs and promote durable lessons into project or agent memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning files and promoted memory can influence future agent sessions.

Mitigation: Install only where persistent learning is intended, keep hooks project-scoped, and review each promotion into agent or project instruction files.

Risk: Learning logs may accidentally capture sensitive data from commands, transcripts, credentials, or project context.

Mitigation: Do not store secrets, raw transcripts, credentials, or sensitive command output in learning files.

Risk: Always-on hooks can add reminders broadly across normal workflows.

Mitigation: Avoid empty matchers for routine use and enable hook reminders only for the projects or prompt classes that need them.

## Reference(s):

- [Hook Setup Guide](artifact/references/hooks-setup.md)
- [OpenClaw Integration](artifact/references/openclaw-integration.md)
- [Entry Examples](artifact/references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/richardan01/skills/selfimproving)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, hook code, and learning-entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent learning logs and optional hook reminders; review stored entries before promoting them into agent or project memory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
