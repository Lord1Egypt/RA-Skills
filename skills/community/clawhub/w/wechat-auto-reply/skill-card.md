## Description:

Automates semi-automatic WeChat replies by reading chat text, selecting a reply with a confidence threshold, and either sending it or asking for confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjdzliu](https://clawhub.ai/user/bjdzliu)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to install and run a WeChat auto-reply workflow for a named contact, with optional direct message sending and confirmation for lower-confidence replies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install external Homebrew tap code that can change after review.

Mitigation: Install only from trusted sources and review the Homebrew formula and installed script before use.

Risk: The automation can inspect WeChat conversations and send messages automatically.

Mitigation: Prefer confirmation mode, avoid sensitive chats, and confirm the data-processing path before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bjdzliu/skills/wechat-auto-reply)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash and AppleScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces WeChat reply guidance and command-oriented setup instructions; execution can inspect chats and send messages through local automation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
