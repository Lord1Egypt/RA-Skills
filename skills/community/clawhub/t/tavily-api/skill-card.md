## Description:

Helps agents search the web, extract page content, map and crawl sites, and conduct research with citations using Tavily through Maton.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can ask an agent to search the web, retrieve and summarize pages, explore site structure, and perform research with citations through their authorized Tavily connection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, URLs, crawl targets, and research prompts are sent to Tavily through Maton.

Mitigation: Avoid private or tokenized URLs unless the user knowingly chooses to send them.

Risk: Authorizing a connection or enabling hosted functions, triggers, and destinations may grant ongoing access or automation.

Mitigation: Authorize only the intended Tavily connection and obtain explicit approval before enabling automation or persistent destinations.

Risk: Raw API-key workflows involve sensitive credentials.

Mitigation: Use the login flow when possible and require explicit approval for raw API-key workflows.

## Reference(s):

- [Tavily skill release](https://clawhub.ai/byungkyu/skills/tavily-api)
- [Tavily API documentation](https://docs.tavily.com)
- [Maton homepage](https://maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with source links and citations; structured results when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the authorized Tavily connection and available web content.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
