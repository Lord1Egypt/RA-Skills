## Description:

Retrieves historical Ozon keyword-trend snapshots by keyword ID across weekly, monthly, quarterly, or yearly periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to inspect a keyword's historical popularity and seasonality before making marketplace decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Node/npm tooling and qhkit or change local configuration when dependencies are missing.

Mitigation: Review or run setup commands yourself and install only if you trust Qinghu qhkit.

Risk: A Qinghu API token is needed for authenticated calls.

Mitigation: Protect the token and review configuration changes before use.

Risk: Trend lookups can consume paid Qinghu credits, with charges varying by result size.

Mitigation: Check the estimate and obtain user approval before paid calls, especially bulk retrieval.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-keyword-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend analysis with supporting figures; optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the period and sample size, and discloses credits used for paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
