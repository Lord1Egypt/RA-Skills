## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns whale leaderboard sentiment derived from Hyperliquid top traders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Trading agents can request whale leaderboard sentiment as one input when assessing market positioning or considering a trade entry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated endpoint requests incur USDC charges and can accumulate costs.

Mitigation: Set an explicit maximum payment amount in the x402 client and review the charge before making repeated requests.

## Reference(s):

- [Whale Sentiment endpoint](https://apexrunner.ai/signals/whale-sentiment)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/whale-sentiment)
- [Related signal: liquidation pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [Related signal: agent conviction score](https://apexrunner.ai/signals/agent-conviction-score)

## Skill Output:

**Output Type(s):** [JSON, Market sentiment data]

**Output Format:** [JSON response containing sentiment, score, and top-trader long percentage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid endpoint response per request; requests use x402 payment in USDC on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
