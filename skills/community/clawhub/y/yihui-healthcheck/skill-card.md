## Description: <br>
Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1yihui](https://clawhub.ai/user/1yihui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, developers, and operators use this skill to assess host security posture, run OpenClaw security and version checks, choose a risk tolerance, and prepare staged hardening plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Host-hardening actions can change firewall, SSH, update, service, or scheduling behavior and may interrupt access if approved without confirming the access path. <br>
Mitigation: Confirm how the user connects, show exact commands and rollback steps, require explicit approval for each state-changing action, and verify access after changes. <br>
Risk: Scheduled audits, notifications, and local state or log files can expose operational details if scoped too broadly. <br>
Mitigation: Review cadence, notification targets, and output locations before scheduling, keep state scoped to this skill, and redact secrets from logs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with numbered choices and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans require explicit approval before state-changing commands and include rollback and verification guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
