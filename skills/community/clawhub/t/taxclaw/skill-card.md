## Description:

TaxClaw extracts fields from supported tax documents into structured JSON or CSV for accountants and tax software, locally by default, and does not prepare or file returns or provide tax advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dougbutdorf](https://clawhub.ai/user/dougbutdorf)

### License/Terms of Use:

MIT

## Use Case:

Taxpayers, accountants, and tax software workflows use TaxClaw to extract printed fields from supported tax documents, review uncertain values, and export structured data. It supports data extraction and review, not tax preparation or tax advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI extraction can produce incorrect tax-form values, and the security review flags tax calculations and review safeguards as a concern.

Mitigation: Check every extracted value against the original document before relying on or exporting it; use a qualified tax professional for tax advice.

Risk: Tax documents contain sensitive identifiers and may leave the device when a cloud or hosted backend is selected.

Mitigation: Use the local backend by default; review the selected provider's privacy terms and explicitly consent before sending documents to a cloud service. Keep identifier masking enabled for agent results.

Risk: Deletion safeguards were not confirmed by the partial security scan, and deletion removes TaxClaw's stored document and extracted data.

Mitigation: Confirm the document ID and ask the user before deletion; export data first if it needs to be retained.

Risk: The release includes an install example that runs a remote script.

Mitigation: Independently inspect and verify the remote script before running the install command.

## Reference(s):

- [TaxClaw project homepage (declared in skill metadata)](https://github.com/DougButdorf/TaxClaw)
- [TaxClaw ClawHub release page](https://clawhub.ai/dougbutdorf/skills/taxclaw)
- [TaxClaw Cloud privacy information](https://mcp.taxclaw.net/privacy)

## Skill Output:

**Output Type(s):** [JSON, CSV, Guidance]

**Output Format:** [Structured JSON or CSV exports, with CLI or MCP status and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted values include review indicators; verify them against the original documents before use.]

## Skill Version(s):

1.1.0 (source: artifact/SKILL.md frontmatter, CHANGELOG.md, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
