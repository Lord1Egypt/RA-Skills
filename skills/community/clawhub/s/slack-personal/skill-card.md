## Description:

Slk lets an agent read, send, search, and manage Slack channels, DMs, threads, drafts, saved items, pins, reactions, and unread activity through the macOS-only slk CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[therohitdas](https://clawhub.ai/user/therohitdas)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users can use this skill to let an agent check Slack context, summarize relevant workspace activity, draft messages for review, or send messages when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill extracts and caches desktop Slack session credentials, allowing an agent to read Slack data and act as the user.

Mitigation: Install only on a personal macOS machine, prefer one-time Keychain Allow over Always Allow, and remove the token cache when not needed.

Risk: The skill can send Slack messages and react to messages as the user.

Mitigation: Use drafts for messages that need human review and approve send actions separately before execution.

Risk: Development guidance in the artifact includes publishing and token-handling steps.

Mitigation: Do not allow agents to follow publish, push, or npm-token steps without separate explicit approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/therohitdas/skills/slack-personal)
- [slkcli npm package](https://www.npmjs.com/package/slkcli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and Slack message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Slack channel, DM, thread, search, unread, saved-item, draft, reaction, and send-command outputs.]

## Skill Version(s):

0.1.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
