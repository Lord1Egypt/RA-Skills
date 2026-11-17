## Description:

Send WhatsApp messages or files from the command line using wacli, including text, replies, reactions, media with captions, authentication, synchronization, and message search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prantikmedhi](https://clawhub.ai/user/prantikmedhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to operate the wacli command-line tool for WhatsApp messaging workflows, including sending messages or files, replying to messages, reacting to messages, and searching chats or message history. It is intended for explicit user-directed WhatsApp actions where recipient, content, and attachments are confirmed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger external WhatsApp messaging actions that expose private content or contact the wrong recipient.

Mitigation: Require explicit user confirmation of recipient, message or file content, and attachment paths before running any send or reaction command.

Risk: Dynamic command templates may be unsafe if recipient, message, or file values are interpolated into shell strings.

Mitigation: Use argument-array execution or robust escaping for all command arguments, especially message text, paths, captions, and recipient identifiers.

Risk: The suggested Homebrew tap and local wacli dependency are unpinned third-party software.

Mitigation: Install only after reviewing and trusting the wacli package source, version, and tap, and prefer pinned or audited releases where available.

Risk: The local wacli store may contain sensitive WhatsApp account state and message history.

Mitigation: Protect the store directory, limit access permissions, and treat ~/.wacli or any custom WACLI_STORE_DIR as sensitive account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prantikmedhi/skills/wacli-whatsapp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privacy-sensitive external messaging guidance and command examples for local wacli execution.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
