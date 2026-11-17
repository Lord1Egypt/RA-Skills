## Description:

Xiaohongshu Auto Publisher Pro helps creators and marketing teams plan, draft, schedule, publish, and analyze Xiaohongshu image-text posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, MCNs, and brand marketing teams use this skill to track topical trends, draft Xiaohongshu posts, maintain a publishing schedule, and review post-performance signals. Human approval should be required before scheduled tasks are created or account actions are taken.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent publishing schedules or cron jobs.

Mitigation: Require explicit approval before creating schedules, and confirm how to list, pause, and delete scheduled tasks and saved content plans.

Risk: The skill can operate a logged-in Xiaohongshu account and submit posts.

Mitigation: Require manual review and approval before opening a logged-in account, filling post fields, submitting content, or collecting analytics.

Risk: Broad social-media automation triggers could initiate account actions in an unintended context.

Mitigation: Confirm the target account, content domain, schedule, and permitted actions before any write, browser, or publishing step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/skills/xiaohongshu-auto-publisher-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/lijinhao123-dot)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with generated post copy, JSON scheduling entries, and account-operation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent schedules, account automation steps, and analytics review actions that require explicit user approval.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
