## Description:

Uses the Tavily API to provide real-time web search and content extraction for current-information requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangkelvin](https://clawhub.ai/user/fangkelvin)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route web research, recent-information, and news-search requests to Tavily. It is intended for workflows where an agent needs search results or extracted web content through a Tavily API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries may disclose sensitive information to Tavily.

Mitigation: Do not search for secrets, credentials, private customer data, or internal project details unless policy allows sharing them with Tavily.

Risk: Troubleshooting may accidentally expose the Tavily API key.

Mitigation: Use a presence check instead of printing the API key when diagnosing configuration issues.

## Reference(s):

- [Tavily](https://tavily.com)
- [Tavily Search API endpoint](https://api.tavily.com/search)
- [ClawHub skill page](https://clawhub.ai/fangkelvin/skills/tavily-skill)
- [Publisher profile](https://clawhub.ai/user/fangkelvin)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search requests require curl, jq, and a TAVILY_API_KEY; responses are returned from Tavily as JSON.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
