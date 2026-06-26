## Description: <br>
Log query and troubleshooting workflows with Volcengine CLS. Use when users need error analysis, time-range queries, aggregation dashboards, or incident diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, SREs, and incident responders use this skill to construct Volcengine CLS log queries, summarize affected services and counts, identify top errors or anomaly dimensions, and produce remediation suggestions. <br>

### Deployment Geography for Use: <br>
Global, subject to the configured Volcengine CLS service region. <br>

## Known Risks and Mitigations: <br>
Risk: CLS investigations may include logs with secrets, credentials, or sensitive user data. <br>
Mitigation: Use appropriately scoped, preferably read-only Volcengine access and avoid sending sensitive log content unless it is intended for the investigation. <br>
Risk: Troubleshooting summaries can be misleading if the project, logset, topic, or time window is wrong. <br>
Mitigation: Confirm the target CLS project, logset, topic, and time range before relying on counts, anomaly dimensions, or remediation guidance. <br>


## Reference(s): <br>
- [Volcengine Observability Cls on ClawHub](https://clawhub.ai/cinience/volcengine-observability-cls) <br>
- [Sources](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown containing CLS query statements, affected services and counts, findings, and remediation suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no executable code or bundled tools were found in the release artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
