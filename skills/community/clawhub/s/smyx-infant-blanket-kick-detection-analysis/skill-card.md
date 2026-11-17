## Description:

Submits infant crib images or videos for blanket-coverage and kicking or slippage analysis, returning structured results and alert guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Caregivers and developers can request a structured visual review of crib footage for blanket coverage and kicking or slippage events, then use the returned report in a baby-monitoring workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Infant video and identity data raise privacy and data-transfer concerns.

Mitigation: Before use, ask the provider which video and identity data are sent, to which service, and how account creation and stored tokens are handled; consider not installing until these points are clear.

Risk: The security scan was partial because a referenced path was missing.

Mitigation: Treat the scan as incomplete and review the uncovered behavior before installation.

Risk: The skill describes continuous infant monitoring and alerts.

Mitigation: Do not rely on this skill for continuous monitoring or alerts; maintain adult supervision.

## Reference(s):

- [API interface documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Guidance]

**Output Format:** [Structured JSON analysis results, Markdown report listings, and alert text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blanket coverage estimates, detected events, alert fields, and report links when returned by the service.]

## Skill Version(s):

1.0.15 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
