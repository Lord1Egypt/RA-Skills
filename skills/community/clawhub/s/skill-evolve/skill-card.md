## Description:

Skill Evolve helps an agent preserve lessons from non-trivial tasks by creating, updating, reviewing, or removing reusable SKILL.md files for later reuse.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lorinwei](https://clawhub.ai/user/lorinwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn repeatable lessons from complex work into persistent skill instructions. It is intended for maintaining a reusable agent skill library after successful tasks, corrections, and environment-specific discoveries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change future agent behavior by creating or updating reusable skill files.

Mitigation: Require explicit approval before creating, updating, or deleting skills, and review learned content before activation.

Risk: The artifact includes a recursive deletion command for obsolete skills.

Mitigation: Replace deletion with a validated, reversible workflow such as archiving or moving the skill before permanent removal.

Risk: Captured lessons may include secrets or environment-specific details.

Mitigation: Review proposed skill content and remove credentials, tokens, private endpoints, and local-only assumptions before saving.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lorinwei/skills/skill-evolve)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with example SKILL.md content and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent changes to an agent skill library.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
