## Description:

Analyzes livestock behavior in continuous barn videos alongside environmental sensor data to identify group stress responses associated with abnormal conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Livestock facility operators and animal-care teams can use the skill to correlate barn video behavior with temperature, humidity, ammonia, and other sensor readings, then review environment-linked stress findings and reports. Its documentation describes the results as monitoring references and says it does not provide equipment-control instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks this release suspicious for behavior beyond its livestock-analysis purpose, citing credential handling, broad network actions, and options that may trigger analysis unexpectedly.

Mitigation: Review the findings before installation, with attention to credential transmission to caller-supplied destinations, account registration and token storage, and analysis behavior under export-only options. The scan was partial because one local reference was missing.

## Reference(s):

- [Skill overview and demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-environmental-anomaly-analysis)
- [API reference](artifact/references/api_doc.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Report links]

**Output Format:** [Structured analysis report with behavior features, environmental correlations, stress level, and report links; history lists are formatted as Markdown tables.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The analysis correlates video observations with optional sensor time series. Results are presented as reference information for monitoring.]

## Skill Version(s):

1.0.16 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
