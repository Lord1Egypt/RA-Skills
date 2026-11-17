## Description:

TigerPass guides AI agents in using a hardware-secured crypto wallet and trading terminal for Hyperliquid trading, Polymarket prediction markets, DEX swaps, cross-chain USDC bridging, smart contract execution, x402 payments, and encrypted agent-to-agent commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigerpassnet](https://clawhub.ai/user/tigerpassnet)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to configure and operate autonomous crypto workflows, including wallet initialization, trading, token transfers, DeFi contract calls, cross-chain bridging, payment signing, and agent-to-agent commerce.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an autonomous agent broad real-money signing authority over crypto assets.

Mitigation: Install only when autonomous crypto control is intended, start in TIGERPASS_ENV=test, and enforce explicit spend, protocol, chain, recipient, and merchant limits.

Risk: The skill installs and depends on an external tigerpass CLI that the security evidence describes as unverified.

Mitigation: Prefer pinned, signed releases with checksum verification before allowing the CLI to control funded wallets.

Risk: Unattended listeners, auto-trading flows, unsolicited invoices, or unverified command messages can trigger unwanted payments or transactions.

Mitigation: Do not leave listener or auto-trading flows running without an enforceable policy; verify ownerVerified messages, payment recipients, contracts, spenders, chains, and x402 merchants before execution.

Risk: Unlimited token approvals, custom contract execution, cross-chain bridging, and sequential batch transactions can expose funds if parameters are wrong or one step fails.

Mitigation: Use simulation where available, avoid unlimited approvals where possible, verify allowances and contract addresses against official protocol docs, and inspect transaction results before retrying.

## Reference(s):

- [TigerPass ClawHub Skill Page](https://clawhub.ai/tigerpassnet/skills/tigerpass)
- [TigerPass Homepage](https://tigerpass.net)
- [DeFi & Trading Cookbook](references/defi-cookbook.md)
- [Advanced Commands - Smart Contracts, Signing & x402](references/advanced-commands.md)
- [ACE Agent Commerce Engine](references/ace-protocol.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI operations return JSON to stdout; normal use requires macOS on Apple Silicon and the tigerpass binary.]

## Skill Version(s):

0.1.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
