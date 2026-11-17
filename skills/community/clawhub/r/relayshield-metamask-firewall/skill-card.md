## Description:

Use when the user asks anything about screening a MetaMask Agent Wallet action before it executes, protecting an agent that trades, swaps, bridges, or pays through the MetaMask `mm` CLI or a MetaMask MCP server, or routing MetaMask agent traffic through the RelayShield MCP Proxy Firewall. Single entry point for RelayShield screening of MetaMask agent write calls: pre-payment counterparty screening, payTo pin checks, and the hosted or self-hosted Firewall proxy. Screening is advice and enforcement at the tool call: it never replaces the human's approval, and it never moves funds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nzdsf2-gif](https://clawhub.ai/user/nzdsf2-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users operating MetaMask Agent Wallet can use this skill to screen wallet write actions and route MetaMask MCP calls through RelayShield. It provides pre-payment checks and proxy configuration guidance while keeping human approval required for every write.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious because it reports an unpinned installer that can fetch changing package and repository content, along with a mismatch between the stated wallet-screening purpose and reported installation behavior.

Mitigation: Review the publisher and installer behavior, and verify and inspect fetched content before installation, especially when using the skill alongside wallet tools.

Risk: The scan was partial: two references could not be resolved, and it did not establish what downloaded skills contain.

Mitigation: Review unresolved references and inspect the complete installed contents before enabling the skill.

Risk: Unknown verdicts do not block calls, and a screening timeout fails open, so a write may proceed without a conclusive screening result.

Mitigation: Keep human approval enabled for every write and independently review the recipient and transaction before approving.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nzdsf2-gif/skills/relayshield-metamask-firewall)
- [MetaMask Agent Wallet quickstart](https://docs.metamask.io/agent-wallet/quickstart/)
- [RelayShield developer documentation](https://api.relayshield.net/developers)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet screening guidance for reads and write actions; human approval remains required for writes.]

## Skill Version(s):

0.1.0 (source: frontmatter; agrees with server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
