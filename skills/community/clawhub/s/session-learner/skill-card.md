## Description:

Use when a session reveals stable user preferences, workflow corrections, or project conventions that should be preserved for future sessions. Also use when user explicitly asks to remember rules, update guidance, or summarize learnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lq434239](https://clawhub.ai/user/lq434239)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to identify stable session learnings, propose concise CLAUDE.md rules, and preserve durable workflow or project conventions for future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write lasting agent instructions into CLAUDE.md.

Mitigation: Review each proposed rule before it is written and prefer project-local CLAUDE.md unless a global rule is intentional.

Risk: Automatic end-of-session runs may skip confirmation before persisting guidance.

Mitigation: Avoid automatic end-of-session writes unless the installation policy explicitly allows that behavior.

## Reference(s):

- [Learning Rules](references/learning-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/lq434239/skills/session-learner)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Markdown bullets and CLAUDE.md updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write persistent agent instructions after confirmation, or without confirmation when run from an automatic SessionEnd hook.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
