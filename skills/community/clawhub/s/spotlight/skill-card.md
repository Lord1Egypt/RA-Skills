## Description:

Searches local files and indexed content on macOS using Spotlight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[li-hongmin](https://clawhub.ai/user/li-hongmin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to locate files and indexed document content in user-specified macOS directories before asking which results should be read or acted on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local searches can expose sensitive file paths or lead an agent toward files the user did not intend to inspect.

Mitigation: Use narrow, user-specified directories, present returned paths first, and read files only after explicit user approval.

Risk: Privileged Spotlight indexing commands can change system indexing behavior.

Mitigation: Do not approve or run sudo indexing commands through the agent; run administrative commands directly in Terminal only when intentionally requested by the user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/li-hongmin/skills/spotlight)
- [Publisher Profile](https://clawhub.ai/user/li-hongmin)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns matching paths with file type and size when available; requires macOS Spotlight and a user-specified directory.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
