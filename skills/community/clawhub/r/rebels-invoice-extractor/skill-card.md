## Description:

Extract structured data from invoice and receipt PDFs or images, then output JSON or CSV and maintain a running expense ledger.

This skill is ready for commercial/non-commercial use.

## Publisher:

[99rebels](https://clawhub.ai/user/99rebels)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as freelancers, small businesses, and contractors use this skill to extract invoice and receipt data, categorize expenses, maintain a CSV ledger, and prepare accounting exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change financial records in a local expense ledger.

Mitigation: Review extracted entries before adding them, keep backups, and use edit, delete, and undo commands carefully.

Risk: The skill can save web-discovered export presets that may not match the target accounting platform.

Mitigation: Check platform CSV requirements before saving or using a discovered export preset.

Risk: Generated CSV files may be unsafe when opened in spreadsheet software.

Mitigation: Treat generated CSV files as untrusted and review them before opening, importing, or sharing.

## Reference(s):

- [Configuration Reference](references/configuration.md)
- [Platform Formatting Examples](references/formatting.md)
- [Implementation Notes](references/notes.md)
- [Invoice Extractor Product Plan](references/product-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/99rebels/skills/rebels-invoice-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown confirmations with JSON entries, CSV ledger/export files, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before ledger writes and can use local configuration for categories, defaults, ledger path, and export presets.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
