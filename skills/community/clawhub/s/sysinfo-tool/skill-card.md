## Description: <br>
Display comprehensive system hardware and software information for diagnostics, inventory, and system profiling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to collect local CPU, memory, disk, operating system, uptime, network, and process information for diagnostics, inventory, documentation, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: System information reports can expose hostnames, network interface data, disk layout, usernames, and process command lines. <br>
Mitigation: Review and redact generated output before sharing it outside the intended diagnostic context. <br>
Risk: Process command lines can contain tokens, internal paths, or other sensitive operational details. <br>
Mitigation: Use brief or scoped options when full process details are not needed, and remove secrets or internal paths from reports. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON system information report, with usage guidance shown in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hostnames, network interface details, disk layout, usernames, and process command lines.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
