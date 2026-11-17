## Description:

Send local files to a Telegram chat as documents, photos, video, or audio after resolving paths and checking file size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to send an explicitly selected workspace file to a Telegram chat through the Telegram Bot API. It is intended for file delivery workflows where the environment provides TG_BOT_TOKEN and curl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send local workspace files to Telegram, which may expose private content if the file and destination are not verified.

Mitigation: Use it only for explicit file-send requests and confirm the exact resolved file path and Telegram destination before each send.

Risk: The documented prefix-based workspace path check may not reliably prove path containment in every path layout.

Mitigation: Use a canonical containment check and reject symlinks before uploading any file.

Risk: Cleanup behavior for /tmp files could remove files the skill did not create.

Mitigation: Only delete temporary files created and tracked during the same operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/tg-file-sender)
- [ClawHub metadata homepage](https://clawhub.ai/BusTes01/tg-file-sender)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TG_BOT_TOKEN and curl; sends files up to 50 MB when the file path and Telegram destination are confirmed.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
