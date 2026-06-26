## Description: <br>
Post purchase, sales, and bank entries in TallyPrime with GST voucher classes, and generate sales invoice PDFs via tallyca. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhi152003](https://clawhub.ai/user/abhi152003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accountants, operators, and agents working with a local TallyPrime company use this skill to prepare, post, and review purchase, sales, and bank vouchers with GST handling. The skill also helps generate sales invoice PDFs from TallyPrime-backed data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write persistent voucher and inventory-master changes to a live TallyPrime company. <br>
Mitigation: Use a backup or test company first, confirm the exact company and voucher details before posting, and review the posted entry after creation. <br>
Risk: Incorrect ledgers, stock items, tax fields, or voucher classes could produce inaccurate accounting records. <br>
Mitigation: Require the agent to show ledgers, stock items, UOMs, stock groups, godowns, amounts, GST fields, and voucher class decisions before each write. <br>
Risk: Automatic master-data creation can alter the accounting setup beyond a single voucher entry. <br>
Mitigation: Approve each ledger, stock group, unit, stock item, or godown creation separately. <br>


## Reference(s): <br>
- [TallyPrime Entry Skill](SKILL.md) <br>
- [Bank Statement Vouchers](reference/bank.md) <br>
- [Inventory Masters](reference/inventory.md) <br>
- [Ledger Masters](reference/ledgers.md) <br>
- [Purchase Vouchers](reference/purchase.md) <br>
- [Reports and Post-Entry Review](reference/reports.md) <br>
- [Sales Vouchers](reference/sales.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/abhi152003/tally-prime-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with XML examples and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce accounting-entry summaries, TallyPrime XML payload patterns, CLI commands, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: target metadata, frontmatter, and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
