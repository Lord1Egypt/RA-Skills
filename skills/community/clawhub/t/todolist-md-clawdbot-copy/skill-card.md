## Description: <br>
Read, summarize, propose edits, and write back changes to Markdown todo files using line-stable bot markers without altering task identity or completing tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NitsujY](https://clawhub.ai/user/NitsujY) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users of Markdown-first todo workflows use this skill to review changed todo files, prepare compact task summaries or suggestions, and write approved bot-marked outcomes back to Markdown while preserving file and task identity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses persistent Google Drive credentials and broad Drive access to read and update Markdown files. <br>
Mitigation: Use a dedicated Drive folder or account, verify the OAuth client and gog binary, keep Drive revision history or backups, and revoke or delete stored tokens when access is no longer needed. <br>
Risk: Automated write-back could overwrite recent human edits or introduce unwanted task suggestions. <br>
Mitigation: Start with dry runs or a small folder, review suggestions before apply mode, rely on the revision gate, and keep bot output confined to the dedicated bot-marked section. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/NitsujY/todolist-md-clawdbot-copy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON request and suggestion files, shell command examples, and bot-marked Markdown write-back patterns.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses stable HTML comment markers and line-stable edits; helper scripts can prepare LLM request JSON and apply suggestion JSON to Google Drive Markdown files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
