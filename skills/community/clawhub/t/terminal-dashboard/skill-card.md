## Description: <br>
Tool for shell commands execution, visualization and alerting. Configured with a simple YAML file. terminal-dashboard, go, alerting, charts, cmd. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain3](https://clawhub.ai/user/bytesagain3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to run a local terminal activity journal for data pipeline steps, data quality checks, schema changes, ad-hoc analysis, and pipeline debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-entered activity is stored as plaintext local log data and may remain searchable or exportable later. <br>
Mitigation: Avoid entering passwords, tokens, private customer data, or sensitive internal details; review and manage the local data directory according to your retention requirements. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration] <br>
**Output Format:** [Command-line text output and local log/export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores activity locally under ~/.local/share/terminal-dashboard by default; TERMINAL_DASHBOARD_DIR can override the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
