## Description:

SocialFaktory helps agents draft, generate short video for, schedule, publish, and review metrics for a brand's social posts across TikTok, Instagram, YouTube, X, LinkedIn, Facebook, and Pinterest.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adifsgaid](https://clawhub.ai/user/adifsgaid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and brand operators use this skill to connect an agent to SocialFaktory, draft social content in a brand voice, quote and generate short videos, create channel-specific posts, schedule or publish approved drafts, and read metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth permissions can grant access to selected brands and social channels.

Mitigation: Confirm the user trusts SocialFaktory for the selected brand and choose the narrowest OAuth permissions needed.

Risk: Generation calls may spend the user's SocialFaktory credits.

Mitigation: Quote generation first, show the price, set a monthly credit cap and expiry, and run spending calls only after user approval.

Risk: Publishing actions can queue or send posts to connected social channels.

Mitigation: Review drafts with the user before allowing posts to be queued or published.

## Reference(s):

- [SocialFaktory MCP documentation](https://www.socialfaktory.com/docs/mcp)
- [SocialFaktory website](https://www.socialfaktory.com)
- [ClawHub skill listing](https://clawhub.ai/adifsgaid/skills/socialfaktory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown]

**Output Format:** [Markdown with inline shell commands and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes user approval before OAuth consent, credit-spending generation calls, and publishing actions.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
