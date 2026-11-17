## Description:

Web search via Tavily API for looking up sources, finding links, and retrieving web results when Brave web_search is unavailable or undesired.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jayegt002](https://clawhub.ai/user/jayegt002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tavily web searches, retrieve result links, optionally include images, and filter blocked domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions fetch mutable remote code that may differ from the reviewed artifact.

Mitigation: Verify or pin the downloaded code before running search.sh, and prefer a reviewed release artifact where possible.

Risk: Search queries are sent to Tavily and may expose sensitive user intent or confidential text.

Mitigation: Avoid searching for secrets, credentials, private data, or confidential material.

Risk: The Tavily API key can be stored in a local plaintext apikey file.

Mitigation: Prefer the TAVILY_API_KEY environment variable; if a local file is required, restrict permissions to the current user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jayegt002/skills/tavily-search-skill)
- [Project Homepage](https://github.com/JayeGT002/Tavily-Search-Skill)
- [Tavily API Keys](https://app.tavily.com/api-keys)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON search results with Markdown setup and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include query text, result records, quota information, response time, and filtered domain output.]

## Skill Version(s):

1.0.7 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
