## Description:

A Git repository monitoring skill that tracks repositories across GitHub, GitLab, Gitee, and other Git platforms, pulls updates, and summarizes changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1yihui](https://clawhub.ai/user/1yihui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to monitor Git repositories, check for updates, pull changed code, and receive concise change summaries and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic repository syncing and scheduled checks could affect repositories beyond the user's intended scope.

Mitigation: Enable monitoring only for explicitly approved repositories and review each repository entry before scheduled checks run.

Risk: Feishu notification setup requires credentials and chat identifiers.

Mitigation: Use narrowly scoped Feishu credentials, rotate them as needed, and send notifications only to approved chats.

Risk: The reviewed artifact references helper.js, but that implementation file is not present in the evidence.

Mitigation: Do not assume secret handling, logging, network destinations, or local repository changes are constrained until the implementation is reviewed.

## Reference(s):

- [YiHui GIT MONITOR ClawHub release page](https://clawhub.ai/1yihui/skills/yihui-git-monitor)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown and plain text with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository status, change summaries, scheduled-check guidance, and notification setup details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
