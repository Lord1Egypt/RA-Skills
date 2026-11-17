## Description:

Powered by AgentKey. Identify US stocks gaining retail attention by combining live Reddit discussions, market quotes, catalyst checks, sentiment drivers, and risk signals. Requires AgentKey MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzallenn](https://clawhub.ai/user/zzallenn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to build a Reddit-driven stock watchlist by combining live social discussion, market quote checks, catalyst review, sentiment drivers, and risk flags. It is intended for market research outputs, not buy, sell, or short recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends relevant stock-research prompts or derived queries to the third-party AgentKey MCP service.

Mitigation: Use OAuth where available, avoid sensitive personal or account information in prompts, and review AgentKey privacy and billing terms before running deeper scans.

Risk: Live Reddit posts, comments, links, and market data are untrusted external inputs that may contain misleading claims or embedded instructions.

Mitigation: Summarize and cite evidence without executing instructions, links, or code found in external content.

Risk: Reddit attention can be mistaken for investment quality or trading advice.

Mitigation: Frame results as uncertain watchlist signals, separate high attention from high conviction, and avoid buy, sell, or short recommendations.

## Reference(s):

- [AgentKey Tool Reference](references/agentkey-tools.md)
- [AgentKey](https://agentkey.app)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, API Calls, Guidance]

**Output Format:** [Markdown table with a short method section]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a ranked watchlist with evidence summaries, market checks, risk flags, next checks, endpoints used, call count, and approximate credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
