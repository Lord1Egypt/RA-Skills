## Description:

Yunjia File Transfer helps an agent send local files to the current chat by packaging absolute file paths and a user-facing message into transfer JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billyang1222](https://clawhub.ai/user/billyang1222)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace agents use this skill when a user asks for a file to be found and sent into the current chat. It is intended for file-transfer workflows where the agent can identify exact local file paths and return plugin-readable JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage broad local folder searches and immediate transfer of matched files into chat.

Mitigation: Ask the user to confirm the exact file before sending, limit searches to user-approved directories, and avoid transferring ambiguous matches.

Risk: Requested text and local file paths may be written to a persistent log file.

Mitigation: Avoid sensitive content in transfer messages and prefer an updated version that redacts, disables, or rotates persistent logging.

Risk: Incorrect or relative paths can fail validation or identify the wrong file.

Mitigation: Use absolute platform-specific paths and verify the selected file exists before producing the transfer JSON.

## Reference(s):

- [Windows Guide](references/WINDOWS_GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/billyang1222/skills/yunjia-file-transfer)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON transfer instruction with filePaths, text, and mode fields, with supporting guidance and shell commands in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires absolute local file paths; the script writes transfer JSON to stdout for chat-file delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
