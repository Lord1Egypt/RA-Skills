## Description:

Publish, schedule, and manage social media posts across Twitter/X, Facebook, Instagram, LinkedIn, TikTok, and YouTube, with content planning, engagement, repurposing, and analytics features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[miprinia](https://clawhub.ai/user/miprinia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect social accounts, prepare and publish posts, schedule campaigns, review engagement, and manage related feeds and links across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a saved access token for account and feed management, including actions that can publish publicly or delete content.

Mitigation: Grant only the API scopes needed and require human approval for publishing, public replies, deletions, account disconnections, and changes that can trigger recurring or feed-based posts. Prefer read-only, draft, scheduled, or preview actions when possible.

Risk: The security scan was partial because multiple local references could not be resolved.

Mitigation: Review the complete skill and resolve its referenced materials before installing or granting credentials.

## Reference(s):

- [SocialCannon](https://socialcannon.app)
- [SocialCannon MCP package](https://www.npmjs.com/package/@socialcannon/mcp)
- [ClawHub release page](https://clawhub.ai/miprinia/skills/socialcannon)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown instructions with shell commands, JSON request bodies, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific publishing constraints and requires SocialCannon client credentials for authenticated operations.]

## Skill Version(s):

1.16.0 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
