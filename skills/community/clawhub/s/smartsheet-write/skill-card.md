## Description: <br>
Writes user-approved add or update records to Enterprise WeChat Smart Sheets through a provided webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Roollond](https://clawhub.ai/user/Roollond) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and teams use this skill to capture tasks, bugs, customer records, meeting notes, orders, approvals, and similar structured business data in WeCom Smart Sheets after confirming the destination table and fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Records could be written to the wrong Smart Sheet if the destination table or saved webhook is assumed incorrectly. <br>
Mitigation: Confirm the target table and require user approval before the first reuse of a saved webhook in each conversation. <br>
Risk: Saved webhook URLs function as write credentials for their tables. <br>
Mitigation: Save webhooks only with user consent, avoid saving highly sensitive table webhooks unless needed, and rotate or delete them if exposed or no longer used. <br>
Risk: Incorrect field IDs, option labels, dates, or record IDs can cause failed writes or inaccurate records. <br>
Mitigation: Build payloads from the table schema, ask when field mapping is ambiguous, and confirm important writes before sending. <br>
Risk: Large batches can exceed Smart Sheet rate limits. <br>
Mitigation: Batch large writes and keep each batch within the documented per-sheet and per-document limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Roollond/smartsheet-write) <br>
- [字段类型格式规范](references/field-types.md) <br>
- [真实场景示例](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON payloads and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reuse user-approved table configuration and webhook details for later writes.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
