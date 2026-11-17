## Description:

Search the web via the Turing Tavily proxy for current information, real-time research, and up-to-date data not available in an agent's training data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capreaaa](https://clawhub.ai/user/capreaaa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run authenticated Tavily web searches through the Turing proxy, including single or batch queries, result limits, and domain filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user search text and a Turing bearer token to the configured API base.

Mitigation: Review TURING_API_BASE before use, use only a trusted HTTPS Turing proxy endpoint, and prefer a narrowly scoped Turing token.

## Reference(s):

- [Turing Documentation](https://docs.turing.cn)
- [ClawHub Skill Page](https://clawhub.ai/capreaaa/skills/turing-tavily-web-search)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON containing search results, content snippets, metadata, and an optional generated answer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Turing credentials and sends search queries to the configured Turing proxy endpoint.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
