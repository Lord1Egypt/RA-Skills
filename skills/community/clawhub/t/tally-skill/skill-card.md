## Description:

Full-service CA skill for locally running TallyPrime that reads accounting reports, extracts invoice data, generates PDFs, and posts or updates vouchers through TallyPrime XML-over-HTTP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhi152003](https://clawhub.ai/user/abhi152003)

### License/Terms of Use:

MIT-0

## Use Case:

External accountants, CAs, and business operators use this skill to work with local TallyPrime company data: read reports, verify ledgers, create or update accounting masters, post vouchers, import bank-statement transactions, and generate invoice or receipt PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive accounting and financial records through a local TallyPrime endpoint.

Mitigation: Use only with a trusted local endpoint, preferably localhost, and avoid remote HTTP endpoints unless approved and secured by an administrator.

Risk: The skill can create, alter, cancel, or bulk import accounting records.

Mitigation: Require explicit user approval and use a backup or test company before write operations involving vouchers, masters, inventory, or bank statements.

Risk: Install and upgrade instructions can change the host environment through global package installation or latest-version upgrades.

Mitigation: Preinstall and pin tallyca and scribe through the normal administrative process instead of relying on agent-run global installs or @latest upgrades.

Risk: PDF generation setup may require browser or system dependency changes on shared or production machines.

Mitigation: Prefer the pdfmake backend before using sudo or Playwright dependency setup in shared or production environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/abhi152003/skills/tally-skill)
- [Reports and Data Export](reference/reports.md)
- [Voucher Templates](reference/vouchers.md)
- [Masters Templates](reference/masters.md)
- [Inventory Templates](reference/inventory.md)
- [Errors and Troubleshooting](reference/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, XML templates, extracted accounting summaries, and generated file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local TallyPrime endpoint configured through TALLY_URL and the curl, tallyca, and scribe command-line tools.]

## Skill Version(s):

1.0.11 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
