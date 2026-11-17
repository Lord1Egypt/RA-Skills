## Description:

元安 audits AI skills for malicious patterns, checks Windows and Linux security baselines, and scans education files for student data risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT

## Use Case:

Developers, system administrators, and education staff use the skill to review AI skill directories, check system security settings, and find student data risks in education files before sharing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner may miss disguised threats because some discovery and filename exemptions need review.

Mitigation: Treat a clean scan as an initial signal, review the scanner's coverage, and seek independent review before trusting results.

Risk: Reports may expose student information despite the intended masking.

Mitigation: Avoid real student records until masking is corrected, and inspect reports before sharing them.

Risk: Installation targets and remotely fetched releases may introduce unreviewed changes.

Mitigation: Choose installation targets explicitly, pin a reviewed package version, and review releases that were not assessed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-security-audit)
- [Project homepage](https://github.com/YottaMeta/yotta-security-audit)
- [Threat patterns](references/threat-patterns.md)
- [System baseline checks](references/system-baseline.md)
- [Student data scan guidance](references/student-data-scan.md)
- [Remediation guidance](references/remediation-guide.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Text, Markdown, or JSON audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include findings and locations; student data examples are masked.]

## Skill Version(s):

0.3.3 (source: frontmatter, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
