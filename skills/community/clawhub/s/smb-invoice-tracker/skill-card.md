## Description: <br>
Local invoice tracking ledger with optional LLM-generated reminder text for manually adding invoices, tracking outstanding or paid status, and generating cash flow reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzargona](https://clawhub.ai/user/jzargona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Freelancers and small businesses use this skill to maintain a local invoice ledger, review payment status, generate cash flow reports, and draft reminder text for manual review before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reminder history and Gmail authorization states may be mistaken for proof that a reminder was delivered or Gmail scanning is fully active. <br>
Mitigation: Verify delivery and integration status outside the skill before relying on reminder or Gmail-related state for business decisions. <br>
Risk: LLM reminder generation can send payer names, amounts, due dates, and notes to MiniMax when MINIMAX_API_KEY is configured. <br>
Mitigation: Avoid LLM reminder generation for sensitive invoices unless that data sharing is acceptable, and review generated reminder text before sending. <br>
Risk: The local invoice ledger may contain customer or business-sensitive data. <br>
Mitigation: Periodically review, protect, or delete the files stored under ~/.openclaw/smb-invoice-tracker/ according to the user's data-retention needs. <br>


## Reference(s): <br>
- [SMB Invoice Tracker listing](https://clawhub.ai/jzargona/skills/smb-invoice-tracker) <br>
- [Reference Docs](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Command-line text output plus local JSON ledger and configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes invoice and configuration data under ~/.openclaw/smb-invoice-tracker/; optional reminder generation may send invoice fields to MiniMax when MINIMAX_API_KEY is set.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
