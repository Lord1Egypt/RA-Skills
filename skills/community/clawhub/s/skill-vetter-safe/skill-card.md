## Description:

Scans files in a skills directory for keyword-based security risk signals, assigns risk scores, and writes an audit report with installation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tlcyqj2023](https://clawhub.ai/user/tlcyqj2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill for a first-pass audit of local skill files before installation. It helps surface obvious code-execution, network-access, and privilege-related keywords, but should not be treated as a complete security gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may give misleading install advice because it relies on simple keyword matches.

Mitigation: Use its results as a triage signal and require human review before installing or approving any skill.

Risk: Instruction and documentation files may be missed by the current scan scope.

Mitigation: Review skill instruction files manually and update the scanner to inspect and disclose skipped file types.

Risk: Large or unexpected skill directories may consume excessive local resources during recursive scanning.

Mitigation: Run the scanner in a bounded sandbox and add explicit file count, size, and traversal limits before using it as a policy control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tlcyqj2023/skills/skill-vetter-safe)
- [ClawHub publisher profile](https://clawhub.ai/user/tlcyqj2023)
- [Source skill documentation](artifact/skill.md)
- [Scanner script](artifact/scan_skills.py)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Console text plus a JSON audit report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local skills/技能安全审计报告.json report when run against a skills directory.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
