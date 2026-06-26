## Description: <br>
Safe Shell is a read-only command-line helper that allows file, system, and network queries while blocking destructive or modifying commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengyusheng188](https://clawhub.ai/user/chengyusheng188) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-assistant operators use Safe Shell to propose or check read-only diagnostic commands for file inspection, system status, and network troubleshooting across macOS, Linux, and Windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command filter is best-effort and should not be treated as a secure sandbox. <br>
Mitigation: Review each command before execution and run commands with least privilege in an appropriate sandbox or controlled environment. <br>
Risk: Read-only filesystem, environment, and network diagnostics can expose sensitive local or network information. <br>
Mitigation: Avoid broad filesystem reads, private files, and environment-variable dumps; require explicit approval for network diagnostics or wide system inspection. <br>


## Reference(s): <br>
- [Safe Shell on ClawHub](https://clawhub.ai/chengyusheng188/safe-shell) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text with shell command suggestions and safety refusals] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only command suggestions or refusal messages; command execution should remain separately reviewed.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
