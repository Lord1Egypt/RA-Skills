## Description:

Create, adapt, schedule, publish, and analyze AI-generated social media content across 10 platforms in 13 languages using Twinfold's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lpbaril](https://clawhub.ai/user/lpbaril)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate a Twinfold account from an agent, including creating social posts, adapting content by platform and language, managing drafts and schedules, publishing approved content, checking analytics, and reviewing account notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish social media content to live connected accounts, including immediate publish, scheduled publish, approve, runAutopilot, and autoPublish:true flows.

Mitigation: Require draft-first operation and explicit user confirmation before publishing, scheduling, approving, deleting, running autopilot, or using autoPublish:true.

Risk: Autopilot and multi-platform workflows can affect several accounts, platforms, or languages in one action.

Mitigation: Preview target accounts, languages, platforms, generated content, media, first comments, and scheduled times before allowing the action to proceed.

Risk: Content generation, image generation, Twin queries, brand guide generation, and brand voice generation can consume Twinfold credits.

Mitigation: Check twinfold.getCredits before credit-consuming or multi-post operations and present estimated credit use when available.

## Reference(s):

- [Twinfold](https://twinfold.app)
- [Twinfold MCP tools endpoint](https://twinfold.app/api/mcp/tools)
- [Tool schemas and workflows](references/workflows.md)
- [ClawHub skill page](https://clawhub.ai/lpbaril/skills/twinfold)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON request bodies, shell command examples, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TWINFOLD_API_KEY for authenticated API actions; some operations consume Twinfold credits and may publish or schedule content to connected accounts.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
