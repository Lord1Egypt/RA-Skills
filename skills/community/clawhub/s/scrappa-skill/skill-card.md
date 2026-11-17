## Description:

Access Scrappa's MCP server for Google, YouTube, Amazon, LinkedIn, Trustpilot, flights, hotels, and more via Model Context Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[userlip](https://clawhub.ai/user/userlip)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to configure agent access to Scrappa's MCP server and request search, scraping, translation, review, travel, real estate, marketplace, and job data through its listed tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests sent through the skill are processed by Scrappa and relevant downstream services.

Mitigation: Avoid submitting confidential business data, private URLs, sensitive personal information, or third-party profile lookups unless that processing is acceptable.

Risk: The external Scrappa service requires an API key and may enforce account-specific rate limits.

Mitigation: Configure credentials securely and review Scrappa plan limits before production use.

## Reference(s):

- [Scrappa Documentation](https://scrappa.co/docs)
- [Scrappa MCP Integration Guide](https://scrappa.co/docs/mcp-integration)
- [Scrappa Dashboard](https://scrappa.co/dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Scrappa API key; requests are sent to Scrappa's external MCP service and may be subject to plan rate limits.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
