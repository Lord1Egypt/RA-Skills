## Description:

TopYappers is a social media intelligence skill for discovering viral TikTok content, searching creators across TikTok, Instagram, and YouTube, and tracking trending song charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tadasgedgaudas](https://clawhub.ai/user/tadasgedgaudas)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and social media teams use this skill to query TopYappers for creator discovery, viral video analysis, video search, and trending music reports. It helps agents choose the right TopYappers tool, shape filters correctly, and manage credit usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TopYappers uses an external MCP API that requires a bearer token.

Mitigation: Confirm trust in TopYappers before installation and handle the API key as a credential.

Risk: Creator profiles can include emails and demographic fields that may be personal data.

Mitigation: Retrieve only necessary fields, avoid unnecessary storage or redistribution, and follow platform rules and applicable privacy laws.

Risk: Several tools consume credits per result or request.

Mitigation: Use free creator search first, keep exploratory page sizes small, and monitor credit usage.

## Reference(s):

- [TopYappers Platform](https://www.topyappers.com)
- [TopYappers API Documentation](https://docs.topyappers.com)
- [TopYappers MCP Documentation](https://www.topyappers.com/tools/mcp)
- [TopYappers MCP GitHub](https://github.com/topyappers/topyappers-mcp)
- [ClawHub Skill Page](https://clawhub.ai/tadasgedgaudas/skills/topyappers)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and API call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external TopYappers MCP endpoint with bearer-token authentication, rate limits, and credit-based tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
