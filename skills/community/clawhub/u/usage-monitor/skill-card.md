## Description: <br>
Monitor any service usage dashboard and alert when a configured threshold is reached. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[strongking666](https://clawhub.ai/user/strongking666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure local monitoring for service usage or quota dashboards and receive alerts when usage reaches a chosen percentage threshold. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dashboard URLs, local configuration, and usage logs may reveal account-specific URLs or usage patterns. <br>
Mitigation: Use stable dashboard URLs without tokens, session IDs, API keys, or sensitive query strings, and keep config.json and usage-log.md out of public repositories, screenshots, shared folders, and broad backups. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/strongking666/usage-monitor) <br>
- [README](artifact/README.md) <br>
- [Install Guide](artifact/INSTALL.md) <br>
- [User Guide](artifact/USER-GUIDE.md) <br>
- [Configuration Schema](artifact/config.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update a local usage-log.md file when the monitor is run.] <br>

## Skill Version(s): <br>
2.0.0 (source: release metadata and README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
