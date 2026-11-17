## Description:

Pre-trade token safety scanner for 21+ EVM chains. 6-layer deep scan: contract safety, liquidity health, deployer profiling, holder distribution, trading patterns, social signals. Returns Guardian Score (0-100) with BUY/CAUTION/AVOID verdict. x402 USDC micropayments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request pre-trade safety scans for EVM token contracts and receive a Guardian Score, risk signals, and a BUY, CAUTION, or AVOID verdict before trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports unsafe input handling that could let crafted scan inputs run code.

Mitigation: Only approve scans for trusted token addresses and chain names until input validation is added and executable JavaScript argument embedding is removed.

Risk: The security guidance flags use of a fixed /tmp result path that could overwrite or expose scan results.

Mitigation: Run scans in an isolated environment and prefer a private, unique result path before relying on stored outputs.

Risk: Each scan uses a paid external token-scanning service through x402 USDC payments.

Mitigation: Require explicit per-scan approval and confirm wallet balance, network, and spend limits before execution.

## Reference(s):

- [SUPAH Token Guardian on ClawHub](https://clawhub.ai/supah-based/skills/supah-token-guardian)
- [Supported Chains](artifact/references/supported-chains.md)
- [x402 Protocol](https://www.x402.org)
- [SUPAH API](https://api.supah.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Terminal text report with a JSON result file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The scan command accepts a token address and optional chain, calls an external SUPAH API endpoint, and writes scan data to /tmp/guardian-result.json.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
