## Description:

TrencherAI provides paid Base chain token intelligence through x402-enabled API endpoints for scoring tokens, finding hot tokens, and reviewing smart money activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soynull](https://clawhub.ai/user/soynull)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to call TrencherAI endpoints for Base chain token screening, market scanning, portfolio monitoring, smart money tracking, and automated trading inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents with x402 wallet or Coinbase CDP payment capability may make repeated on-chain USDC payments without adequate spending controls.

Mitigation: Use a low-balance dedicated wallet, require explicit approval or strict budgets, pin the expected host, network, USDC contract, recipient, and maximum price, and avoid automated loops or retries.

Risk: Token scores and BUY, WATCH, or SKIP recommendations may be used as automated trading inputs for volatile Base chain assets.

Mitigation: Treat scores as advisory signals, apply independent checks before trading, and keep automated trading systems within explicit risk and spend limits.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/soynull/skills/trencherai-base-intelligence)
- [TrencherAI website](https://aitrencher.xyz)
- [x402 discovery document](https://api.aitrencher.xyz/.well-known/x402.json)
- [ERC-8004 agent registry](https://www.8004scan.io/agents/base/29167)
- [Coinbase CDP x402 facilitator](https://api.cdp.coinbase.com/platform/v2/x402)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Configuration]

**Output Format:** [Markdown with endpoint documentation, JavaScript examples, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes paid x402 request details for Base Mainnet USDC payments.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
