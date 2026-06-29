## Description: <br>
Live macro, markets, and developer ecosystem data for research, finance, forecasting, and trading agents through low-cost x402 GET calls with no API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents, developers, finance researchers, forecasting workflows, and trading assistants use this skill to retrieve live macroeconomic indicators, Treasury data, yield spreads, and developer ecosystem signals through exact market-data endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 endpoint calls can spend small amounts of USDC. <br>
Mitigation: Use a payment client or wallet policy that requires review, budget limits, or approval before paid calls are retried after HTTP 402 responses. <br>
Risk: Live market and macro data may be stale, unavailable, or unsuitable as a sole basis for financial decisions. <br>
Mitigation: Treat returned data as research input, verify important figures against authoritative sources, and apply domain review before trading or forecasting decisions. <br>


## Reference(s): <br>
- [ClawHub Riley Market Data release page](https://clawhub.ai/rccola990-cloud/riley-market-data) <br>
- [AgentExchange market-data catalog](https://store.agentexchange.work/) <br>
- [AgentExchange market-data samples](https://store.agentexchange.work/samples) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with exact HTTP GET endpoints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid endpoints use x402 USDC payments on Base; free catalog and sample endpoints are available before paid calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
