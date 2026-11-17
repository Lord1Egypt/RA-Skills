## Description:

ZT4AI Self-Audit helps agents audit OpenClaw workspaces, installed skills, and configurations against Zero Trust for AI risks including prompt injection, credential exposure, excessive privilege, behavioral manipulation, and integrity drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanarchytan](https://clawhub.ai/user/tanarchytan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and agent operators use this skill to audit OpenClaw skills and workspace configuration for Zero Trust for AI risks, produce remediation guidance, and establish integrity baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect broad OpenClaw workspace and skill locations, including files that may contain private paths or secrets.

Mitigation: Narrow the scan scope where possible and require owner confirmation before workspace-wide credential searches.

Risk: Audit reports and integrity baselines may persist sensitive paths or secret-hit context in memory.

Mitigation: Review report contents before storing or sharing, redact sensitive details, and avoid saving raw secret values.

Risk: The bundled integrity-check script needs review before its baseline results are treated as authoritative.

Mitigation: Treat integrity results as advisory until the script behavior is reviewed and corrected, then regenerate baselines after intentional changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/tanarchytan/skills/zt4ai-self-audit)
- [Risk Classification Guide](references/risk-classification.md)
- [Per-Skill Audit Checklist](references/audit-checklist.md)
- [Action Tiers - Graduated Trust Model](references/action-tiers.md)
- [ZT4AI Audit Report Template](references/report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown reports with inline shell commands, checklists, findings, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce persistent audit reports and integrity baselines in workspace memory when used as described.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
