## Description: <br>
SUPAH Pulse provides real-time crypto market intelligence briefings with market regime, fear and greed, BTC and ETH dominance, gas costs, trending tokens, top movers, DeFi TVL shifts, liquidations, and a 0-100 Market Pulse Score using x402 USDC micropayments on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supah-based](https://clawhub.ai/user/supah-based) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and crypto-focused agents use this skill to get a paid, real-time market briefing before trading, allocation, or advisory workflows. It summarizes market conditions and writes structured results that an agent can inspect. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger paid x402 calls that spend USDC on Base. <br>
Mitigation: Use a low-balance wallet or spending limits, and require explicit confirmation before paid calls when the host agent supports it. <br>
Risk: The market briefing may be mistaken for financial advice. <br>
Mitigation: Treat outputs as market data and analysis only; require human review before trading, allocation, or advisory decisions. <br>
Risk: SUPAH_API_BASE can redirect the paid SUPAH request to an alternate endpoint. <br>
Mitigation: Leave SUPAH_API_BASE unset unless the alternate endpoint is trusted. <br>
Risk: The script writes its JSON result to /tmp/market-pulse-result.json. <br>
Mitigation: Run in an environment where temporary-file writes are acceptable and review the file before reusing it in downstream workflows. <br>


## Reference(s): <br>
- [SUPAH Pulse on ClawHub](https://clawhub.ai/supah-based/supah-pulse) <br>
- [supah-based publisher profile](https://clawhub.ai/user/supah-based) <br>
- [x402 protocol](https://www.x402.org) <br>
- [SUPAH API](https://api.supah.ai) <br>
- [CoinGecko global market API](https://api.coingecko.com/api/v3/global) <br>
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/?limit=7) <br>
- [DeFiLlama chains API](https://api.llama.fi/v2/chains) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text briefing with a JSON result file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports focus values full, quick, defi, and gas; writes /tmp/market-pulse-result.json; paid SUPAH calls use x402 USDC micropayments on Base.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
