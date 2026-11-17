## Description:

Operate on todolist-md Markdown todo files. Read + summarize tasks, propose edits, and write outcomes back into Markdown using only <!-- bot: ... --> markers (line-stable write-back).

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitsujy](https://clawhub.ai/user/nitsujy)

### License/Terms of Use:


## Use Case:

Developers and task-focused users use this skill to review Markdown todo files, summarize open work, prepare concise suggestion requests, and write approved bot suggestions back with stable Markdown markers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Google Drive authority could expose unrelated personal or business files if the skill is connected to a general-purpose account or folder.

Mitigation: Use a dedicated Google account or isolated Drive folder that contains only intended Markdown todo files.

Risk: Stored OAuth refresh tokens can continue granting access after initial setup.

Mitigation: Store tokens with restricted file permissions and revoke or delete them when the skill is no longer in use.

Risk: Untrusted suggestions JSON could write unwanted bot suggestions back into Markdown files.

Mitigation: Keep suggestions JSON trusted, review generated suggestions before apply mode, and run dry-run first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nitsujy/skills/todolist-md-clawdbot)
- [Project homepage](https://github.com/NitsujY/todolist-md)
- [Publisher profile](https://clawhub.ai/user/nitsujy)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request or suggestion files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes only bot-marked Markdown suggestion sections or review markers; prepare mode emits compact JSON for changed files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
