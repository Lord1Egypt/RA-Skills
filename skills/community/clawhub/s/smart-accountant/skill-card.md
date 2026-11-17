## Description:

Provides double-entry accounting support with GST compliance checks, audit controls, period closing guidance, journal entry workflows, and financial reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dakshhmehta](https://clawhub.ai/user/dakshhmehta)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and agents use this skill to classify transactions, prepare balanced journal entries, run GST validation, manage ledger operations, perform closing and reconciliation workflows, and generate financial reports.

### Deployment Geography for Use:

India-focused; general accounting guidance requires local tax review before use elsewhere.

## Known Risks and Mitigations:

Risk: Posting and correction scripts can change local SQLite financial records without reliably enforcing the stated approval and audit controls.

Mitigation: Use only in a test or non-production accounting workspace until approval enforcement, dry-run or confirmation gates, read-only preview behavior, and stronger audit controls are added.

Risk: Rectification and reversal flows may not provide atomic correction behavior or reversal idempotency.

Mitigation: Add transaction-wrapped reverse-and-repost operations, idempotency checks, unique request identifiers, and independent review before applying corrections.

Risk: Period and GST handling can depend on date-aware configuration and jurisdiction-specific accounting review.

Mitigation: Maintain current period and tax configuration, treat generated postings as reviewable previews, and require qualified accounting review before relying on outputs for production records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dakshhmehta/skills/smart-accountant)
- [Artifact skill index](artifact/SKILL.md)
- [GST guard guidance](artifact/gst_guard.md)
- [Database tooling guidance](artifact/db_tool.md)
- [Audit control rulebook](artifact/audit_rule.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and Node.js shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local SQLite ledger scripts when installed; financial postings should be previewed and approved before database writes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
