## Description:

SUPAH Pulse provides real-time crypto market intelligence, including market regime, sentiment, asset dominance, gas costs, DeFi TVL shifts, liquidations, and a Market Pulse Score for agent decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to request a concise crypto market briefing before trading, allocation, advisory, or monitoring workflows. The briefing combines paid SUPAH regime data with public market, sentiment, and DeFi data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically spend wallet USDC through x402 paid calls.

Mitigation: Run it only in environments where paid calls require user approval or strict wallet spending limits.

Risk: The authoritative security summary reports a local temporary-file overwrite risk.

Mitigation: Avoid running the skill with elevated privileges until the /tmp output path is fixed.

Risk: Crypto market briefings and tactical suggestions can be incorrect, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as decision-support context, not financial advice, and require human review before trading or allocation decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/supah-based/skills/supah-pulse)
- [Publisher Profile](https://clawhub.ai/user/supah-based)
- [x402 Protocol](https://www.x402.org)
- [SUPAH API](https://api.supah.ai)
- [CoinGecko Global Market API](https://api.coingecko.com/api/v3/global)
- [Alternative.me Fear & Greed API](https://api.alternative.me/fng/?limit=7)
- [DeFiLlama Chains TVL API](https://api.llama.fi/v2/chains)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text briefing plus JSON result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and Node.js; may require SUPAH_API_BASE; writes JSON output to /tmp/market-pulse-result.json.]

## Skill Version(s):

2.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
