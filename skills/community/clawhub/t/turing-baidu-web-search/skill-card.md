## Description:

Search the web via the Turing Baidu proxy for Chinese-language, China-focused, or current Baidu Search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capreaaa](https://clawhub.ai/user/capreaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Baidu-backed web searches for Chinese-language and China-focused current information, returning structured search results for follow-up research.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and bearer credentials may be sent to any configured Turing API base URL.

Mitigation: Use only a trusted HTTPS Turing API base and consider allowlisting the proxy host before forwarding credentials.

Risk: Sensitive or personal data in search terms may be transmitted to the configured search proxy.

Mitigation: Avoid placing secrets, personal data, or confidential business information in search queries.

## Reference(s):

- [Turing documentation](https://docs.turing.cn)
- [ClawHub skill page](https://clawhub.ai/capreaaa/skills/turing-baidu-web-search)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration]

**Output Format:** [JSON search results printed by a Python command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TURING_API_KEY, TURING_CLIENT, and TURING_ENVIRONMENT; supports result count and recency filters.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
