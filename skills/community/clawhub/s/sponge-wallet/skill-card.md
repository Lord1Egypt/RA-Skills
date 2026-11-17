## Description:

Manages crypto wallets, transfers tokens, swaps on DEXes, checks balances, and accesses paid APIs (search, image gen, prediction markets, web scraping, document parsing, sales prospecting) via x402 micropayments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rishabluthra](https://clawhub.ai/user/rishabluthra)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Sponge wallet balances, transfers, swaps, transaction history, funding requests, withdrawals, and paid x402 API calls from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move wallet funds through transfers, swaps, withdrawals, signed payments, and auto-paid API requests.

Mitigation: Prefer test keys and small balances, and manually confirm every transfer, swap, withdrawal, signed payment, and auto-paid API request before execution.

Risk: Wallet credentials are stored locally at ~/.spongewallet/credentials.json or provided through SPONGE_API_KEY.

Mitigation: Treat stored credentials and environment keys as sensitive secrets, restrict local file access, and remove credentials with logout when no longer needed.

Risk: Overriding SPONGE_API_URL can direct authentication and wallet calls to an untrusted endpoint.

Mitigation: Use only the default Sponge API endpoint or a Sponge endpoint that the user fully controls and trusts.

Risk: The paid API interface can auto-pay for services by default.

Mitigation: Set auto_pay to false when previewing payment requirements or when the user needs explicit approval before a paid request.

## Reference(s):

- [Sponge Wallet Skill Page](https://clawhub.ai/rishabluthra/skills/sponge-wallet)
- [README.md](README.md)
- [SKILL.md](SKILL.md)
- [REFERENCE.md](REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Wallet and paid API commands return JSON status objects with success or error states.]

## Skill Version(s):

1.0.0 (source: server evidence release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
