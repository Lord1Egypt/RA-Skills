## Description:

Sector Scanner helps an agent scan Chinese A-share theme sectors, rank sector heat and capital-flow labels, and summarize stock-level scoring details from TDX market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to fetch TDX market data, score configured A-share sectors, and present rankings, capital-flow summaries, and selected stock details. The results are for market organization and review, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on live TDX and Sina market-data endpoints, so output can be unavailable, stale, incomplete, or unauthenticated.

Mitigation: Run it in an isolated Python environment, review the pytdx dependency, and treat rankings as informational market summaries rather than integrity-protected financial data.

Risk: The generated rankings and capital-flow labels could be mistaken for investment recommendations.

Mitigation: Present results as analysis aids only and retain the artifact's warning that scores do not constitute investment advice.

## Reference(s):

- [Scoring Rules](references/scoring_rules.md)
- [ClawHub skill page](https://clawhub.ai/hunkguo/skills/sector-scanner)
- [Sina Finance API endpoint](http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/)
- [Sina Finance](http://finance.sina.com.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with JSON or CSV scan results and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Progress messages are written separately from machine-readable JSON output; CSV export can create ranking and detail files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
