## Description: <br>
Ubuntu Inspector runs local Ubuntu health checks across system information, CPU, memory, disk, network, service status, security signals, processes, logs, and package update status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengchiangwork](https://clawhub.ai/user/chengchiangwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect Ubuntu servers, troubleshoot system issues, and generate local maintenance reports during routine operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local inspection report can contain sensitive system details such as hostnames, IP addresses, listening ports, usernames, login history, process listings, and recent errors. <br>
Mitigation: Run the skill only on Ubuntu systems you intend to inspect, protect or delete the /tmp report after use, and share the report only with authorized recipients. <br>
Risk: Running with root privileges can expose fuller host and log details than a normal user run. <br>
Mitigation: Use root only when full visibility is required for the inspection task. <br>


## Reference(s): <br>
- [Ubuntu Inspector ClawHub page](https://clawhub.ai/chengchiangwork/ubuntu-inspector) <br>
- [Publisher profile](https://clawhub.ai/user/chengchiangwork) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a generated plain-text inspection report path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated report is written under /tmp and may include sensitive host, network, user, process, login, and error-log details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
