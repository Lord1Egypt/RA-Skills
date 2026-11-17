## Description:

Create or update AgentSkills. Use when designing, structuring, or packaging skills with scripts, references, and assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to design, structure, validate, and package AgentSkills, including skills that need vault-aware credential guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or edited skill content can introduce incorrect or misleading guidance.

Mitigation: Review SKILL.md and bundled resources before deployment, and test helper scripts on representative examples.

Risk: The packaging validator warns about possible secrets but does not block packaging them.

Mitigation: Review generated or edited skills for plaintext secrets, use vault-based environment references, and run a separate secret scan before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/skill-creator-vault-enhancement)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify skill files and package .skill archives when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
