## Description:

Trade Analyzer reviews trading records from CSV or cleaned text, computes performance and consistency metrics, and produces a Markdown trading recap report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[misso0513](https://clawhub.ai/user/misso0513)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users and developers use this skill to review stock trading logs, summarize basic performance statistics, and generate strategy recap guidance. Reports should be reviewed by a human and should not be treated as trusted financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the analyzer currently cannot run due to a syntax error.

Mitigation: Fix and test analyzer.py before relying on generated reports.

Risk: The security evidence says Excel support is overstated.

Mitigation: Treat CSV and text as the supported paths unless Excel handling is separately verified.

Risk: Generated Markdown reports may be mistaken for trusted financial advice or rendered unsafely from untrusted records.

Mitigation: Review reports before acting on them and sanitize any rendered content from user-supplied trade records.

## Reference(s):

- [Trade Analyzer ClawHub page](https://clawhub.ai/misso0513/skills/trade-analyzer)
- [Publisher profile](https://clawhub.ai/user/misso0513)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with tables, text analysis, and code-facing helper outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local CSV or text trade records and emits summary metrics, strategy consistency observations, and improvement suggestions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
