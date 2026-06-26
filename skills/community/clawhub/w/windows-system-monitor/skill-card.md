## Description: <br>
Monitors Windows system status, including CPU, memory, disk, network, processes, and event logs, and notifies users when issues are detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Windows administrators use this skill to check host health, review resource pressure, and receive alerts when configured thresholds are exceeded. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitoring can expose system status, resource usage, process, network, log, or alert details to unintended recipients. <br>
Mitigation: Configure Feishu and other alerts to send only minimal necessary system details to trusted recipients. <br>
Risk: A monitoring schedule could run more often or in more contexts than intended. <br>
Mitigation: Confirm that monitoring runs only on explicit request or on a schedule the operator approves. <br>
Risk: Referenced monitoring code is not bundled in this release artifact. <br>
Mitigation: Inspect any separate Python monitoring script before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jirboy/windows-system-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/jirboy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and references to JSON status reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local monitoring scripts, report files, logs, and Feishu notification configuration.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
