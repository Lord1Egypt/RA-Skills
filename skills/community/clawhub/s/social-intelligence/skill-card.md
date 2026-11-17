## Description:

Social Intelligence provides AI-powered social media research across Twitter, Instagram, Reddit, and TikTok for search, lead generation, brand monitoring, sentiment analysis, influencer discovery, and CSV export through Xpoz MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide AI agents through social media research workflows, including post search, expert and lead discovery, sentiment analysis, brand monitoring, influencer research, and CSV export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and CSV exports may contain sensitive social-media data or unnecessary personal data.

Mitigation: Avoid sending confidential, regulated, or unnecessary personal data in searches, and treat large social-media exports as sensitive datasets.

Risk: The skill depends on the Xpoz service and xpoz-setup authentication flow.

Mitigation: Review the Xpoz service and xpoz-setup skill before installing, especially how OAuth tokens, search queries, and CSV exports are handled.

## Reference(s):

- [Xpoz](https://xpoz.ai)
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup)
- [Social Intelligence on ClawHub](https://clawhub.ai/atyachin/skills/social-intelligence)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and service/tool references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to request CSV exports from Xpoz MCP tools, with exports described by the artifact as up to 64K rows per query.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
