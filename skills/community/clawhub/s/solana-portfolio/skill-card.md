## Description:

Solana Portfolio helps an agent manage read-only Solana portfolio workflows, including wallet tracking, token distribution, asset value, PnL, and educational rebalancing summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liji3597](https://clawhub.ai/user/liji3597)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to inspect Solana holdings across connected wallets, add or remove wallet records, list wallets, and request portfolio, PnL, or rebalancing summaries. The skill is intended for read-only portfolio visibility and does not require private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Caller-supplied Telegram user IDs could expose another user's wallet and portfolio records if the dispatcher does not bind requests to the authenticated user.

Mitigation: Deploy only behind a trusted dispatcher that supplies the authenticated user's own Telegram ID and blocks arbitrary user ID selection.

Risk: Wallet addresses, holdings, values, and PnL are sensitive financial metadata.

Mitigation: Treat portfolio outputs as private user data and avoid logging, sharing, or displaying them outside the user's authorized session.

Risk: The artifact includes rebalancing and PnL behavior that is not fully documented in the main skill instructions.

Mitigation: Review the included financial analysis scripts before installation and present rebalancing output as educational information, not investment advice.

## Reference(s):

- [Solana Portfolio ClawHub skill page](https://clawhub.ai/liji3597/skills/solana-portfolio)
- [liji3597 ClawHub publisher profile](https://clawhub.ai/user/liji3597)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text and JSON command output for agent-facing portfolio workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English responses are supported by script flags; portfolio output may include sensitive wallet, holding, value, PnL, and allocation metadata.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
