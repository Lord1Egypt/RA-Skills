## Description:

Premium Skill Creator by Kevin Jeppesen (The Operator Vault). Create better OpenClaw skills with a premium first-use setup wizard pattern, minimal context bloat, and reusable scaffolding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevjade](https://clawhub.ai/user/kevjade)

### License/Terms of Use:


## Use Case:

Developers and skill authors use this skill to create or upgrade OpenClaw skills with a first-use setup wizard, persistent workspace configuration, concise SKILL.md content, and optional scaffolding scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffolding helper writes files to a chosen output directory and can replace existing generated skill content.

Mitigation: Use a dedicated output directory, avoid shared or attacker-controlled folders, and check whether the target skill directory already exists before running the bundled script.

## Reference(s):

- [Links](references/LINKS.md)
- [Skill Creator Operator Overview](references/OVERVIEW.md)
- [Skill Creator Principles](references/PRINCIPLES.md)
- [Skill Creator Operator on ClawHub](https://clawhub.ai/kevjade/skills/skill-creator-operator)
- [Kevin Jeppesen on YouTube](https://www.youtube.com/@kevin-jeppesen)
- [Operator Vault](https://theoperatorvault.io)
- [Operator Vault Skool](https://skool.com/operator-vault)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create SKILL.md, references, scripts, and workspace configuration files for a new skill.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
