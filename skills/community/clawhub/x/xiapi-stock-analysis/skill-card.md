## Description:

Helps agents produce structured A-share stock analysis and comparison reports covering fundamentals, technical indicators, financials, valuation, capital flows, risks, and disclaimers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill when they need a structured report for one named A-share stock or a comparison across multiple A-share stocks. It guides an agent to gather DAXIAPI data, align reporting periods and time windows, and present conclusions with concrete field citations rather than unsupported investment claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run an unpinned third-party CLI with access to a DAXIAPI token.

Mitigation: Install only after reviewing the daxiapi-cli supply chain, prefer a pinned reviewed CLI version, and run it with minimal filesystem and environment access.

Risk: API tokens may be exposed in logs, command transcripts, or chat output during configuration and troubleshooting.

Mitigation: Use environment variables or secret handling where available, avoid printing tokens, and redact tokens from any shared output.

Risk: Unsanitized stock identifiers could lead to incorrect command execution or invalid data retrieval.

Mitigation: Validate stock codes or company names with the search and stock-info commands before running further data collection.

Risk: Financial conclusions can become misleading when data is missing, stale, or compared across inconsistent reporting periods.

Mitigation: Mark missing data clearly, downgrade conclusions when evidence is incomplete, and align report periods and technical-analysis windows before comparing stocks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-stock-analysis)
- [CLI command reference](artifact/references/cli-commands.md)
- [Error handling guide](artifact/references/error-handling.md)
- [Stock analysis report template](artifact/assets/report-template.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, ratings, risk notes, disclaimers, and inline CLI commands when setup or data collection is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output; requires explicit A-share targets; normalizes financial periods, time windows, and currency units for comparison.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
