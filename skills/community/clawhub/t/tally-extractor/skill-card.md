## Description:

Parses invoices and bills from PDFs, images, or messages, extracts structured accounting data, validates key tax fields, and forwards canonical JSON to a configured bridge for Tally entry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meetpaladiya44](https://clawhub.ai/user/meetpaladiya44)

### License/Terms of Use:

MIT-0

## Use Case:

Accountants, CAs, and finance operators use this skill to turn invoice PDFs, images, or chat messages into validated voucher payloads for Tally workflows. It is intended to reduce manual entry while preserving checks for GSTINs, HSN codes, tax math, totals, and low-confidence fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends invoice contents and tax identifiers to a configured bridge.

Mitigation: Install it only when the bridge endpoint and operators are trusted, and protect and rotate the bridge credentials.

Risk: The workflow can cause Tally vouchers, and possibly ledgers, to be created through Instance B.

Mitigation: Require explicit human approval before posting accounting entries, especially for low-confidence extraction results.

## Reference(s):

- [Extraction Schema](reference/extraction-schema.md)
- [Bridge HTTP Contract](reference/bridge.md)
- [Telegram Reply Templates](reference/prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces canonical voucher JSON for bridge submission and human-facing status or clarification messages.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
