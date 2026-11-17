## Description:

A local Streamlit log analysis dashboard for log statistics, duplicate detection, error analysis, and anomaly identification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godyounger](https://clawhub.ai/user/godyounger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run a local dashboard that analyzes selected log directories for volume, duplicate lines, error patterns, recent errors, and timestamp-based anomalies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected log directories can contain sensitive operational data or secrets.

Mitigation: Point the dashboard only at necessary scoped directories and review or redact sensitive logs before analysis when possible.

Risk: Dependencies are installed from pip without pinned versions.

Mitigation: Use a contained Python environment and lock or review dependency versions before deployment.

Risk: Large log sets can take significant time or memory to analyze.

Mitigation: Use the maximum file count control and avoid broad directories unless the analysis requires them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/godyounger/skills/splunk-log-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, analysis]

**Output Format:** [Markdown guidance and local Streamlit dashboard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally against user-selected .log, .txt, or .csv files; default Streamlit port is 8506.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
