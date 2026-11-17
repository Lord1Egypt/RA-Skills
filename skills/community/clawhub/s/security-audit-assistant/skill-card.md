## Description:

Conducts lightweight security baseline audits on OpenClaw-managed servers, identifies SSH, firewall, update, password, logging, service, and file-permission findings, and returns reports with remediation commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huoxinjiang](https://clawhub.ai/user/huoxinjiang)

### License/Terms of Use:

MIT-0

## Use Case:

DevOps engineers, sysadmins, and small business operators use this skill to run fast baseline checks across OpenClaw-managed nodes and collect human-readable findings for routine hardening or client-facing security reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests managed-node execution and cron authority.

Mitigation: Install only in environments where that authority is acceptable, and limit runs and schedules to intended OpenClaw-managed nodes.

Risk: The artifact ships an incomplete scanner with a mock executor, so reported audit results may not reflect real node state.

Mitigation: Treat results as unreliable until real OpenClaw node execution is verified in a test environment.

Risk: Suggested fixes include sudo changes to SSH, firewall, packages, and system permissions that can disrupt access or production behavior.

Mitigation: Review each command, make backups, validate SSH and firewall changes, and prepare rollback access before applying fixes.

## Reference(s):

- [Security Audit Assistant on ClawHub](https://clawhub.ai/huoxinjiang/skills/security-audit-assistant)
- [CIS Benchmark Summary](references/cis-benchmark-summary.md)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks/)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown, JSON, or plain text reports with inline shell remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May be scheduled through OpenClaw cron; remediation commands require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
