## Description:

AI+Crypto Twitter automation agent. Post tweets, reply to KOLs, and quote tweet trending content. Integrates with opentwitter/opennews (6551) for hot topic fetching and Claude for content generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearl799](https://clawhub.ai/user/pearl799)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to have an agent draft and publish AI and crypto Twitter/X posts, replies, and quote tweets from their configured account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately publish live public Twitter/X posts, replies, or quote tweets from the configured account without a built-in confirmation or dry-run step.

Mitigation: Review generated content before execution and add an explicit approval or dry-run step before allowing the agent to publish.

Risk: The skill requires Twitter/X write credentials and a 6551 API token.

Mitigation: Use an account appropriate for delegated posting, protect the tokens locally, and rotate credentials if exposure is suspected.

Risk: The release depends on the unpinned tweepy package.

Mitigation: Pin and review the dependency before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/pearl799/skills/twitter-agent)
- [Publisher Profile](https://clawhub.ai/user/pearl799)
- [X Developer Platform](https://developer.x.com)
- [6551 MCP](https://6551.io/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script results include success status, tweet or reply identifiers, post URLs, and published text.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
