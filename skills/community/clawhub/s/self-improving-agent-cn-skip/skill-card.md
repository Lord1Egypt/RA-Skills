## Description:

This skill helps an agent record command errors, user corrections, and best practices as long-term memory to reduce repeated mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to capture repeated command failures, user preference corrections, and project best practices so future agent runs can consult prior lessons before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store commands, errors, corrections, and preferences across projects, which may retain sensitive or stale information.

Mitigation: Require explicit confirmation before saving memories and regularly review or redact memory files.

Risk: The skill describes automatic instruction-file edits and sudo fallback behavior, which can change agent behavior or escalate commands unexpectedly.

Mitigation: Disable automatic sudo fallback and require review before applying memories or editing AGENTS.md or MEMORY.md.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/a-din/skills/self-improving-agent-cn-skip)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSONL memory records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads local memory files under the user's OpenClaw memory directory when its helper scripts are used.]

## Skill Version(s):

1.0.0 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
