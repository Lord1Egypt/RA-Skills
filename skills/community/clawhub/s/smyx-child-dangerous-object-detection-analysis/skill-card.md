## Description:

Provides a workflow for submitting child activity videos for dangerous-object and electrical-socket contact analysis, returning structured findings and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Families, childcare providers, and developers can submit child activity videos to check for contact with preset hazardous objects or electrical sockets, then review structured findings, alert text, and report links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags a mismatch between the child-safety monitoring description and supplied capabilities, along with privacy and unintended-action concerns. Its partial scan does not establish that advertised real-time monitoring or alerts work.

Mitigation: Before installation, verify the service destination, what video and account information it sends or stores, and the permissions it receives. Treat results as supplemental and maintain adult supervision.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-child-dangerous-object-detection-analysis)
- [API interface reference](artifact/references/api_doc.md)
- [Skill demonstration page](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis results, JSON, Markdown, Alert text, Report links]

**Output Format:** [Structured JSON results and text; historical reports can be presented as a Markdown table.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected behavior, confidence, event time, alert level, snapshot URL, and report links when returned by the service.]

## Skill Version(s):

1.0.11 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
