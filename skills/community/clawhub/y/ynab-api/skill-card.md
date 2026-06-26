## Description: <br>
YNAB (You Need A Budget) budget management via API for adding transactions, tracking goals, monitoring spending, creating transfers, and generating budget reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f-liva](https://clawhub.ai/user/f-liva) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent manage a personal YNAB budget, including budget checks, spending analysis, goal tracking, transfers, scheduled transaction reports, and transaction entry. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live YNAB budget records, including adding transactions and creating transfers. <br>
Mitigation: Before any add, transfer, or approval action, verify the exact account, payee, date, amount, category, and whether YNAB should be used. <br>
Risk: The YNAB token and budget reports can expose sensitive personal financial information. <br>
Mitigation: Keep the token private, restrict config file permissions, avoid logging full API keys, and treat scheduled report output as sensitive. <br>
Risk: Broad finance prompts could cause unintended budget operations. <br>
Mitigation: Review proposed changes before execution and require explicit confirmation for actions that modify records. <br>


## Reference(s): <br>
- [YNAB API Skill for Claude Code](artifact/README.md) <br>
- [YNAB API Guide](artifact/references/api-guide.md) <br>
- [Category Examples](artifact/references/category-examples.md) <br>
- [YNAB API documentation](https://api.ynab.com) <br>
- [YNAB developer settings](https://app.ynab.com/settings/developer) <br>
- [ClawHub skill page](https://clawhub.ai/f-liva/ynab-api) <br>
- [Publisher profile](https://clawhub.ai/user/f-liva) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and terminal stdout, with JSON returned by helper scripts for YNAB API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, a YNAB API token, and a YNAB budget ID; some scripts can create or approve live budget records.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata and skill.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
