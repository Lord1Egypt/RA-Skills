## Description: <br>
Execute commands with superuser privileges. Use for system administration tasks requiring elevated permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to request or describe command execution that requires sudo-level privileges, including running commands as root or another configured user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables sudo-level command execution and the security summary says it lacks guardrails for powerful system changes. <br>
Mitigation: Install only when elevated system administration is intended, require explicit approval for each privileged command, and use contained or non-production environments unless strong operational controls are in place. <br>


## Reference(s): <br>
- [Sudo Tool on ClawHub](https://clawhub.ai/dinghaibin/sudo-tool) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Privileged commands should require explicit approval and an appropriate sudoers configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
