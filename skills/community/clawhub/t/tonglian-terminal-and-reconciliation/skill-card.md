## Description: <br>
Guides an agent through Tonglian terminal applications, merchant additions, VIP reconciliation setup, and processing-fee invoice requests using fixed templates, recipient rules, and user confirmation before outbound actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations employees use this skill to prepare Tonglian terminal request spreadsheets, VIP reconciliation configuration spreadsheets, related email drafts, and Feishu delivery/task steps for payment operations workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can involve customer billing, merchant, terminal, contact, and invoice data. <br>
Mitigation: Review source data before use, minimize shared fields, and verify merchant, terminal, phone, and amount values against approved records before creating spreadsheets or outbound messages. <br>
Risk: The workflow can guide the agent to send files or emails to named recipients and create Feishu tasks. <br>
Mitigation: Confirm recipients, templates, attachments, and task details with the user before any message, email, file delivery, or task creation is executed. <br>
Risk: Template-dependent spreadsheets may be wrong if fixed columns, formatting, or identifier types are changed. <br>
Mitigation: Use the approved templates, preserve fixed column layouts and styles, store numeric identifiers as text, and review generated files before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/skills/tonglian-terminal-and-reconciliation) <br>
- [Source skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown-style workflow guidance, generated email text, Excel spreadsheet files, and task/message instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outbound email, file delivery, and task creation steps require explicit user confirmation before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
