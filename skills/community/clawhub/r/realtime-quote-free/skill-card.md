## Description:

实时行情跟踪 helps an agent retrieve and summarize A-share quote data with multi-provider fallback, latency handling, and structured market-analysis outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and developers use this skill to request A-share stock quotes, compare market-data sources, and produce structured JSON or Markdown summaries for monitoring and decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests shell command authority without a narrow explanation or safeguards.

Mitigation: Review the skill before installing, use it only with trusted publishers, and restrict or disable command execution when the market-data workflow does not require it.

Risk: Market data can be delayed, unavailable, or inconsistent across providers.

Mitigation: Treat outputs as informational support and verify important financial decisions against authoritative, licensed market-data sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/realtime-quote-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON or Markdown text, with configuration guidance and command snippets when setup is required]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference market-data API credentials such as STOCK_API_KEY and may include risk-oriented analysis fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
