## Description: <br>
Riley Crypto Trading helps agents discover new and trending crypto token launches, run pre-trade safety checks, and retrieve live DEX, price, yield, and prediction-market data through paid x402 GET APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto research agent builders use this skill to poll token launches, evaluate token risk, and retrieve market data before deciding whether to take action. It is intended for read-only pre-trade research and decision support, not autonomous trading approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 API calls can spend funds from the payment client or wallet used by the agent. <br>
Mitigation: Use only with a payment client or wallet budget you control, set spending limits, and review call patterns before enabling automation. <br>
Risk: Crypto market data and token safety checks can be incomplete, stale, or unsuitable as financial advice. <br>
Mitigation: Require independent verification and human approval before any buy, sell, or allocation decision. <br>
Risk: The skill is read-only, but a downstream agent could combine its guidance with separate trading tools. <br>
Mitigation: Keep data retrieval separate from trade execution and gate any trading tool behind explicit user authorization. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rccola990-cloud/riley-crypto-trading) <br>
- [x402 Agent Store API Base](https://store.agentexchange.work) <br>
- [New and Trending Token Launches Endpoint](https://store.agentexchange.work/crypto/launches?chain=solana&limit=15) <br>
- [Pre-Trade Security Check Endpoint](https://store.agentexchange.work/crypto/security?address=0x6982508145454ce325ddbe47a25d4ec3d2311933&chain=ethereum) <br>
- [Live DEX Token Data Endpoint](https://store.agentexchange.work/crypto/dex?q=WIF) <br>
- [CoinGecko Token Prices Endpoint](https://store.agentexchange.work/crypto/prices?ids=bitcoin,ethereum) <br>
- [DeFi Yields Endpoint](https://store.agentexchange.work/defi/yields?chain=Base&min_tvl=10000000) <br>
- [Prediction Market Odds Endpoint](https://store.agentexchange.work/markets/prediction?q=bitcoin&top=5) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with x402 GET endpoint URLs and query examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses paid read-only x402 API calls; no hidden code, trading execution, or persistence is indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
