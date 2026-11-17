## Description:

The pre-trade data stack for crypto trading and sniping agents helps discover new and trending token launches, run token safety checks before buying, and pull live DEX price, liquidity, and buy/sell flow data over x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rccola990-cloud](https://clawhub.ai/user/rccola990-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to route crypto trading agents through a pre-trade workflow: discover candidate tokens, check risk signals, and retrieve live market data before deciding whether to trade.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger paid x402 USDC requests for live crypto-data calls.

Mitigation: Use wallet-side or client-side spending caps and require confirmation before paid requests.

Risk: Remote-supplied next_calls may lead agents into follow-up paid requests without clear cost controls.

Mitigation: Validate the destination, price, and total session cost before following remote next_calls automatically.

## Reference(s):

- [ClawHub Riley Crypto Trading](https://clawhub.ai/rccola990-cloud/skills/riley-crypto-trading)
- [AgentExchange x402 Store](https://store.agentexchange.work)
- [Crypto Launches Endpoint](https://store.agentexchange.work/crypto/launches?chain=solana&limit=15)
- [Crypto Security Endpoint](https://store.agentexchange.work/crypto/security?address=0x6982508145454ce325ddbe47a25d4ec3d2311933&chain=ethereum)
- [Crypto DEX Endpoint](https://store.agentexchange.work/crypto/dex?q=WIF)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with endpoint URLs and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an x402 payment client for paid live data calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
