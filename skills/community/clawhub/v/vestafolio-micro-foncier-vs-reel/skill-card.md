## Description:

Compare unfurnished rental taxation between micro-foncier and regime reel with deficit foncier using Vestafolio's simulator API after collecting the required rental, charge, tax-bracket, and prior-deficit inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to compare French unfurnished-rental tax outcomes under micro-foncier and regime reel. It collects the simulator's required inputs, obtains explicit approval before sending them to Vestafolio, calls the simulator API, and explains the resulting recommendation, savings, assumptions, and limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends rental figures and tax-bracket inputs to Vestafolio's external API.

Mitigation: Before transmission, summarize the destination and exact fields to be sent, obtain explicit user approval, and offer the manual simulator link if approval is declined.

Risk: Tax rules, thresholds, and rates can change, and the simulator is an estimate rather than tax advice.

Mitigation: State the coded assumptions and limits in the answer, and recommend professional review when deficit treatment or binding tax choices matter.

Risk: If execution or network access fails, a schema fetch alone does not complete the simulation.

Mitigation: Report that the calculation could not be completed, avoid inventing a recommendation, and provide the simulator link for manual use when useful.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/vestafolio/skills/vestafolio-micro-foncier-vs-reel)
- [Vestafolio simulator API](https://www.vestafolio.com/api/tools/v1/micro-foncier-vs-reel)
- [Vestafolio interactive simulator](https://www.vestafolio.com/simulateurs/micro-foncier-vs-reel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown narrative with optional shell commands and API-derived calculation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be in French when the user writes in French and should ground personalized results in the API response rather than mental arithmetic.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter says 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
