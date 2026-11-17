## Description:

A custom tool for web searching using the Brave Search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mryee2023](https://clawhub.ai/user/mryee2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to let an agent retrieve current web search results through the Brave Search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to the Brave Search API and may expose sensitive information if users include secrets, customer data, or confidential internal details.

Mitigation: Avoid submitting secrets, private customer data, or confidential internal details in search queries.

Risk: The skill requires a Brave API key through BRAVE_API_KEY.

Mitigation: Provide the key through the environment and manage it as a secret according to local credential handling practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mryee2023/skills/yee-brave-search)
- [Brave Search API endpoint](https://api.search.brave.com/res/v1/web/search)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON search results or JSON error object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and the BRAVE_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
