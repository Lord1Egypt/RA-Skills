## Description:

Analyzes workplace camera footage for changes in facial-expression and posture patterns, then produces employee emotion-trend reports and HR alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams use the reports to review behavioral trends and consider voluntary, supportive employee check-ins. The reports are for internal wellbeing reference and should not be used for diagnosis or employment decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports linked to workstations may identify employees despite anonymity claims.

Mitigation: Treat reports as identifiable employee data, restrict access, and require transparent outreach and meaningful consent and opt-outs.

Risk: Footage may be sent for cloud processing contrary to selected settings.

Mitigation: Do not use real employee footage until destination and no-analysis controls are fixed and cloud processing is explicitly authorized.

Risk: Retention and HR access controls are not established by the bundled code.

Mitigation: Independently verify the service's retention and HR access controls before use.

## Reference(s):

- [API interface and data-handling guidance](artifact/references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Guidance, Links]

**Output Format:** [Structured JSON analysis and human-readable report text with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may contain behavioral metrics, trend alerts, and HR support suggestions; results can be optionally saved to a file.]

## Skill Version(s):

1.0.14 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
