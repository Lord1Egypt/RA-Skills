## Description:

Wechat Control provides Python commands for a local Windows WeChat client to log in, send text messages, list recent chats, and report total unread messages through itchat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltf13133-wq](https://clawhub.ai/user/ltf13133-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and local automation users use this skill to operate a single logged-in Windows WeChat desktop account from Python or command-line workflows. It is suited to private local use where recipients and message text can be reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send messages through the user's logged-in WeChat account.

Mitigation: Use it only in a private local environment and review the recipient and message text before running send commands.

Risk: The skill can reuse a cached WeChat login session through loginInfo.pkl.

Mitigation: Do not share or sync loginInfo.pkl, and delete the cache when the session should no longer be reused.

Risk: The skill has limited safeguards around account actions.

Mitigation: Install only when account-level automation is acceptable and run commands interactively for sensitive conversations.

## Reference(s):

- [Wechat Control on ClawHub](https://clawhub.ai/ltf13133-wq/skills/wechat-control)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with inline Python and shell command examples; runtime commands print text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local Windows WeChat desktop session and Python dependencies listed in requirements.txt.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
