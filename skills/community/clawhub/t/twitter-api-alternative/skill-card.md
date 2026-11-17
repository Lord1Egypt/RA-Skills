## Description:

Twitter API Alternative helps agents search large Twitter datasets with natural language queries, Boolean filters, profile lookup, conversation tracking, and CSV exports through Xpoz MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External users, researchers, and developers use this skill to search Twitter social data, inspect profiles and interactions, and export CSV datasets without managing a Twitter developer account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the mcporter npm package, the Xpoz service, and the xpoz-setup authentication skill.

Mitigation: Verify trust in those dependencies before installation and use approved environments for authenticated Xpoz access.

Risk: Generated CSV download links can expose large social-media datasets that may be sensitive in lead generation or regulated research workflows.

Mitigation: Limit sharing and retention of exported datasets, and handle download links as sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atyachin/skills/twitter-api-alternative)
- [Publisher profile](https://clawhub.ai/user/atyachin)
- [Xpoz](https://xpoz.ai)
- [xpoz-setup skill](https://clawhub.ai/skills/xpoz-setup)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to initiate Xpoz MCP searches and retrieve CSV export download links.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
