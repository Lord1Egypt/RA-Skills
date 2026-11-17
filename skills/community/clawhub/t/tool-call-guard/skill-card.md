## Description:

Classifies agent tool calls by side effect and returns a suggested allow, confirm, or block decision for file, network, messaging, and payment actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating agents with file, network, database, messaging, or payment tools can use this skill to classify calls and shape approval workflows. Treat its decisions as advisory: the classifier does not enforce blocks or approvals on its own.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The classifier can label some dangerous actions safe and does not itself enforce blocks or approvals.

Mitigation: Treat its result as advisory. Before relying on it for files, messages, or payments, use an enforcing dispatcher that rejects unknown operations, requires explicit approval, and records appropriately redacted audits. Independently review the source and probe classifications; enforcement by a separate host integration remains unverified.

## Reference(s):

- [Tool Call Guard on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/tool-call-guard)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [UIBC protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)
- [LGD ecosystem hub](https://zhaoxinghua09-cell.github.io/lgd-hub/)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [Structured JSON classification with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Classification is advisory; execution blocking and approval require a separate enforcing integration.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
