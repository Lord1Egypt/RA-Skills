## Description: <br>
A local Streamlit log analysis dashboard for log statistics, duplicate detection, error analysis, and anomaly identification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GodYounger](https://clawhub.ai/user/GodYounger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to launch a local dashboard for inspecting selected log folders, summarizing log volume, finding duplicate lines, identifying errors, and spotting time-based anomalies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log files can contain secrets, tokens, IP addresses, and operational details. <br>
Mitigation: Point the dashboard only at intended folders, keep file limits narrow, and avoid exposing the local dashboard beyond the machine running it. <br>
Risk: Analyzing many large log files can consume significant memory or take a long time. <br>
Mitigation: Use the maximum file count and file pattern settings to limit each analysis run. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GodYounger/system-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and local Streamlit dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The dashboard reads a user-selected local log directory and can display statistics, tables, and charts at localhost:8506.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
