## Description:

Connect to Windsor.ai MCP for natural language access to 325+ data sources including Facebook Ads, GA4, HubSpot, Shopify, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carlosarturoleon](https://clawhub.ai/user/carlosarturoleon)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to query connected Windsor.ai marketing, analytics, CRM, and e-commerce data in natural language and produce performance analysis or reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned package execution path.

Mitigation: Use a pinned or locally reviewed mcporter binary before connecting the Windsor.ai MCP service.

Risk: A troubleshooting command can expose more local secrets than necessary.

Mitigation: Prefer a keychain or secrets manager and avoid bulk exporting values from environment files.

Risk: The skill connects Windsor.ai business data to an external MCP service.

Mitigation: Install only after confirming that this data connection is acceptable for the user's business data and access policies.

## Reference(s):

- [Windsor.ai](https://windsor.ai)
- [ClawHub Skill Page](https://clawhub.ai/carlosarturoleon/skills/windsor-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include analytics summaries, report outlines, query guidance, setup commands, and mcporter configuration snippets.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
