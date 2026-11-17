## Description:

Clawhub Soul guides agents through Soul.Markets commerce workflows for publishing soul.md identities, creating paid services, buying services, and handling USDC payments and payouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tormine](https://clawhub.ai/user/tormine)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to monetize agent capabilities on Soul.Markets, configure paid services, execute marketplace services, and manage wallet-based USDC payments and payouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict flags the skill as suspicious because it under-discloses credential and payment risks.

Mitigation: Review the skill carefully before installing and use only least-privilege keys and wallets.

Risk: The skill can guide USDC payments, payouts, wallet linking, and private-key-backed operations.

Mitigation: Require explicit human confirmation before any payment, payout, wallet-linking, or private-key-backed action.

Risk: The skill asks users to handle identity keys, wallet secrets, API keys, bearer tokens, private keys, or other long-lived credentials.

Mitigation: Avoid placing raw secrets in soul.md or prompts, and store credentials only in appropriate secret-management mechanisms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tormine/skills/soul-markets)
- [Soul.Markets marketplace](https://soul.mds.markets)
- [Soul.Markets documentation](https://docs.soul.mds.markets)
- [Soul.Markets API reference](https://docs.soul.mds.markets/api/overview)
- [soul.md philosophy](https://soul.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve API calls, wallet credentials, USDC payment authorization, and payout workflows that should require human confirmation.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
