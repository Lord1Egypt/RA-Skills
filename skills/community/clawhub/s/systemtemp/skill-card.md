## Description: <br>
SystemTemp helps agents monitor system temperature, CPU status, sensor readings, alerts, and temperature reports through a local Node.js CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ofather](https://clawhub.ai/user/ofather) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for current hardware temperature status, review recent temperature history, configure threshold alerts, and generate local temperature reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI creates and updates local temperature history, alert configuration, and report files under ~/openclaw_workspace. <br>
Mitigation: Install and run it with normal user permissions, and review the configured workspace paths before relying on the stored files. <br>
Risk: The documented cron example can run monitoring commands repeatedly on a schedule. <br>
Mitigation: Add scheduled execution only when continuous monitoring is intended, and verify the cron command path matches the installed workspace. <br>
Risk: Temperature readings depend on the target machine's exposed thermal sensor files. <br>
Mitigation: Validate sensor availability and expected readings on the target hardware before using alerts or reports for operational decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ofather/systemtemp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown or plain text responses with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local thermal sensor files and writes local history, alert configuration, and reports under ~/openclaw_workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
