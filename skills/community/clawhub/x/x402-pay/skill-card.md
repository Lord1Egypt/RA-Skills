## Description: <br>
A skill for making HTTP 402 (x402) USDC micropayments on Base, discovering paid x402 services, checking prices and balances, and funding wallets through supported flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pivortex](https://clawhub.ai/user/pivortex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill when an agent needs to access x402-protected HTTP resources, preview payment requirements, check wallet funding, or make user-approved paid API calls. It is also used to guide wallet setup and cross-chain funding for Base USDC payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent spend real crypto funds or sign payment transactions. <br>
Mitigation: Use a dedicated low-balance wallet, keep wallet-level spend limits and allowlists enabled, and review every command, price, recipient, and transaction before approval. <br>
Risk: A paid endpoint price or funding quote may exceed the user's intended spend. <br>
Mitigation: Preview the live price before payment, pass the confirmed value as the hard payment cap, and rely on the included fail-closed checks when price requirements cannot be verified. <br>
Risk: Broad private-key environment variables may expose funds that were intended for other tools. <br>
Mitigation: Prefer managed wallet flows or the namespaced X402_PRIVATE_KEY variable, and confirm with the user before using generic private-key aliases. <br>
Risk: Cross-chain funding can fail, expire, or refund to the wrong destination. <br>
Mitigation: Confirm the refund address, chain, memo requirement, quote deadline, and funding amount before sending any deposit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pivortex/x402-pay) <br>
- [Project homepage](https://github.com/NearDeFi/agent-payments-skill) <br>
- [Detecting wallets](references/detecting-wallets.md) <br>
- [Wallet flows](references/wallet-flows.md) <br>
- [NEAR Intents funding](references/near-intents-funding.md) <br>
- [Onramp funding](references/onramp-funding.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report service details, decoded prices, wallet balances, funding quotes, response bodies, and transaction hashes.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
