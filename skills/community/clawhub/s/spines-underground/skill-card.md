## Description:

Browse, search, access free content, and purchase curated poetry, philosophy, music theory, and consciousness content from Spine's Underground.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisamaraventano-spine](https://clawhub.ai/user/lisamaraventano-spine)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to browse Spine's Underground, retrieve free catalog items, search for content, and complete USDC purchases for paid items on Base or Solana.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags a mutable third-party MCP package for crypto purchases without pinning the reviewed code.

Mitigation: Use a pinned, reviewed package version and run the MCP server with minimal filesystem, environment, network, and wallet access.

Risk: Purchases involve direct USDC payments on Base or Solana.

Mitigation: Independently confirm the chain, token, recipient, amount, and transaction details before signing any payment.

## Reference(s):

- [Spine's Underground ClawHub skill page](https://clawhub.ai/lisamaraventano-spine/skills/spines-underground)
- [Publisher profile](https://clawhub.ai/user/lisamaraventano-spine)
- [Spine commerce API](https://spine.substratesymposium.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include catalog browsing, search results, free content, purchase guidance, and payment verification responses.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
