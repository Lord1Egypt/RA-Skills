## Description: <br>
Helps an agent operate a user's Youdao Cloud Notes by listing directories, searching notes, reading note content, bulk-reading folders, and creating notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wendy199804](https://clawhub.ai/user/wendy199804) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find, read, summarize, and create Youdao Cloud Notes through a local command-line helper. It is suited for note retrieval, folder-level analysis, and structured reporting over a user's own Youdao notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a full browser session cookie for Youdao account access. <br>
Mitigation: Store YOUDAO_COOKIE only in a trusted local environment, treat it like a password, and remove or rotate it after use. <br>
Risk: Bulk folder reads can expose many private notes to the agent context. <br>
Mitigation: Use narrow folder IDs, confirm the folder scope before read_all operations, and avoid broad folders unless all notes are intended for analysis. <br>
Risk: The skill can create notes in the user's Youdao account. <br>
Mitigation: Preview note titles, content, destination folders, and create commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wendy199804/youdaonote-web) <br>
- [Youdao Note web app](https://note.youdao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON/text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses YOUDAO_COOKIE from the local environment and may return private note content for agent analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
