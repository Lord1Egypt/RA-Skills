## Description: <br>
Helps agents operate 蜀宁 OA timesheet workflows, including login, project lookup, timesheet submission, updates, daily queries, and detail checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ithou](https://clawhub.ai/user/ithou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or their delegated agents use this skill to manage 蜀宁 OA work records after authenticated login. It supports submitting daily timesheets, saving drafts, updating or logically deleting records, checking record status, viewing details, and listing projects. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Stored OA credentials, encryption keys, or printed tokens could expose account access. <br>
Mitigation: Use encrypted credentials, protect OA_ENC_KEY and any local key cache, avoid saving printed tokens, and verify the OA base URL before login. <br>
Risk: Submit, update, batch, or delete actions can change business timesheet records. <br>
Mitigation: Require explicit user confirmation before record-changing actions and review the target date, project, record ID, description, and draft versus submit mode. <br>
Risk: Project IDs, time-entry IDs, and internal configuration values may be sensitive in normal chat responses. <br>
Mitigation: Return business-readable fields by default and reveal internal IDs only when the user explicitly asks or an operation requires them. <br>


## Reference(s): <br>
- [蜀宁 OA 工时系统 API 参考](references/api.md) <br>
- [ClawHub skill page](https://clawhub.ai/ithou/sn-work-record) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run Python scripts that call OA APIs using local credentials; some commands can submit, update, or logically delete timesheet records.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
