## Description:

Manage your LinkedIn presence with Reepl -- create drafts, publish and schedule posts, manage contacts and collections, generate AI images, create carousels, post to Twitter/X, and maintain your voice profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhibavishi](https://clawhub.ai/user/abhibavishi)

### License/Terms of Use:


## Use Case:

External users and social content teams use this skill to draft, publish, schedule, and repurpose LinkedIn and Twitter/X content through Reepl while preserving the user's voice profile and saved content library.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Reepl MCP key can grant broad access to read and manage LinkedIn and connected Twitter/X content.

Mitigation: Use secret or environment-based credential handling when supported, and avoid sharing logs or screenshots that contain the configured MCP URL.

Risk: Publish, comment, schedule, delete, and profile-update actions can affect real social accounts.

Mitigation: Require explicit user approval before invoking any action that publishes, comments, schedules, deletes, or updates a profile.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/abhibavishi/skills/reepl)
- [Reepl](https://reepl.io)
- [Reepl Help Center](https://help.reepl.io)
- [MCP Setup Guide](https://mcp.reepl.io)
- [Reepl AI model settings](https://app.reepl.io/settings/ai-models-api)
- [Reepl Chrome Extension](https://chromewebstore.google.com/detail/reepl/geomampobbapgnflneaofdplfomdkejn)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and plain-text social content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Reepl MCP connection using REEPL_MCP_KEY; LinkedIn content is plain text and Twitter/X tweets are limited to 280 characters each.]

## Skill Version(s):

1.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
