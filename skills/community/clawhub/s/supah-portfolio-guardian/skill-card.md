## Description:

Automated wallet monitoring with real-time alerts for portfolio value, suspicious-transaction signals, approval monitoring, and risk warnings across Base and EVM chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[supah-based](https://clawhub.ai/user/supah-based)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to query SUPAH for watched-wallet management, portfolio health checks, risk alert checks, and rebalance suggestions for Base and EVM wallets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends wallet addresses and portfolio queries to SUPAH or the configured API endpoint.

Mitigation: Use it only for wallet data you are comfortable sharing with SUPAH or the configured endpoint.

Risk: The security evidence warns that the skill overstates protection for real-time transactions, approvals, and suspicious transfers.

Mitigation: Do not rely on it as a real-time protection control; review results before making financial or security decisions.

Risk: The local state file stores watched-wallet tracking metadata.

Mitigation: Treat the local state file as sensitive, restrict filesystem access, and remove watched wallets when monitoring is no longer needed.

Risk: The skill uses x402 USDC micropayments for paid API calls.

Mitigation: Configure payment limits and review per-call costs before enabling automatic agent use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/supah-based/skills/supah-portfolio-guardian)
- [SUPAH API endpoint](https://api.supah.ai)
- [x402 documentation](https://www.x402.org)
- [SUPAH website](https://supah.ai)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON responses with brief CLI status and cost text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, curl, SUPAH_API_BASE, outbound HTTPS to api.supah.ai, and x402 USDC payment support on Base.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
