## Description:

Analyzes financial news, industry trends, selected stocks, technical indicators, and sentiment to produce stock-industry analysis reports.

This skill is for research and development only.

## Publisher:

[ligo-gao](https://clawhub.ai/user/ligo-gao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to generate research-oriented summaries of financial news, industry heat, sentiment, technical indicators, stock scores, and watchlist-style suggestions. Its output should be treated as informational analysis, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may include fabricated or randomized market data while presenting trading-style suggestions.

Mitigation: Use only after verifying live data provenance, clearly label simulated data, and do not rely on generated reports for trading decisions.

Risk: Automated or scheduled runs can repeatedly persist unverified analysis and reports.

Mitigation: Avoid cron automation until outputs are trustworthy, and review generated reports before distribution or downstream use.

Risk: The skill stores news, stock records, logs, and reports locally for extended periods.

Mitigation: Review local retention settings and disable or shorten long-term storage when report history or source data should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ligo-gao/skills/stock-industry-analyzer)
- [Artifact README](artifact/README.md)
- [Artifact skill documentation](artifact/SKILL.md)
- [Configuration reference](artifact/config.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain-text and Markdown-style reports with tables, scores, links, and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write reports and analysis history to local SQLite tables and report files when run in persistent mode.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact README, artifact config.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
