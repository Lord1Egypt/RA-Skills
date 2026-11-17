## Description:

Tax helps individuals, freelancers, and small businesses locally capture tax-relevant facts, track possible missing documents, and generate CPA-ready handoff summaries without providing tax advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticio](https://clawhub.ai/user/agenticio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Tax to organize year-round tax documents, expenses, notices, and CPA questions. The skill supports recordkeeping, possible missing-item checks, and professional handoff preparation while leaving tax treatment and filing decisions to licensed professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive tax records are stored as local plaintext files under ~/.openclaw/workspace/memory/tax/.

Mitigation: Use a private account or encrypted disk, check local file permissions, and avoid syncing the tax memory folder to broad backups or shared storage.

Risk: Generated CSV files may expose users to spreadsheet-related risks when opened.

Mitigation: Treat generated CSV files as untrusted, review them before opening in spreadsheet software, and avoid sharing them beyond the intended professional review workflow.

## Reference(s):

- [CPA Handoff](references/cpa-handoff.md)
- [Cross-Year Memory](references/cross-year-memory.md)
- [Facts vs. Judgments](references/fact-vs-judgment.md)
- [Recordkeeping](references/recordkeeping.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, CSV, JSON, Shell commands, Guidance]

**Output Format:** [Plain text responses, local JSON records, Markdown summaries, and CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores tax memory and generated summaries as local plaintext files under ~/.openclaw/workspace/memory/tax/ when scripts are run.]

## Skill Version(s):

4.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
