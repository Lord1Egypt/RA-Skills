## Description:

Skill Guard scans local AI skill files for heuristic risk patterns before installation, use, or audit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaibuer](https://clawhub.ai/user/huaibuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan local AI skill packages before installing unknown skills, evaluating third-party code, auditing skill behavior, or running untrusted code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can produce misleading safe results because it may miss malicious skill instructions in Markdown files or unreadable files.

Mitigation: Use it only as a lightweight heuristic checker and manually review important skill instructions and unreadable files before relying on the result.

Risk: Users may install or run a different package version than the one represented by this evidence.

Mitigation: Confirm the exact package version and release metadata before installing or executing the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huaibuer/skills/skill-guard-waai)
- [Publisher Profile](https://clawhub.ai/user/huaibuer)

## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Guidance]

**Output Format:** [JSON-like scan report and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports status, severity level, aggregate counts, and up to 15 detected risk details.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter metadata reports 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
