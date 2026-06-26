## Description: <br>
DNS reconnaissance and subdomain enumeration using rapiddns-cli and the RapidDNS API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rapiddns](https://clawhub.ai/user/rapiddns) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security practitioners use this skill to set up rapiddns-cli and run authorized DNS reconnaissance, including subdomain enumeration, reverse IP lookup, CIDR enumeration, advanced DNS queries, and bulk DNS data export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RapidDNS API keys can be exposed through command history, configuration files, or shared logs. <br>
Mitigation: Treat the API key like a password, avoid sharing logs that contain credentials, and prefer protected configuration or environment-based handling. <br>
Risk: Bulk DNS reconnaissance and exports can be misused or run against unauthorized targets. <br>
Mitigation: Run enumeration only for authorized targets and scope large exports before execution. <br>
Risk: Export and extraction workflows can create local result files containing reconnaissance data. <br>
Mitigation: Store generated files in an appropriate workspace and review them before sharing or retaining them. <br>


## Reference(s): <br>
- [RapidDNS API Reference](references/api.md) <br>
- [RapidDNS website](https://rapiddns.io) <br>
- [RapidDNS CLI releases](https://github.com/rapiddns/rapiddns-cli/releases/latest) <br>
- [ClawHub skill page](https://clawhub.ai/rapiddns/rapiddns) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide generation of RapidDNS CLI output in JSON, CSV, or text formats and local result files when export workflows are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
