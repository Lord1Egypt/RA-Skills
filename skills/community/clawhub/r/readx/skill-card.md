## Description:

Twitter/X intelligence toolkit: analyze users, tweets, trends, communities, and networks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxtsky](https://clawhub.ai/user/wxtsky)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and analysts use this skill to analyze public Twitter/X users, tweets, trends, communities, and networks through readx MCP tools or direct readx API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a readx API key and may ask agents to store it in local or editor configuration.

Mitigation: Use a platform secret store or environment variable where possible, avoid placing long-lived keys in URLs or shared configuration, and rotate keys that may have been exposed in shell history or shared files.

Risk: The security evidence marks the release as suspicious because credential handling and persistence require user review before installation.

Mitigation: Install only after reviewing the credential flow, confirm the key is sent only to readx.cc, and keep user consent explicit before persisting credentials.

## Reference(s):

- [readx ClawHub Skill Page](https://clawhub.ai/wxtsky/skills/readx)
- [wxtsky ClawHub Publisher Profile](https://clawhub.ai/user/wxtsky)
- [readx Service](https://readx.cc)
- [readx API Documentation](https://readx.cc/api-docs.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, bullet lists, inline metrics, and optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include derived engagement metrics, ranked comparisons, key takeaways, and setup guidance for readx MCP or API access.]

## Skill Version(s):

1.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
