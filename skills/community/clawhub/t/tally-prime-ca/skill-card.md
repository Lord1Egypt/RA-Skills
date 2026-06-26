## Description: <br>
Tally Prime CA receives structured accounting JSON, posts vouchers to a locally running TallyPrime instance, reads accounting reports, manages masters, and generates invoice or receipt PDFs through the tallyca CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meetpaladiya44](https://clawhub.ai/user/meetpaladiya44) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External accountants, chartered accountants, and accounting operators use this skill to move validated voucher data into TallyPrime, create or update required accounting masters, review standard reports, and generate GST-compliant PDFs. It is intended for controlled Tally environments where write actions are approved before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live accounting data, including creating, altering, importing, or cancelling Tally entries. <br>
Mitigation: Use it only in a controlled Tally environment with backups, least-privilege access, and explicit operator approval for every write action. <br>
Risk: The skill depends on host-level CLI installation and a Tally bridge or tunnel endpoint. <br>
Mitigation: Pin and preinstall tallyca, avoid sudo package installation from agent sessions, and restrict TALLY_URL and bridge access to trusted endpoints. <br>
Risk: Accounting reports and company exports may expose sensitive financial data. <br>
Mitigation: Minimize full company, account, and report exports and share only the fields needed for the current accounting task. <br>


## Reference(s): <br>
- [Bridge Input Schema](artifact/reference/bridge-input.md) <br>
- [Masters](artifact/reference/masters.md) <br>
- [Vouchers](artifact/reference/vouchers.md) <br>
- [Reports and Data Export](artifact/reference/reports.md) <br>
- [Inventory](artifact/reference/inventory.md) <br>
- [Errors](artifact/reference/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON summaries, XML request templates, and generated PDF files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TALLY_URL and a reachable local TallyPrime XML-over-HTTP endpoint; PDF flows require the tallyca CLI.] <br>

## Skill Version(s): <br>
1.0.9 (source: evidence release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
