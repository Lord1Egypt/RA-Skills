## Description: <br>
Weather-driven demand forecasting that correlates temperature with energy and commodity trade flows and provides Holt-Winters predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drivenbymyai-max](https://clawhub.ai/user/drivenbymyai-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to forecast weather-driven energy or commodity demand, inspect temperature-trade seasonality, and plan inventory around expected demand changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends trade and forecasting parameters to a third-party service. <br>
Mitigation: Confirm the provider is approved before sending sensitive proprietary demand, inventory, or forecasting assumptions. <br>
Risk: The demand forecast endpoint is documented as a paid x402 request. <br>
Mitigation: Approve paid requests intentionally and review parameters before execution. <br>
Risk: Forecasts and seasonality analysis may be incomplete or inaccurate for operational planning. <br>
Mitigation: Use the output as decision support and validate results against internal demand, inventory, and market data. <br>


## Reference(s): <br>
- [Weather Demand ClawHub page](https://clawhub.ai/drivenbymyai-max/weather-demand) <br>
- [SputnikX homepage](https://sputnikx.xyz) <br>
- [Weather Demand API base](https://sputnikx.xyz/api/v1/agent) <br>
- [Demand forecast endpoint](https://sputnikx.xyz/api/v1/agent/trade/demand-forecast?reporter=LV&hs2=27&months=6) <br>
- [Weather and trade seasonality endpoint](https://sputnikx.xyz/api/v1/agent/trade/seasonality?reporter=LV&hs2=27) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, markdown] <br>
**Output Format:** [Markdown with inline bash code blocks and API response interpretation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve a third-party API and a disclosed paid x402 endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
