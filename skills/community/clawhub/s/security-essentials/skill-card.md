## Description: <br>
Harden OpenClaw agent deployments with SSH lockdown, firewall rules, automated security audits, secret rotation reminders, RAM/process monitoring, and CVE alerting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nogravedev](https://clawhub.ai/user/nogravedev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review and harden OpenClaw agent hosts, including SSH, firewall, ports, secrets, processes, recurring audits, and incident-response playbooks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose sensitive host changes such as SSH or firewall edits, process termination, cron installation, or broad secret scans. <br>
Mitigation: Use read-only audit mode by default and require explicit approval before executing changes or scanning sensitive locations. <br>
Risk: Recurring reports or security findings could expose secrets, host details, or incident context if sent to an unsafe channel. <br>
Mitigation: Confirm the report destination, redact sensitive values, and avoid sending findings to broad or untrusted channels. <br>
Risk: The linked paid kit is outside the reviewed artifact. <br>
Mitigation: Review and scan the paid kit separately before installing or following its commands. <br>


## Reference(s): <br>
- [Security Essentials on ClawHub](https://clawhub.ai/nogravedev/security-essentials) <br>
- [Publisher profile](https://clawhub.ai/user/nogravedev) <br>
- [ClawKits website](https://clawkits.xyz) <br>
- [ClawKits Gumroad listing](https://clawkits.gumroad.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review command proposals before execution, especially for host security changes.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
