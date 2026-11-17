## Description:

Enables agents to discover x402-protected services, preview prices, check wallet balances, fund wallets when needed, and pay HTTP 402 resources after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pivortex](https://clawhub.ai/user/pivortex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent handle HTTP 402 and x402 payment workflows, including service discovery, price checks, wallet selection, optional funding, payment execution, and response reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can facilitate real blockchain payments, and loss of funds may be irreversible.

Mitigation: Require explicit human approval for every command and transaction, preview the decoded price before payment, and use a dedicated low-balance wallet.

Risk: Raw private keys and generic private-key environment variables can give an agent broad payment authority.

Mitigation: Prefer managed signer or wallet-provider flows with spend limits and allowlists, and avoid generic PRIVATE_KEY-style variables in shared agent environments.

Risk: Paid endpoints, service catalogs, facilitators, RPC providers, and cross-chain funding services may be unavailable, inaccurate, malicious, or subject to changing terms.

Mitigation: Review paid endpoint URLs, service details, wallet sessions, generated .env files, and funding/refund destinations before use.

Risk: A quoted price can change between preview and payment.

Mitigation: Recheck stale prices and pass the user-confirmed price as the payment command's hard cap so payment fails closed if the quote increases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pivortex/skills/x402-pay)
- [Project homepage](https://github.com/NearDeFi/agent-payments-skill)
- [Detecting Wallets](references/detecting-wallets.md)
- [Wallet Flows](references/wallet-flows.md)
- [NEAR Intents Funding](references/near-intents-funding.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paid endpoint responses, transaction hashes, decoded prices, wallet status, and funding instructions.]

## Skill Version(s):

2.0.0 (source: server release metadata, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
