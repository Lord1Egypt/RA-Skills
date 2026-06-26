## Description: <br>
Evaluates stablecoin depeg events for crisis arbitrage opportunities when a user asks whether to buy, watch, or avoid a depegged stablecoin. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[june-kris](https://clawhub.ai/user/june-kris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to triage stablecoin depeg events by combining current price, TVL signals, exploit-check prompts, and position-sizing guidance before deciding whether to buy, watch, or avoid. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading-style recommendations for depegged stablecoins may be wrong, stale, or financially harmful. <br>
Mitigation: Treat output as research, verify exploit facts, collateral status, liquidity, and team statements independently, and present BUY/WATCH/AVOID conclusions as non-authoritative. <br>
Risk: Live price and TVL data from external APIs can be missing, delayed, or matched to the wrong protocol. <br>
Mitigation: Cross-check CoinGecko and DefiLlama results against other reputable sources and complete the manual exploit-analysis checklist before sharing a recommendation. <br>
Risk: Exact capital inputs can reveal sensitive portfolio details. <br>
Mitigation: Use approximate capital ranges rather than exact portfolio values when running or discussing the assessment. <br>


## Reference(s): <br>
- [Depeg Assessment Decision Framework](references/decision-framework.md) <br>
- [CoinGecko API](https://api.coingecko.com/api/v3) <br>
- [DefiLlama API](https://api.llama.fi) <br>
- [ClawHub skill page](https://clawhub.ai/june-kris/stablecoin-depeg-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style recommendation with price, collateral, exploit-analysis, action, position-size, target, and stop-condition sections.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a BUY/WATCH/AVOID recommendation and manual verification checklist; does not execute trades.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
