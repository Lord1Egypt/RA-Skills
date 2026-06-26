## Description: <br>
Comprehensive system diagnostics and health check for Linux servers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and server administrators use this skill to inspect Linux system health, diagnose resource pressure, and generate local diagnostic reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diagnostic output can reveal sensitive local system details such as hostnames, IP addresses, routes, filesystems, services, and logged-in users. <br>
Mitigation: Treat terminal, JSON, and HTML reports as sensitive; redact or restrict them before sharing outside the operational team. <br>
Risk: The default network check performs a DNS lookup for google.com. <br>
Mitigation: Avoid the network check in air-gapped or no-egress environments, or review and edit the DNS target before running it. <br>


## Reference(s): <br>
- [ClawHub System Doctor listing](https://clawhub.ai/ericlooi504/sys-doctor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands] <br>
**Output Format:** [Terminal text, JSON, or HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include hostnames, IP addresses, mounted filesystems, running services, logged-in users, and DNS check timing.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
