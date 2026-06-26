## Description: <br>
Provides local SiYuan Note API guidance and helper commands for reading, writing, searching, templating, SQL-querying, and managing notebooks, documents, and blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moxunjinmu](https://clawhub.ai/user/moxunjinmu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and SiYuan Note users use this skill to let an agent operate on a local SiYuan workspace for notebook, document, block, search, template, and SQL workflows. It is intended for deliberate local note-management tasks where the user can provide a SiYuan API token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to private local notes, including search, export, modification, deletion, and SQL queries. <br>
Mitigation: Install only when agent access to the local SiYuan workspace is intended, provide the token only for deliberate SiYuan tasks, and require explicit approval before creating, updating, deleting, exporting, or sending note data. <br>
Risk: SQL statements may expose sensitive note content or run queries the user did not intend. <br>
Mitigation: Review SQL statements before execution and limit queries to the minimum notebook, document, fields, and row counts needed for the task. <br>
Risk: The helper script sends authenticated requests to the local SiYuan API and has no built-in policy guardrails. <br>
Mitigation: Run it only against the local SiYuan service, keep the API token in a scoped environment variable, and remove the token when the task is complete. <br>


## Reference(s): <br>
- [SiYuan Note API reference](references/api.md) <br>
- [Official SiYuan API documentation](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md) <br>
- [ClawHub release page](https://clawhub.ai/moxunjinmu/siyuan-note) <br>
- [Publisher profile](https://clawhub.ai/user/moxunjinmu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python helper usage, and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a locally running SiYuan instance and a user-provided SiYuan API token for protected endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
