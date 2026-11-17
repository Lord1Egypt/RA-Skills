## Description:

Search for products on Amazon/shopify and buy with USDC on Solana. Swap tokens using Jupiter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xasus1](https://clawhub.ai/user/xasus1)

### License/Terms of Use:


## Use Case:

External users and agents use Scout Commerce to search for Amazon or Shopify products, review product details, place US-shipping orders paid with USDC on Solana, and swap supported wallet tokens.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can place product orders and execute token swaps from a funded Crossmint wallet.

Mitigation: Use an isolated environment, fund only limited amounts, and review purchase and swap commands before they run.

Risk: The skill stores an API key, wallet address, and shipping profile in local plaintext credentials.json.

Mitigation: Keep credentials.json private, avoid committing or sharing it, and rotate or revoke the API key if the file may have been exposed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/xasus1/skills/scout-commerce)
- [Scout homepage](https://scout.trustra.xyz)
- [Scout API v2](https://scout-api.trustra.xyz/api/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands; helper scripts return JSON or plain-text command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product presentations may include media attachments for product images.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
