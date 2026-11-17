## Description:

Analyzes Google search interest for a keyword in a selected market to identify rising, stable, declining, or seasonal demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers, marketers, and product researchers use this skill to assess keyword demand and seasonality in a chosen market before planning products or campaigns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid queries can consume qinghu credits, especially when retrieving many results.

Mitigation: Check the current estimate, explain possible variable charges, and obtain user approval before calling the paid tool.

Risk: The skill may install or upgrade Node and qhkit and alter local account configuration.

Mitigation: Review setup commands and account changes before execution; install only trusted packages with user approval.

Risk: Account tokens can be exposed if pasted into agent chat or shell history.

Mitigation: Provide credentials through a secure secret mechanism instead of pasting tokens into chat.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-google-trends)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Files]

**Output Format:** [Markdown summary with optional tabular data file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the market, time period, and sample size when available; larger results may be delivered as a file.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
