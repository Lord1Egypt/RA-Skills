## Description: <br>
Checks and summarizes local system information, including operating system, kernel, CPU, memory, disk, network, uptime, logged-in users, and user account details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xyxsz](https://clawhub.ai/user/xyxsz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and system administrators use this skill to inspect a host, summarize server status, and produce a concise system report during checks or troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can expose local usernames, logged-in sessions, IP addresses, hostnames, operating system details, home directories, or shell information. <br>
Mitigation: Review and redact system reports before sharing them outside the trusted operational context. <br>
Risk: System inventory details can help profile a host if disclosed to an unintended audience. <br>
Mitigation: Limit report collection and distribution to users who need local system inspection results. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands] <br>
**Output Format:** [Markdown report, with optional .md or .txt file output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summarizes read-only local inspection command output and highlights notable issues such as high disk usage or low memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
