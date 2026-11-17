## Description:

Safely operates a user's Youdao Note Web account through cookie-authenticated commands to list directories, search notes, read note contents, bulk-read folders, and create notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wendy199804](https://clawhub.ai/user/wendy199804)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate Youdao Note Web: locate folders or notes, read and summarize note contents, and create notes after the user has selected the target account area.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a full browser login cookie for Youdao Note account access.

Mitigation: Treat YOUDAO_COOKIE like a password, inject it only through the environment, avoid storing it longer than needed, and rotate it after use.

Risk: The skill can bulk-read folders or create notes without built-in confirmation controls.

Mitigation: Run bulk reads or note creation only after clearly choosing the target folder or note and reviewing the command before execution.

Risk: Runtime dependencies are listed without pinned versions.

Mitigation: Use an isolated environment and consider pinning dependencies before installation.

## Reference(s):

- [ClawHub Youdao Note Web skill page](https://clawhub.ai/wendy199804/skills/youdaonote-web)
- [Youdao Note Web](https://note.youdao.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output from the bundled CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include note text, directory or search result JSON, created-note metadata, and structured Markdown analysis reports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
