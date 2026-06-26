## Description: <br>
Executes SSH commands on remote servers using password or key-based authentication, with error handling and logging for command execution results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xlbbb-cn](https://clawhub.ai/user/xlbbb-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run a single command on an authorized SSH-accessible server for remote administration, troubleshooting, or maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad remote command execution capability on SSH-accessible systems. <br>
Mitigation: Use least-privilege SSH accounts and require explicit human approval for commands that change files, services, permissions, deployments, or data. <br>
Risk: Weak default host verification can allow connection to an untrusted host. <br>
Mitigation: Enable --strict-host-key and maintain known_hosts entries for approved servers. <br>
Risk: Passwords, private-key passphrases, command text, or command output may expose sensitive information in command lines or logs. <br>
Mitigation: Prefer key-based authentication, avoid passing secrets on the command line, and protect logs that contain commands or remote output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xlbbb-cn/sshexec) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Console text with stdout, stderr, logs, and remote exit status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Executes one remote command per invocation and returns the remote command exit code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
