## Description:

Tavily Research conducts web-grounded research with explicit citations for comparisons, current events, market analysis, and detailed reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evanydl](https://clawhub.ai/user/evanydl)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-oriented agents use this skill to gather Tavily-backed web evidence and synthesize cited research reports from a topic or question.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read shared local MCP authentication caches when TAVILY_API_KEY is not set.

Mitigation: Prefer a dedicated TAVILY_API_KEY supplied through a scoped secret mechanism and review credential access before deployment.

Risk: The OAuth fallback runs an unpinned npm helper when no credential is available.

Mitigation: Pin and review the OAuth helper dependency, or disable the fallback and require preconfigured credentials in managed environments.

Risk: Research queries are sent to Tavily for processing.

Mitigation: Avoid submitting confidential or regulated data unless the deployment has approved Tavily use and data-handling terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/evanydl/skills/tavily-research)
- [Tavily](https://tavily.com)
- [Tavily MCP Server](https://mcp.tavily.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Text or Markdown-compatible research output, printed to stdout or saved to an optional output file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts JSON input with a required research topic and optional mini, pro, or auto model selection.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
