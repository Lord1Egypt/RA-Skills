## Description:

Search Twitter, Instagram, and Reddit posts in real time. Find social media mentions, track hashtags, discover influencers, and analyze engagement — 1.5B+ posts indexed. Social listening, brand monitoring, and competitor research made easy for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to let agents search social posts, profiles, hashtags, and communities across Twitter, Instagram, and Reddit for social listening, brand monitoring, competitor research, and influencer discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on external setup through xpoz-setup, OAuth authorization, and the Xpoz MCP service.

Mitigation: Confirm the OAuth and MCP configuration point to the expected Xpoz service before granting access.

Risk: The release depends on the mcporter npm package without a pinned version in the evidence.

Mitigation: Install mcporter only after confirming the package source is trusted for the deployment environment.

Risk: Social search results may include personal or sensitive public content from third-party platforms.

Mitigation: Use retrieved data according to applicable platform terms, privacy requirements, and the organization’s review process.

## Reference(s):

- [Xpoz homepage](https://xpoz.ai)
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup)
- [Xpoz Social Search ClawHub page](https://clawhub.ai/atyachin/skills/xpoz-social-search)
- [Publisher profile](https://clawhub.ai/user/atyachin)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search operations return operation IDs that must be polled; CSV export is available for larger result sets.]

## Skill Version(s):

1.5.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
