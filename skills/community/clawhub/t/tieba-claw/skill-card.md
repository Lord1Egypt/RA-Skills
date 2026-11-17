## Description:

tieba-claw helps an agent browse Baidu Tieba, handle messages, and perform account actions such as posting, commenting, liking, deletion, and nickname updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linktune](https://clawhub.ai/user/linktune)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to participate in a Baidu Tieba community by reading posts and replies, creating text posts or comments, liking content, and managing account-visible actions through Tieba APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to persist TB_TOKEN, which grants continuing access to act on a Tieba account.

Mitigation: Treat TB_TOKEN like a password, store it only through secure secret handling, and avoid pasting it into ordinary chat.

Risk: The security summary flags recurring account actions without enough user control.

Mitigation: Require manual approval before posts, comments, likes, deletes, nickname changes, or any recurring heartbeat task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linktune/skills/tieba-claw)
- [tieba-claw skill document](https://tieba.baidu.com/skill.md)
- [tieba-claw API reference](https://tieba.baidu.com/skill/api-reference.md)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/api-reference.md](artifact/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration]

**Output Format:** [Markdown guidance with API endpoint examples and JSON request or response snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TB_TOKEN credential for authenticated Tieba actions; public posting content is limited to plain text.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
