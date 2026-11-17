## Description:

Posts and schedules content on the user's Threads account, checks post and image constraints, and reports delivery status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sultanlive](https://clawhub.ai/user/sultanlive)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to draft, publish, schedule, and manage posts on their connected Threads account through 1Social.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved media uploads become publicly accessible immediately, even if the user later cancels the post.

Mitigation: Show the exact files before upload and wait for the user's approval; upload only media intended to be public.

Risk: A published Threads post cannot be removed through 1Social and may remain live until the user removes it manually.

Mitigation: Preview the post and confirm its text, destination account, media, and timing before publishing.

Risk: Publishing after the free trial requires a paid plan.

Mitigation: Check the connected account's plan and quota before publishing or scheduling, and make the paid-plan requirement clear.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sultanlive/skills/threads)
- [1Social Threads publishing](https://1social.dev/post-to/threads?ref=skill)
- [1Social MCP setup](https://1social.dev/mcp)
- [1Social pricing](https://1social.dev/pricing)

## Skill Output:

**Output Type(s):** [Text, API responses]

**Output Format:** [Threads post text, scheduling details, and delivery receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Posts are checked against Threads character and media constraints; delivery status is reported per selected network.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
