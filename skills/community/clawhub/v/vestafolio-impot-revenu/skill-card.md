## Description:

Compute French income tax (impôt sur le revenu) with the 2026 progressive barème, quotient familial and décote using Vestafolio's simulator API, after asking the simulator's questions (revenu net imposable, situation familiale, déclaration commune, enfants à charge, handicap, garde alternée, parent isolé, réductions).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather French household tax inputs, obtain consent to send those inputs to Vestafolio, and return an API-grounded estimate of income tax, marginal rate, average rate, parts fiscales, and tax effects of family situation changes.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: The skill may transmit income, family situation, children-related fields, partner income, and reductions or credits to Vestafolio's external API.

Mitigation: Summarize the exact fields and values to be sent, obtain user approval for that destination and data scope, and skip the API call if the user declines.

Risk: The calculation is an estimate for French income tax and may be incomplete for unmodeled taxes or changed tax rules.

Mitigation: Ground numerical answers in the API result, state assumptions and limits, and avoid inventing results when execution or network access is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-impot-revenu)
- [Vestafolio](https://www.vestafolio.com)
- [Vestafolio income-tax simulator](https://www.vestafolio.com/simulateurs/impot-revenu)
- [Vestafolio income-tax API schema](https://www.vestafolio.com/api/tools/v1/impot-revenu)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, API Calls]

**Output Format:** [Markdown with tax calculation summaries and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user approval before sending personal tax inputs to Vestafolio's external API.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
