## Description:

Helps retirees and near-retirees plan account withdrawals by estimating draw order, required minimum distributions, taxes, and Medicare IRMAA effects, with guidance on Roth conversion timing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

External users, including retirees and near-retirees, use this skill to compare taxable, traditional, and Roth withdrawal sequences and review five-year estimates for taxes, required minimum distributions, and IRMAA. It supports planning discussions; current tax figures and Roth conversion effects need independent verification.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Roth conversion recommendations may not include the conversion amount and related tax effects in the year-by-year model.

Mitigation: Treat conversion results as planning guidance; independently model conversion dollars and related tax and IRMAA effects, and verify projections with a qualified financial or tax professional.

Risk: The included tax brackets, IRMAA thresholds, and RMD assumptions are estimates and may not match current-year figures.

Mitigation: Verify current IRS and SSA tables before relying on a plan, as the skill's documentation directs.

## Reference(s):

- [Sequencing Doctrine](artifact/references/sequencing-doctrine.md)
- [Tax Tables & Thresholds (2026 estimates; verify)](artifact/references/tax-tables-2026.md)
- [ClawHub release](https://clawhub.ai/voronindenis5/skills/retirement-withdrawal-sequencer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with a five-year withdrawal plan, estimates, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses estimated tax and account assumptions; current-year figures and Roth conversion effects require independent verification.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
