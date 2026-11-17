## Description:

CLI tool for Telegram via MTProto that helps an agent read and send messages, manage groups and contacts, search conversations, download media, and automate Telegram workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baontq23](https://clawhub.ai/user/baontq23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to operate the node-telegram-cli tool for explicit Telegram account tasks, especially machine-readable inbox review, search, messaging, media handling, and group or contact administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Telegram CLI session can grant broad account access, including private chats, groups, contacts, and downloaded media.

Mitigation: Use the skill only for explicit Telegram tasks, pin and verify the npm package version where possible, limit automation scope, and log out when the retained CLI session is no longer needed.

Risk: Messaging, forwarding, deleting, marking messages read, and managing groups or contacts can create irreversible or visible side effects.

Mitigation: Confirm the target peer and action before sending, deleting, marking read, or changing groups and contacts.

Risk: Interactive commands can block automation and expose the agent to unintended conversation state.

Mitigation: Use machine-readable JSON mode for commands and avoid the documented interactive ntg chat command in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baontq23/skills/telegram-cli)
- [Publisher profile](https://clawhub.ai/user/baontq23)
- [node-telegram-cli repository](https://github.com/baontq23/node-telegram-cli)
- [node-telegram-cli npm package](https://www.npmjs.com/package/node-telegram-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should use the ntg --json flag for automation and avoid interactive chat mode.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
