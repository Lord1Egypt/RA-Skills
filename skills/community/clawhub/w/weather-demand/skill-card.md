## Description:

Weather-driven demand forecasting that correlates temperature with energy and commodity trade flows and returns Holt-Winters predictions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading or operations teams use this skill to forecast weather-driven energy or commodity demand and examine temperature-trade seasonality for Baltic trade flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External API calls may incur paid x402 charges or send request parameters to a third-party service.

Mitigation: Require user approval before invoking paid endpoints and review reporter, commodity, and time-window parameters before sending requests.

Risk: Forecast and correlation outputs may be inaccurate or unsuitable for operational decisions without domain review.

Mitigation: Treat results as decision support and have analysts validate assumptions, confidence intervals, and downstream actions.

## Reference(s):

- [Weather Demand ClawHub Skill Page](https://clawhub.ai/drivenbymyai-max/skills/weather-demand)
- [SputnikX Homepage](https://sputnikx.xyz)
- [Weather Demand API Base URL](https://sputnikx.xyz/api/v1/agent)
- [Demand Forecast Endpoint Example](https://sputnikx.xyz/api/v1/agent/trade/demand-forecast?reporter=LV&hs2=27&months=6)
- [Weather and Trade Correlation Endpoint Example](https://sputnikx.xyz/api/v1/agent/trade/seasonality?reporter=LV&hs2=27)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline bash examples and API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external paid demand-forecast API endpoint disclosed in the skill.]

## Skill Version(s):

1.0.0 (source: release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
