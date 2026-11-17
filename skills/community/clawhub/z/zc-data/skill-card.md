## Description:

Queries Zhuochuang commodity-market data for prices, inventory, costs, imports and exports, supply and demand, futures and spot prices, and historical trends across commodity categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaifb](https://clawhub.ai/user/zhaifb)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to retrieve current provider-sourced commodity-market data instead of relying on stale model knowledge. It is suited for questions about prices, quotes, inventory, costs, margins, supply and demand, imports and exports, and recent market trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commodity-market queries and the XZ_APIKEY are sent to Zhuochuang's external API.

Mitigation: Install only when this data sharing is acceptable, keep the API key in the XZ_APIKEY environment variable, and avoid exposing credentials in prompts or logs.

Risk: Returned market data is provider-sourced and may affect trading, procurement, or business decisions.

Mitigation: Confirm data freshness, source, API key ownership, and billing terms before using outputs for operational decisions.

## Reference(s):

- [Zhuochuang data search API](https://api.zhuochuang.com/openclaw/data-search)
- [ClawHub skill page](https://clawhub.ai/zhaifb/skills/zc-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown text with optional JSON response fields and curl or Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided XZ_APIKEY and sends market-data queries to Zhuochuang's external API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
