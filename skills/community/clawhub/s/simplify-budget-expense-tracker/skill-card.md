## Description: <br>
Logs, finds, updates, and deletes expenses, income, and recurring budget items in a Simplify Budget Google Sheet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serdarsalim](https://clawhub.ai/user/serdarsalim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to operate a personal budget tracker backed by the required Simplify Budget Google Sheet. It supports budget ledger reads and writes for expenses, income, recurring items, subscription-style entries, receipt logging, and monthly summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires editor access to a user's budget spreadsheet. <br>
Mitigation: Use a dedicated copy of the required sheet template, share it only with the intended Google service account, and keep the service-account key outside the repository with restrictive file permissions. <br>
Risk: Financial mutation paths can update or delete budget records, including recurring-payment records. <br>
Mitigation: Review the bundled commands before deployment and require explicit confirmation before destructive recurring-item deletes or other sensitive mutations. <br>
Risk: The package includes an unrelated local OpenClaw session-pruning script. <br>
Mitigation: Remove or ignore the session-pruning script unless that local maintenance behavior is intentionally needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/serdarsalim/simplify-budget-expense-tracker) <br>
- [Simplify Budget Template](https://docs.google.com/spreadsheets/d/1fA8lHlDC8bZKVHSWSGEGkXHNmVylqF0Ef2imI_2jkZ8/edit?gid=524897973#gid=524897973) <br>
- [Simplify Budget website](https://simplifybudget.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell commands, configuration values, and summarized script results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform Google Sheets reads and writes through bundled shell scripts when configured with spreadsheet and service-account credentials.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
