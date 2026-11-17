## Description:

Provides authenticated access to Wendian Starmap market intelligence, including real-time quotes, K-line bars, heatmaps, sector rotation analytics, concept linkage, trading calendars, reference data, futures snapshots, and strategy screeners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wendian-ai](https://clawhub.ai/user/wendian-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query Wendian Starmap for market data, heatmaps, sector rotation signals, concept membership, and stock screening workflows. Outputs support research, dashboards, charting, and analysis, not direct financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the Wendian API key and market-data query parameters to markethot.wendian.net.

Mitigation: Use a dedicated Wendian Starmap API key, keep it scoped to this service, and avoid placing unrelated sensitive data in request parameters or generated files.

Risk: Market strategies, stock screeners, and heatmap outputs may be mistaken for investment advice.

Mitigation: Treat returned data as research input and require appropriate financial, compliance, or human review before making trading or investment decisions.

Risk: Large date ranges, broad heatmaps, or oversized batch symbol lists can produce large responses or timeouts.

Mitigation: Keep date_count, limit, columns_count, and batch symbol lists within the documented bounds and prefer narrower queries for interactive use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wendian-ai/skills/wendian-stock-skill)
- [Wendian Starmap](https://markethot.wendian.net)
- [Wendian Starmap Skill Data API base URL](https://markethot.wendian.net/app-api/member/skill-data)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with API endpoint descriptions, curl examples, and JSON request bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WENDIAN_MARKETHOT_APIKEY and sends user-directed market-data query parameters to Wendian Starmap.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
