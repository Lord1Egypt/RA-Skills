## Description:

SkillMe helps agents search ClawHub and skills.sh, compare discovered skills, install ClawHub skills, and convert skills.sh skills into OpenClaw-compatible format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghesericsu](https://clawhub.ai/user/ghesericsu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover relevant agent skills across ClawHub and skills.sh, evaluate basic quality signals, choose an install location, and convert skills.sh skills into OpenClaw-compatible SKILL.md files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install unverified remote instructions into active skill folders.

Mitigation: Prefer local workspace installs, inspect converted SKILL.md content before activation, and avoid global unattended installs.

Risk: The skill runs unpinned external commands while searching or installing skills.

Mitigation: Pin or verify external packages and remote skill sources before installation.

## Reference(s):

- [SkillMe on ClawHub](https://clawhub.ai/ghesericsu/skills/skillme)
- [skills.sh registry](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with result tables, install commands, and generated SKILL.md content when converting skills.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce filesystem changes when the user confirms an installation or conversion workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
