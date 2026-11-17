## Description:

Search the public Internet with YouMind Search. Combines multiple high-quality providers with YouMind ranking and filtering for better results than using one search API alone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p697](https://clawhub.ai/user/p697)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search the public web for fresh external information, online research, recent news, source gathering, and domain-filtered lookup. It is intended for YouMind web search, not private YouMind library search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to YouMind along with authentication using the configured API key.

Mitigation: Install only if YouMind is trusted for the searches being run, and keep YOUMIND_API_KEY scoped and stored as an environment variable.

## Reference(s):

- [YouMind](https://youmind.com/)
- [ClawHub Skill Page](https://clawhub.ai/p697/skills/youmind-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouMind account and YOUMIND_API_KEY environment variable.]

## Skill Version(s):

2.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
