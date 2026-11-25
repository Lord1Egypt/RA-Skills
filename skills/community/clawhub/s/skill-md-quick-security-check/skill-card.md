## Description:

Runs a fast five-pattern security check on a third-party SKILL.md before you install it: remote scripts piped into a shell, destructive commands, wildcard tool approvals, hidden Unicode, and credential access or data exfiltration. Gives a short safe-to-read, fix-first, or do-not-install result with the lines that triggered it. Use when you want a quick first pass on a skill you downloaded; for a full audit with a semantic purpose review and a written report, use the SKILL.md Security Auditor instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanqingsong2024](https://clawhub.ai/user/yuanqingsong2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and people evaluating downloaded agent skills use this check for a quick first pass before installation. It identifies matches for five mechanical security patterns and returns a short result with the triggering line numbers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scan has medium confidence and partial coverage because a local reference could not be resolved.

Mitigation: Review the skill and its referenced material yourself before installing it; a benign scan result does not mean risk-free.

Risk: Mechanical pattern checks can miss harmful instructions written in plain language.

Mitigation: Read the skill yourself and use a semantic review for a fuller audit.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/yuanqingsong2024/skills/skill-md-quick-security-check)
- [skillmdvalidator.com companion checker](https://skillmdvalidator.com)
- [SKILL.md Security Auditor](https://skillhq.dev/skills/yuanqingsong/skill-md-security-auditor)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Short prose result with pattern findings and line numbers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Five mechanical checks; includes a brief caution that passing the checks does not rule out harmful instructions in plain language.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
