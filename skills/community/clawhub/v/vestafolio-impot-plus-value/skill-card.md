## Description:

Computes French real-estate capital gains tax with holding-period abatements using Vestafolio's simulator API after collecting required sale inputs and obtaining explicit user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to estimate French property capital gains tax for sales of secondary residences, rental properties, or LMNP real-regime properties. It helps compare tax exposure now versus waiting, while grounding numerical results in Vestafolio's simulator output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property sale and tax inputs may be transmitted to Vestafolio's external API.

Mitigation: The skill requires a summary of fields and explicit user approval before any POST, and it offers the manual simulator link if approval is declined.

Risk: Tax rates, abatements, and eligibility for forfait deductions can change or depend on a user's facts.

Mitigation: Responses should present results as estimates, state assumptions and limits, and avoid treating simulator output as tax advice.

Risk: A failed or unavailable API call could lead to unsupported numerical answers.

Mitigation: The artifact instructs the agent not to invent results and to provide the manual simulator link when execution or network access is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-impot-plus-value)
- [Vestafolio publisher profile](https://clawhub.ai/user/vestafolio)
- [Vestafolio simulator](https://www.vestafolio.com/simulateurs/impot-plus-value)
- [Vestafolio simulator API schema](https://www.vestafolio.com/api/tools/v1/impot-plus-value)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with API-grounded calculation summaries and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before transmitting simulator inputs to Vestafolio; provides a manual simulator link when execution or approval is unavailable.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
