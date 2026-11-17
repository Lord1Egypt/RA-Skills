## Description:

Stellar Agent Wallet lets AI agents manage a Stellar USDC hot wallet for 402-gated API payments, balance and trustline checks, XLM-to-USDC swaps, direct Stellar payments, and USDC bridge or cross-chain sends through MPP Router, x402 facilitators, and Rozo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawnmuggle](https://clawhub.ai/user/shawnmuggle)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent builders use this skill to let an AI agent operate a limited-balance Stellar USDC wallet for paid API calls, account setup checks, direct payments, and supported cross-chain USDC transfers. It is intended for controlled hot-wallet workflows where the user reviews mainnet spending and pins expected payment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move real funds from a Stellar hot wallet.

Mitigation: Use a dedicated low-balance wallet, test on testnet first, and avoid connecting a primary wallet.

Risk: A paid API URL or 402 challenge can influence payment recipient, asset, amount, and async polling destinations.

Mitigation: Pin expected recipient, asset, and amount with the documented expectation flags before signing payments.

Risk: Unattended payment flags can bypass normal confirmation in limited workflows.

Mitigation: Avoid --yes and --max-auto on mainnet unless the expected payment details are independently verified and automation limits are intentionally narrow.

Risk: File-based wallet secrets are plaintext and can be spent by anyone who can read them.

Mitigation: Store only expendable funds in the hot wallet, keep secret files at mode 600, and prefer Stellar CLI identities where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawnmuggle/skills/stellar-agentic-wallet)
- [Publisher profile](https://clawhub.ai/user/shawnmuggle)
- [MPP Router homepage](https://www.mpprouter.dev/)
- [Repository metadata](https://github.com/mpprouter/stellar-agent-wallet-skill)
- [Mainnet checklist](references/mainnet-checklist.md)
- [Sponsored mode](references/sponsored-mode.md)
- [MPP charge spec](references/mpp-charge-spec.md)
- [x402 exact spec](references/x402-exact-spec.md)
- [SDK API cheatsheet](references/sdk-api-cheatsheet.md)
- [Verifying refunds](references/verifying-refunds.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text, with optional JSON output from wallet scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands submit signed Stellar transactions or call user-selected paid API URLs; mainnet use can move real funds.]

## Skill Version(s):

1.8.8 (source: server release evidence, frontmatter metadata, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
