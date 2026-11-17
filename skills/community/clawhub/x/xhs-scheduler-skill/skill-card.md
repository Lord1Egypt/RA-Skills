## Description:

小红书智能排期发布器 helps content creators manage Xiaohongshu post queues, schedule publishing, recommend posting times, and track publishing status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxzxlj](https://clawhub.ai/user/sxzxlj)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, MCN operators, and brand content teams use this skill to plan Xiaohongshu posts, maintain a local publishing queue, trigger scheduled publishing through a Xiaohongshu MCP service, and receive optional success or failure notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated publishing can post incorrect, sensitive, or non-compliant content publicly.

Mitigation: Review queued posts before publishing and use confirmation or dry-run steps before unattended operation.

Risk: Webhook URLs, bot tokens, DingTalk secrets, and Xiaohongshu session data may expose account or notification access if shared.

Mitigation: Keep credentials private, restrict notification channels, and avoid including sensitive titles, links, or error details in shared channels.

Risk: Dependency or platform changes may affect scheduling and publishing behavior.

Mitigation: Pin dependencies where possible and verify publishing behavior on accounts you control before regular use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxzxlj/skills/xhs-scheduler-skill)
- [xiaohongshu-mcp dependency](https://github.com/xpzouying/xiaohongshu-mcp.git)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate on local queue data and optional notification webhook configuration.]

## Skill Version(s):

1.0.0 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
