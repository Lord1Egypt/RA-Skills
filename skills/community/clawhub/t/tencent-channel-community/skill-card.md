## Description: <br>
Tencent Channel (QQ Channel) community-management skill that guides agents to use tencent-channel-cli for channel, member, post, notification, direct-message, moderation, and Q&A workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External community managers, operators, and agents use this skill to manage Tencent Channel communities through CLI-backed workflows for publishing, moderation, member operations, notifications, and channel administration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can take account-facing channel actions from recent-notification context. <br>
Mitigation: Require the agent to show the exact notification number and target summary before replies, DMs, approvals, rejections, deletes, mutes, kicks, or other changes. <br>
Risk: The skill may fetch titles for arbitrary user-provided URLs. <br>
Mitigation: Approve untrusted links before title fetching, or require the agent to use the provided URL text without fetching remote content. <br>
Risk: The Tencent Channel CLI workflow can exercise account-level channel authority. <br>
Mitigation: Install and use only when the publisher and CLI workflow are trusted, and require explicit confirmation for documented high-risk operations. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/tencent-adm/tencent-channel-community) <br>
- [Tencent Connect AI homepage](https://connect.qq.com/ai) <br>
- [Channel and guild management reference](references/manage-guild.md) <br>
- [Member management reference](references/manage-member.md) <br>
- [Feed and content management reference](references/feed-reference.md) <br>
- [Notification workflow reference](references/notification-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses tencent-channel-cli command schemas and reference documents to shape executable steps; returns user-facing summaries while minimizing sensitive fields.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
