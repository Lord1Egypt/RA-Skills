## Description: <br>
Full-service CA skill for locally running TallyPrime that reads accounting reports, extracts invoice data, generates PDFs, and posts or updates vouchers after user confirmation and review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhi152003](https://clawhub.ai/user/abhi152003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External accounting users and CA teams use this skill to work with a local TallyPrime instance for invoice extraction, GST-aware voucher posting, master setup, report export, outstandings review, and PDF generation. The skill is intended for supervised workflows where users confirm company context and write actions before accounting data is changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read from and write to live accounting data in a local TallyPrime company. <br>
Mitigation: Use it only in supervised workflows, confirm the exact company before any write action, and require explicit user approval before broad exports, master creation, voucher posting, alteration, or cancellation. <br>
Risk: A wrong or untrusted TALLY_URL could connect the agent to an unintended accounting instance. <br>
Mitigation: Keep TALLY_URL pointed to a trusted local TallyPrime server and verify connectivity before acting. <br>
Risk: The skill includes package and system installation or upgrade steps for PDF generation dependencies. <br>
Mitigation: Do not let the agent install or upgrade npm, OS, Playwright, or Chromium packages without administrator approval. <br>
Risk: Voucher creation or updates can be incorrect if ledgers, GST fields, voucher class, company context, or totals are not verified. <br>
Mitigation: Follow the documented preflight checks, create or confirm required masters first, and fetch the posted entry back from Tally for review before telling the user it is complete. <br>


## Reference(s): <br>
- [Tally Skill ClawHub page](https://clawhub.ai/abhi152003/tally-skill) <br>
- [Reports and Data Export reference](reference/reports.md) <br>
- [Vouchers reference](reference/vouchers.md) <br>
- [Masters reference](reference/masters.md) <br>
- [Inventory reference](reference/inventory.md) <br>
- [Errors and Troubleshooting reference](reference/errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with accounting summaries, command snippets, XML templates, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a trusted local TallyPrime endpoint through TALLY_URL and the documented curl, tallyca, and scribe tools.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
