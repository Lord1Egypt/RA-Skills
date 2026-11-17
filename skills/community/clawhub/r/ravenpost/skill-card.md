## Description:

Schedule and publish social media posts to Instagram, TikTok, X, LinkedIn, Threads, Bluesky, YouTube, Pinterest and Telegram through Ravenpost's hosted MCP server — preview every destination before anything goes out, schedule it or drop it into a weekly queue, and read follower counts and engagement back. Use when the user wants to post, cross-post, schedule, queue or draft social content to their connected accounts, asks what is scheduled, or asks how their posts did.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muratkaragozgil](https://clawhub.ai/user/muratkaragozgil)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to draft, preview, schedule, queue, and publish social posts to their connected accounts, and to check schedules and engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved schedules can publish while the user is away.

Mitigation: Review destinations, content, media, and timing before approving; use drafts for unattended jobs unless the user has approved the schedule.

Risk: Submitted post content is received by Ravenpost, whose hosted implementation was not inspected.

Mitigation: Submit only content appropriate for the connected service.

Risk: Revoking app access may not cancel schedules that already exist.

Mitigation: Check and cancel existing scheduled posts separately when access is revoked.

## Reference(s):

- [Ravenpost MCP overview](https://ravenpo.st/mcp/)
- [Ravenpost MCP tool documentation](https://ravenpo.st/docs/mcp/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Text]

**Output Format:** [Markdown guidance with shell commands and structured MCP requests and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Social account and workspace specific; publication timing and destinations depend on user approval and configured accounts.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
