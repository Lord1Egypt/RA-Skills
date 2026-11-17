## Description:

Upgrade Guardian is a cognitive protocol for safely managing and auditing OpenClaw upgrades by analyzing configuration-level risks and runtime behavioral shifts with semantic changelog analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[radonx](https://clawhub.ai/user/radonx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to review OpenClaw release notes, compare possible changes against their configurations and workflows, and produce upgrade audit, mitigation, and verification plans before and after upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated upgrade guidance can include backup cleanup, file writes, log or session inspection, and background monitoring commands.

Mitigation: Review each command before execution, prefer config-only backups when appropriate, and avoid running deletion or long-running monitoring commands unless the operator explicitly approves them.

Risk: Proposed configuration changes may alter OpenClaw authentication, routing, session, provider, or workflow behavior.

Mitigation: Treat configuration edits as proposals, test high-priority changes in a staging or controlled environment, and run the verification checklist before considering the upgrade complete.

Risk: Optional monitoring examples may create scripts or logs in the user's home directory.

Mitigation: Use workspace-relative report locations where practical and choose one-shot validation when persistent background monitoring is not required.

## Reference(s):

- [Upgrade Guardian on ClawHub](https://clawhub.ai/radonx/skills/upgrade-guardian)
- [Upgrade Guardian README](README.md)
- [Changelog Analysis Patterns for Silent Breaking Changes](references/changelog_analysis_patterns.md)
- [Risk Categories for Upgrade Analysis](references/RISK_CATEGORIES.md)
- [Upgrade Audit Report Template](references/AUDIT_REPORT_TEMPLATE.md)
- [Common Verification Checklist for OpenClaw Upgrades](references/VERIFICATION_CHECKLIST.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown audit reports with checklists, verification steps, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose configuration changes or commands for operator review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
