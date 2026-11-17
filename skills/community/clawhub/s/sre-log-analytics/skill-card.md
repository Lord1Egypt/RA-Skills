## Description:

Analyze system logs by time range using the Google SRE framework to summarize operations, classify errors, score health, and suggest improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roryyu](https://clawhub.ai/user/roryyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SRE teams use this skill to inspect system or application logs for a chosen time range, aggregate important failures, assess service health, and produce an incident-ready analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log reports may include sensitive log content, secrets, personal data, or raw samples.

Mitigation: Use explicit log paths and time ranges, redact secrets and personal data before report generation, and review any included samples before sharing.

Risk: Broad log access can expose unrelated system data.

Mitigation: Scope analysis to the minimum required logs and time windows instead of broad system-wide collection.

Risk: Shared reports may disclose sensitive operational details.

Mitigation: Check sanitized content and recipient permissions before exporting or sharing reports to cloud documents.

## Reference(s):

- [Google SRE Core Principles](artifact/references/sre-principles.md)
- [System Log Analysis Report Template](artifact/references/report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/roryyu/skills/sre-log-analytics)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with structured sections and optional inline log samples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include health scores, exception aggregation, and short-, mid-, and long-term recommendations.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
