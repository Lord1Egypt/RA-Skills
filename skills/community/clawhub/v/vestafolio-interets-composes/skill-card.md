## Description:

Projects compound-interest growth for an investment with initial capital and monthly contributions by collecting simulator inputs and, with user approval, calling Vestafolio's simulator API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer compound-interest projection questions with Vestafolio's simulator, including final value, total invested, gains, and a year-by-year evolution table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulator inputs are sent to Vestafolio's external API.

Mitigation: Before any API call, summarize the exact fields and values, name the destination, obtain user approval, and omit personal identifiers, account details, credentials, files, and broader conversation history.

Risk: Projection outputs can be mistaken for guaranteed returns or investment advice.

Mitigation: State that calculations assume constant returns and contributions, exclude tax and fees, and are estimates rather than investment advice.

## Reference(s):

- [Vestafolio compound-interest API schema](https://www.vestafolio.com/api/tools/v1/interets-composes)
- [Vestafolio compound-interest simulator](https://www.vestafolio.com/simulateurs/interets-composes)
- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-interets-composes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown text with optional tables, API request details, assumptions, limits, and simulator links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a year-by-year investment table and must be grounded in the approved Vestafolio API result.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
