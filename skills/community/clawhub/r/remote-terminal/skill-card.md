## Description: <br>
Remote Terminal helps agents connect to remote Linux servers and execute commands through SSH, Telnet, or web terminals with host management, logging, and safety checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckaorceu](https://clawhub.ai/user/ckaorceu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and administrators use this skill to run commands on remote Linux hosts, manage host aliases, perform common service and system checks, and troubleshoot SSH connectivity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run commands on remote servers, including production or multi-host operations. <br>
Mitigation: Review every production or multi-host command before execution, require explicit confirmation for dangerous commands, and use least-privilege accounts. <br>
Risk: Password authentication and host inventory files can expose sensitive credentials or server details. <br>
Mitigation: Prefer SSH keys and SSH config aliases, avoid password mode, do not store passwords in hosts.json, and protect host inventory files. <br>
Risk: Disabling or weakening host-key verification can expose connections to interception. <br>
Mitigation: Keep host-key verification enabled, verify host fingerprints before first use, and avoid disabling StrictHostKeyChecking for production hosts. <br>
Risk: Local logs may reveal hostnames, commands, and operational activity. <br>
Mitigation: Treat remote-terminal logs as sensitive files, restrict filesystem permissions, and review or rotate logs according to operational policy. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckaorceu/remote-terminal) <br>
- [SSH Config Guide](references/ssh_config_guide.md) <br>
- [Security Best Practices for Remote Terminal Access](references/security_best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration snippets, and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote command stdout, stderr, exit codes, execution timing, host inventory details, and audit-log guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
