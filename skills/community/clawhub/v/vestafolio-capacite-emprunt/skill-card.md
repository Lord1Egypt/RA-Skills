## Description:

Estimate the maximum mortgage a French household can borrow from income, existing charges and the HCSF 35 % debt ratio using Vestafolio's simulator API, after asking the simulator's questions (net household income, fixed charges, rate, duration, insurance rate).

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to estimate French mortgage borrowing capacity from household income, fixed charges, interest rate, loan duration, insurance rate, and debt-ratio assumptions. The agent gathers required inputs, obtains approval before sending them to Vestafolio's API, and explains the returned estimate with relevant assumptions and limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends household financial inputs to Vestafolio's external API.

Mitigation: Before each API POST, summarize the exact fields and values to be sent and obtain explicit approval for that data and destination.

Risk: The borrowing estimate could be mistaken for bank approval or personalized financial advice.

Mitigation: State that the result is an estimate, not a bank pre-approval or financial advice, and explain that lenders may apply additional criteria.

Risk: Unnecessary personal data could be disclosed during the calculation.

Mitigation: Send only required simulator inputs and exclude names, addresses, account identifiers, credentials, files, and broader conversation history.

## Reference(s):

- [Vestafolio publisher profile](https://clawhub.ai/user/vestafolio)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-capacite-emprunt)
- [Vestafolio API schema](https://www.vestafolio.com/api/tools/v1/capacite-emprunt)
- [Vestafolio borrowing-capacity simulator](https://www.vestafolio.com/simulateurs/capacite-emprunt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Code]

**Output Format:** [Markdown answer grounded in JSON API results, with optional shell command or code snippets when needed to call the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before transmitting simulator inputs to Vestafolio.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
