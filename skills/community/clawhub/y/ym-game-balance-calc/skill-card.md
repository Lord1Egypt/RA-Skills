## Description:

Verifies game damage, leveling, and economy numbers with reproducible balance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Game designers, developers, and technical analysts use this skill to run local CLI checks for DPS formulas, leveling curves, and economy balance before comparing and tuning parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous or missing numeric inputs can lead to misleading balance conclusions.

Mitigation: Ask the user to choose DPS, leveling curve, or economy analysis and provide the required numeric parameters before running the calculator.

Risk: Custom formula strings could introduce ambiguity or unsafe expression handling.

Mitigation: Use only the built-in formula names documented by the skill; unsupported formula inputs are rejected.

## Reference(s):

- [Formula reference](artifact/references/formulas.md)
- [Server-resolved source repository](https://github.com/liuyuming0823/ym-game-balance-calc)
- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-game-balance-calc)
- [Publisher profile](https://clawhub.ai/user/liuyuming0823)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style report excerpts with reproducible shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline standard-library calculator; reports include verdicts and rerun commands for parameter comparisons.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
