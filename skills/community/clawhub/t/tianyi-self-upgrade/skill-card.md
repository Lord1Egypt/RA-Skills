## Description: <br>
Helps OpenClaw maintain and upgrade itself by checking versions, migrating deprecated configuration fields, validating dependencies, creating backups, and producing upgrade reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fffdz](https://clawhub.ai/user/fffdz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and maintainers use this skill to inspect configuration health, preview or apply low-risk maintenance updates, and plan safer migrations with backup and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make durable OpenClaw configuration changes without a strong approval boundary. <br>
Mitigation: Use dry-run first, require review before applying configuration changes, and keep backups before any modification. <br>
Risk: Configuration backups may contain tokens or other sensitive values. <br>
Mitigation: Store backups in a protected location and avoid exposing backup paths or contents in shared logs. <br>
Risk: The advertised rollback command may not be implemented or reliable for recovery. <br>
Mitigation: Verify rollback behavior manually before relying on it, and keep a known-good copy of the configuration. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown upgrade report with PowerShell command and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include backup paths, validation results, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
