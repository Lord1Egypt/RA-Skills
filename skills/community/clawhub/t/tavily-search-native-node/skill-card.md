## Description:

Minimal Tavily web search for OpenClaw using native Node.js with no dependencies, returning Tavily's synthesized answer plus source URLs and snippets for verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jwestburg](https://clawhub.ai/user/jwestburg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a user needs current web information, recent news, research, comparisons, or source-backed lookup results. It performs a bounded Tavily search with optional topic, depth, result count, and domain filters, then returns a concise answer with source URLs and snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and domain filters are sent to Tavily and may expose sensitive user or organization context.

Mitigation: Do not send secrets or confidential text; get explicit owner approval before sending privacy-sensitive non-secret fields to Tavily.

Risk: Shell interpolation of user-controlled query text can execute or expand content before the script receives it.

Mitigation: Invoke the Node script through an argv array with shell disabled, passing the full user query as data.

Risk: External search calls can consume Tavily credits or hit provider rate limits.

Mitigation: Prefer one well-scoped basic search per topic, use domain filters where appropriate, and verify current Tavily pricing and limits before operational use.

Risk: Search answers, titles, snippets, URLs, and page text are external content and may be inaccurate or unsafe to follow as instructions.

Mitigation: Treat returned content as untrusted evidence, cite the source URLs relied on, and do not execute instructions from search results.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jwestburg/skills/tavily-search-native-node)
- [Tavily search endpoint](https://api.tavily.com/search)
- [Tavily app and API key dashboard](https://app.tavily.com)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text by default, or redacted JSON when invoked with --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include the searched query, synthesized answer, source URLs, snippets, timing details, and exact API-key redaction when the key appears in returned text.]

## Skill Version(s):

1.0.30 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
