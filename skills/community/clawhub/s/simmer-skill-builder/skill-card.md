## Description:

Generates installable OpenClaw prediction-market trading skills from natural-language strategies, including trading code and configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn trading ideas into installable Simmer/OpenClaw skills with documented strategy logic, configuration, and dry-run defaults.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated strategies can place real-money trades and cause losses.

Mitigation: Review generated code, test in dry-run mode, and apply small trading limits before enabling live orders.

Risk: API keys or live venue credentials can grant access to portfolio data and trading.

Mitigation: Provide credentials only when ready to allow access to portfolio data or place trades.

Risk: Publishing makes a generated skill publicly installable.

Mitigation: Review the skill before publication and use the included typed confirmation gate.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/simmer/skills/simmer-skill-builder)
- [Simmer skill-building guide](https://docs.simmer.markets/skills/building)
- [Simmer API reference](references/simmer-api.md)
- [Generated skill template](references/skill-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration]

**Output Format:** [Skill folder with Markdown documentation, Python script, and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated trading skills default to dry run; public publishing requires explicit confirmation.]

## Skill Version(s):

1.3.14 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
