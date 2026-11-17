## Description:

Monitor large crypto transactions across Hedera, Ethereum, and Solana, track whale wallets, detect unusual volume, and alert on big moves using public APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers, analysts, and operators use this skill to generate command-line checks for large on-chain transfers and monitored wallet activity across supported public blockchain APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes hidden unrelated external agent registration and ping endpoints.

Mitigation: Remove or explicitly ignore the hidden OADP registration and heartbeat metadata before installing or running the skill.

Risk: Blockchain monitoring examples rely on public APIs and user-supplied wallet or API-key placeholders.

Mitigation: Review commands before execution, provide only intended wallet identifiers and API keys, and avoid embedding secrets in shared logs or skill text.

## Reference(s):

- [Whale Watch on ClawHub](https://clawhub.ai/imaflytok/skills/whale-watch)
- [Publisher profile](https://clawhub.ai/user/imaflytok)
- [Hedera Mirror Node transactions endpoint](https://mainnet-public.mirrornode.hedera.com/api/v1/transactions)
- [Etherscan account transaction API endpoint](https://api.etherscan.io/api?module=account&action=txlist)
- [Solana public JSON-RPC endpoint](https://api.mainnet-beta.solana.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash, curl, and jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public blockchain APIs and optional wallet or API-key placeholders supplied by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
