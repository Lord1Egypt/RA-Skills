## Description:

Guides an agent through publishing and managing Xiaohongshu notes through the web interface, including text, image-text, and video posts, scheduled publishing, draft handling, comment replies, and performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuritu](https://clawhub.ai/user/wuritu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to prepare, publish, schedule, and manage Xiaohongshu posts, replies, drafts, and content performance workflows through browser-based steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent Xiaohongshu login and browser-profile reuse can give the skill continuing account access.

Mitigation: Use a dedicated Xiaohongshu account or browser profile and review login state before enabling publishing, comment, or notification workflows.

Risk: The scheduled Cron auto-reply workflow can publish unattended public replies.

Mitigation: Disable or remove the Cron auto-reply workflow unless unattended replies are explicitly intended and reviewed.

Risk: Drafts, publishing queues, and replied-comment records are directed to hard-coded local memory paths.

Mitigation: Move these records into a user-approved skill-specific storage location with documented retention and deletion rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuritu/skills/temp-xhs-skill)
- [Xiaohongshu creator platform](https://creator.xiaohongshu.com/)
- [Xiaohongshu publishing page](https://creator.xiaohongshu.com/publish/publish?source=official)
- [Xiaohongshu notifications](https://www.xiaohongshu.com/notification)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, configuration]

**Output Format:** [Markdown guidance with procedural steps, checklists, and reply templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser navigation steps, suggested post settings, local record locations, and user confirmation checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
