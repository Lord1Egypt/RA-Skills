## Description:

Analyzes incoming call content for multi-dimensional risk, identifies scam scripts, assesses fraud risk levels, and generates an Anti-Fraud Guardian analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users can submit call audio, a recording URL, or a transcript to review potential scam patterns and receive a structured risk report. They can also retrieve previously generated reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious due to a reported mismatch between its advertised call fraud analysis and other capabilities, plus privacy, identity, and behavior-control concerns. The scan was partial, so evidence is incomplete.

Mitigation: Follow the scanner guidance and do not install until remote processing, account setup, credential handling, history retrieval, and export-only behavior are clarified; review the unresolved reference because the scan was partial.

## Reference(s):

- [API documentation](references/api_doc.md)
- [Skill demo](https://lifeemergence.com/sample.html)
- [ClawHub release page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fraud-call-identification-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Text, JSON, Report links]

**Output Format:** [Structured analysis text or JSON, with report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save analysis output to a file; historical reports are returned as structured data.]

## Skill Version(s):

9.9.22 (source: server-resolved ClawHub release metadata; artifact frontmatter lists 1.0.25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
