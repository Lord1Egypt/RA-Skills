## Description:

Unified Dev Wallet Monitor for BSC and Solana - Monitor only, manual buy only, no private keys.

This skill is for research and development only.

## Publisher:

[mybusd](https://clawhub.ai/user/mybusd)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto researchers use this skill to monitor BSC and Solana developer wallet activity, record token-transfer detections, and receive manual DEX links for independent review. It does not require private keys or sign transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a reusable billing API key and client-side charging logic.

Mitigation: Rotate the published credential, move billing enforcement server-side, and require explicit user consent before any charge.

Risk: Monitoring logs and detection files can expose sensitive operational activity even when blockchain data is public.

Mitigation: Treat logs and detections as sensitive data, restrict access, and redact them before sharing for support or debugging.

Risk: Manual DEX links could be mistaken for trading recommendations or verified safe purchase paths.

Mitigation: Keep trading manual-only, require users to independently verify token contracts and DEX destinations, and avoid presenting detections as endorsements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mybusd/skills/sol-bsc-dev-monitor)
- [Jupiter Aggregator](https://jup.ag)
- [PancakeSwap](https://pancakeswap.finance/swap)
- [Solana mainnet RPC endpoint](https://api.mainnet-beta.solana.com)
- [BSC RPC endpoint](https://bsc-dataseed.binance.org)
- [SkillPay billing service](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON monitoring results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local log files and detection JSON files for BSC and Solana monitoring sessions.]

## Skill Version(s):

1.0.10 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
