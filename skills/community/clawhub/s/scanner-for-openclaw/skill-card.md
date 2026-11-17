## Description:

Scans local OpenClaw configuration files for insecure network, channel-policy, and tool-permission settings, then reports findings with remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoowii](https://clawhub.ai/user/zoowii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw administrators use this skill to audit local OpenClaw deployments before production exposure, after configuration changes, or during periodic security checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw configuration files that may contain sensitive deployment settings.

Mitigation: Install only when this access is acceptable, run without elevated privileges, and review generated reports before sharing them.

Risk: Audit reports can expose security posture details if written outside the intended workspace.

Mitigation: Keep output paths inside the workspace and use security_report_*.md names.

Risk: Manual packaging on shared systems may create avoidable operational exposure.

Mitigation: Use the normal ClawHub installation path and do not manually run package_skill.py on shared systems.

## Reference(s):

- [Config Security Scanner ClawHub Page](https://clawhub.ai/zoowii/skills/scanner-for-openclaw)
- [Clawdis Homepage](https://github.com/openclaw/openclaw/tree/main/skills/openclaw-security-scanner)
- [Permission Management](references/permission-management.md)
- [Remediation Playbook](references/remediation-playbook.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown security audit report with concise command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write security_report_*.md in the workspace; reads local OpenClaw configuration files only.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
