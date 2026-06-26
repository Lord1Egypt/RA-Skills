## Description: <br>
Display a compact ASCII dashboard showing system uptime, CPU load, memory, disk usage, and top open network ports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianghwxm](https://clawhub.ai/user/jianghwxm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to get a quick local Linux system status snapshot before troubleshooting or checking basic host health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dashboard can expose local host details such as uptime, resource usage, disk capacity, and listening TCP ports. <br>
Mitigation: Run it only when a local system snapshot is intended, and avoid posting the output to public or untrusted channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianghwxm/sysspeek) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text] <br>
**Output Format:** [Plain text ASCII dashboard] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports uptime, CPU load, memory use, root disk usage, and listening TCP ports.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
