## Description:

Simulates early retirement (FIRE) financed by invested capital for a French saver using Vestafolio's simulator API after collecting the required financial and retirement inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate capital-funded early retirement timing, required capital, sustainability, and improvement levers for French FIRE scenarios. It is for retirement simulation estimates and not statutory pension-rights calculation or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can transmit personal financial and retirement inputs to Vestafolio's external API.

Mitigation: Before any API call, summarize the fields and values to be sent, obtain the user's agreement, and omit names, addresses, account identifiers, credentials, files, unused optional data, and conversation history.

Risk: Simulation results may be mistaken for financial advice or guaranteed retirement outcomes.

Mitigation: Present results as estimates, state assumptions and limits, and note that real returns, tax law, statutory pension income, and user circumstances can differ.

Risk: If network access or the API fails, the agent may be tempted to substitute mental arithmetic or example values.

Mitigation: Do not invent a result; say the calculation could not be completed and provide the interactive simulator link when useful.

## Reference(s):

- [Vestafolio age-retraite API schema and simulation endpoint](https://www.vestafolio.com/api/tools/v1/age-retraite)
- [Vestafolio age-retraite interactive simulator](https://www.vestafolio.com/simulateurs/age-retraite)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-age-retraite)
- [Vestafolio site](https://www.vestafolio.com)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, API calls]

**Output Format:** [Markdown or text with optional inline shell commands and API-derived retirement simulation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounds numerical answers in the Vestafolio API result after user approval; responds in French when the user writes in French.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter states 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
