## Description:

Autonomous social media management for X/Twitter using OpenClaw native tools to draft, post, engage, schedule, and track account activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psmamm](https://clawhub.ai/user/psmamm)

### License/Terms of Use:


## Use Case:

External users use this skill to operate an X/Twitter account through browser-based posting, engagement, content planning, scheduling, and engagement tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish or schedule posts and perform engagement actions on a live X/Twitter account without clear approval gates.

Mitigation: Require draft preview and explicit approval for every post, reply, quote, like, follow, and scheduled job before execution.

Risk: Automated posting can continue after setup and create unwanted account activity.

Mitigation: Use clear posting limits, logs, and a fast stop path before enabling scheduled posting.

## Reference(s):

- [Content Templates](references/content-templates.md)
- [ClawHub Skill Listing](https://clawhub.ai/psmamm/skills/social-media-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce social post drafts, schedules, engagement plans, and tracking logs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
