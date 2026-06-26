## Description: <br>
Use installed TrueCrypt on Windows to mount, dismount, inspect, and automate legacy TrueCrypt containers or encrypted partitions from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanestane](https://clawhub.ai/user/stanestane) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and power users use this skill to generate cautious Windows TrueCrypt CLI commands for mounting, dismounting, inspecting, and automating legacy TrueCrypt volumes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TrueCrypt is discontinued, so legacy usage can carry maintenance, compatibility, and security uncertainty. <br>
Mitigation: Use this skill only when TrueCrypt support is intentionally required, note the discontinued status when relevant, and review generated commands before use. <br>
Risk: Passing passwords with /p can expose secrets in process listings, logs, or shell history. <br>
Mitigation: Prefer interactive password entry or keyfiles, and include /p only when the user explicitly accepts the exposure risk. <br>
Risk: Incorrect volume paths, device paths, or drive letters can mount or dismount the wrong target. <br>
Mitigation: Confirm the TrueCrypt executable, target volume, and drive letter first; start with install checks or command preparation before risky operations. <br>


## Reference(s): <br>
- [TrueCrypt command cookbook](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell and batch code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include install checks, command explanations, and cautious validation steps; avoids command-line passwords unless the user accepts that risk.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
