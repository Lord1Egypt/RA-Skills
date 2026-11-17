## Description:

Search the public web through the AISA web search endpoint and return structured titles, links, and snippets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent look up public web information, gather recent sources, and return structured search results. It is suited for general online lookup tasks that can be sent to the AISA API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, requested URLs, and related results are sent to AISA's API using the configured AISA_API_KEY.

Mitigation: Avoid using the skill with secrets, private URLs, regulated data, credentials, or credential-related requests.

Risk: The packaged client includes research and extraction modes beyond simple title, link, and snippet search.

Mitigation: Review enabled modes and restrict automatic invocation to the modes appropriate for the deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisadocs/skills/web-search-aisa)
- [AISA Service](https://aisa.one)
- [AISA API Base](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and terminal text with structured titles, links, snippets, answers, citations, and usage details when returned by the API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends web search, extraction, and research requests to AISA API endpoints.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
