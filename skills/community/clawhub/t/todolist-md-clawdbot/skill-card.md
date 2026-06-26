## Description: <br>
Read, summarize, propose edits, and write back changes for Markdown todo files using line-stable bot markers without altering task identity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NitsujY](https://clawhub.ai/user/NitsujY) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users of todolist-md use this skill to review Markdown todo files, summarize open tasks, propose bot-marked edits, and write accepted outcomes back to the same Markdown files. It is especially focused on Google Drive workflows that preserve file identity and avoid unnecessary LLM calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests durable Google Drive access and can update Drive files. <br>
Mitigation: Install only when persistent Drive access is acceptable, prefer a dedicated Google account or OAuth client, and delete the saved refresh token when the skill is no longer needed. <br>
Risk: Incorrect folder or file identifiers could cause the helper scripts to inspect or update unintended Markdown files. <br>
Mitigation: Verify target folderId and fileIds before running, use dry-run or prepare mode first, and keep Drive revision history or backups available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NitsujY/todolist-md-clawdbot) <br>
- [todolist-md project homepage](https://github.com/NitsujY/todolist-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JavaScript or Python helper behavior, and JSON request or suggestion files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces bot-marked Markdown suggestions and review stamps; the helper scripts can generate compact JSON handoff files and apply accepted suggestions back to Google Drive Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
