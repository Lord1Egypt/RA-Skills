## Description:

Live macro, markets, and developer-ecosystem data for research, finance, forecasting, and trading agents through low-cost x402 GET calls with no API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to retrieve live macroeconomic, market, and developer ecosystem data for research, forecasting, finance, and trading workflows through paid or preview GET endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger small paid x402 requests to store.agentexchange.work through the agentcash MCP.

Mitigation: Confirm payment behavior before installation and set wallet or spending limits when the client supports them.

Risk: Live market and macroeconomic data may be inappropriate as the sole basis for financial or trading decisions.

Mitigation: Validate important results against authoritative sources and apply human review for finance, forecasting, or trading workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rccola990-cloud/skills/riley-market-data)
- [Agent Store catalog](https://store.agentexchange.work/)
- [Agent Store samples](https://store.agentexchange.work/samples)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Markdown guidance with endpoint URLs and GET call instructions; live API responses depend on the selected endpoint.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses x402 GET calls; paid endpoints return HTTP 402 before the client signs payment and retries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
