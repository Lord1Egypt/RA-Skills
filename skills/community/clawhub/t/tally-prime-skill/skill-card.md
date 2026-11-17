## Description:

Post purchase, sales, and bank entries in TallyPrime with GST voucher classes and generate sales invoice PDFs via tallyca.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhi152003](https://clawhub.ai/user/abhi152003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and accountants use this skill to prepare TallyPrime purchase, sales, and bank entries, verify required ledgers and stock items, and generate sales invoice PDFs from Tally data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make persistent changes to TallyPrime accounting data.

Mitigation: Review and approve every proposed voucher or master creation before allowing the skill to post it.

Risk: Accounting data is sent to the HTTP endpoint configured in TALLY_URL.

Mitigation: Keep TALLY_URL pointed only at a trusted local TallyPrime instance.

Risk: The documented tallyca install path may install an unpinned global npm package.

Mitigation: Install only a deliberately selected and trusted tallyca version.

## Reference(s):

- [Bank Statement Vouchers](artifact/reference/bank.md)
- [Inventory Masters](artifact/reference/inventory.md)
- [Ledgers](artifact/reference/ledgers.md)
- [Purchase Vouchers](artifact/reference/purchase.md)
- [Reports](artifact/reference/reports.md)
- [Sales Vouchers](artifact/reference/sales.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with XML templates and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted TALLY_URL endpoint and the curl, tallyca, and scribe CLIs for documented workflows.]

## Skill Version(s):

1.0.1 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
