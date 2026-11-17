## Description:

自主安全审计 - 定期检查系统安全、发现风险、生成报告

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwe](https://clawhub.ai/user/bandwe)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run structured OpenClaw security audits, inspect configuration, permissions, logs, and network posture, and generate risk-scored remediation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect configuration, logs, network details, and credential-related files that contain sensitive data.

Mitigation: Review the skill before use, limit audit scope to intended systems, and run it only where such inspection is authorized.

Risk: Audit commands or log searches may expose API keys, sensitive log entries, host details, or retained audit history.

Mitigation: Prefer checks that verify key presence and file permissions without printing secret values, redact log matches, and avoid saving history unless explicitly enabled.

Risk: The skill describes outbound network checks and scheduled audits that may run without clear operator consent.

Mitigation: Require confirmation before outbound network calls, and keep scheduled audits, notifications, and saved history disabled until intentionally configured.

## Reference(s):

- [Security Audit Hand on ClawHub](https://clawhub.ai/bandwe/skills/security-audit-hand)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk scores, prioritized remediation plans, audit checklists, and dashboard metrics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
