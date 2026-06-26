## Description: <br>
Runs a local Streamlit dashboard for log statistics, duplicate detection, error analysis, and anomaly detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodYounger](https://clawhub.ai/user/GodYounger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and security teams use this skill to launch a local dashboard that inspects application logs for volume, duplicates, errors, and time-based anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard reads the log directory selected by the user, which can expose more local files than intended if a broad private folder is chosen. <br>
Mitigation: Point the dashboard only at the specific log directory needed for the analysis. <br>
Risk: Dashboard results may display credentials, personal data, or internal infrastructure details contained in logs. <br>
Mitigation: Treat dashboard output as sensitive and review or redact logs before sharing results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GodYounger/splunk-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and an interactive Streamlit dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally against user-selected log directories; dashboard output may include sensitive log content.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
