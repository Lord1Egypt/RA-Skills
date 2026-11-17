## Description:

TaxWise is a China-focused tax and bookkeeping assistant for small and midsize businesses, with tools for tax-rate lookup, invoice extraction, bookkeeping, filing drafts, financial analysis, compliance checks, and tax-planning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keybryant](https://clawhub.ai/user/keybryant)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators can use this skill to run China-oriented tax-rate queries, invoice recognition, local bookkeeping, draft tax calculations, financial summaries, compliance checks, and tax-planning prompts for small and midsize businesses. Outputs should be reviewed against current tax authority guidance before filing or operational use.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sensitive financial records may be stored as local plaintext JSON in the skill directory.

Mitigation: Use only non-sensitive test data unless the storage location is access-controlled, encrypted, backed up, and covered by the user's data-retention practices.

Risk: Tax calculations, period filters, and compliance checks may be incomplete or approximate.

Mitigation: Treat generated filing drafts, compliance warnings, and planning suggestions as review aids, then verify them against current tax authority rules and a qualified tax professional before submission.

Risk: Invoice OCR and some external data integrations are mock implementations by default.

Mitigation: Do not rely on mock OCR or static tax data for production decisions; replace mocks with approved OCR, tax-rate, and business-credit APIs before production use.

Risk: Bookkeeping records can be deleted through the command-line tool.

Mitigation: Review delete actions before execution and keep backups or audit exports for records that must be retained.

## Reference(s):

- [China Tax Rates Reference](references/china_tax_rates.md)
- [ClawHub Skill Page](https://clawhub.ai/keybryant/skills/taxwise)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Command-line text, JSON, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some tools read and write local bookkeeping records in JSON; invoice OCR and live data integrations are mocked until replaced with production APIs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
