## Description: <br>
Validate OpenClaw installation safety by checking for common security misconfigurations and setup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusy2k](https://clawhub.ai/user/marcusy2k) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to audit an OpenClaw setup for permission, plugin manifest, sandboxing, and dependency-version issues before or during ongoing local operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dependency check may contact npm while auditing the local OpenClaw version. <br>
Mitigation: Run the skill deliberately in an environment where npm network access is acceptable, or perform dependency checks manually. <br>
Risk: Suggested remediation commands may remove plugins, update packages, reset configuration, or change file permissions. <br>
Mitigation: Review each suggested fix before running it and execute the skill as a normal user. <br>
Risk: Optional cron or heartbeat scheduling can make setup checks recur automatically. <br>
Mitigation: Use recurring scheduling only when continuous local setup auditing is intended. <br>


## Reference(s): <br>
- [Setup Validator Checks](references/CHECKS.md) <br>
- [Example Fixes for Common Issues](references/EXAMPLE_FIXES.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/marcusy2k/setup-validator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown documentation with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include actionable warnings and remediation commands for the user's local OpenClaw setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
