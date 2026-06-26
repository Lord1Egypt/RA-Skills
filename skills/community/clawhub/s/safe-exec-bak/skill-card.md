## Description: <br>
Safe Exec.Bak helps OpenClaw agents route shell commands through local risk detection, approval requests, and audit logging before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gjc0909](https://clawhub.ai/user/gjc0909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when agents need to execute shell commands that may delete data, modify system configuration, use elevated privileges, or otherwise require human oversight. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary local shell commands, including system-changing commands. <br>
Mitigation: Review commands before approval, require explicit human approval for sudo, deletion, firewall, service, and other system-changing operations, and install only in environments where local command execution is acceptable. <br>
Risk: Approval controls can be weakened or bypassed through agent and non-interactive use, environment variables, or pending request files. <br>
Mitigation: Keep SAFE_EXEC_AUTO_CONFIRM unset, avoid agent-driven use of safe-exec-approve, and periodically inspect pending requests and configuration files. <br>
Risk: The local audit log supports traceability but should not be treated as tamper-proof. <br>
Mitigation: Use the audit log as operational evidence only, protect the host account and log path, and pair it with external controls when stronger audit integrity is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gjc0909/safe-exec-bak) <br>
- [Install source: Clone from GitHub](https://github.com/OTTTTTO/safe-exec.git) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local approval, listing, rejection, and audit-log workflows for shell command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
