## Description:

Use the ReelsFarm CLI to make short-form marketing content with AI (TikTok and Instagram slideshows, AI avatar images, product photos, AI videos) and schedule approved posts to your own TikTok, Instagram, YouTube and Facebook accounts. Covers setup, discovery and safe confirmation. Needs a ReelsFarm account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mateohysa](https://clawhub.ai/user/mateohysa)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and marketers use this skill to discover ReelsFarm capabilities, create short-form marketing media, and schedule approved posts to their own social accounts. It guides setup and confirmation of actions that spend credits or publish content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media creation can spend account credits, and approved posts may publish later.

Mitigation: Preview with --dry-run, review the content, cost, destination accounts, and timing, and approve each action before it runs.

Risk: The API key grants access to the user's ReelsFarm account, and content is processed by ReelsFarm.

Mitigation: Protect the API key and review content before sending it to the service.

## Reference(s):

- [ReelsFarm MCP documentation](https://reelsfarm.com/docs/mcp)
- [ReelsFarm](https://reelsfarm.com)
- [ReelsFarm on ClawHub](https://clawhub.ai/mateohysa/skills/reelsfarm)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown guidance with inline shell commands; ReelsFarm returns JSON status and asset links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can create image, video, and slideshow assets or schedule social posts through the user's ReelsFarm account.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
