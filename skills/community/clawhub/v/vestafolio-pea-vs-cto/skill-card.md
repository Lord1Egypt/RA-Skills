## Description:

Compare PEA, CTO (compte-titres) and assurance-vie net-of-tax outcomes for a French investor using Vestafolio's simulator API after collecting the simulator inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and financial planning assistants use this skill to compare French PEA, CTO, and assurance-vie scenarios with user-approved simulator inputs. It is intended for France-specific investment envelope comparisons and not for personalized tax advice without checking assumptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends simulator inputs to Vestafolio's external API.

Mitigation: Require explicit user approval after summarizing the exact fields and values to be sent, and do not transmit names, account identifiers, credentials, documents, or unrelated financial details.

Risk: Investment tax rates and simulator assumptions may be outdated or unsuitable for an individual case.

Mitigation: Ground numerical answers in the API result, state assumptions and limits, and avoid presenting results as tax advice.

## Reference(s):

- [Vestafolio publisher profile](https://clawhub.ai/user/vestafolio)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-pea-vs-cto)
- [Vestafolio simulator API](https://www.vestafolio.com/api/tools/v1/pea-vs-cto)
- [Vestafolio PEA vs CTO simulator](https://www.vestafolio.com/simulateurs/pea-vs-cto)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Markdown]

**Output Format:** [Markdown with concise analysis, assumptions, warnings, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are grounded in the Vestafolio API result after user approval; French is used when the user writes in French.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
