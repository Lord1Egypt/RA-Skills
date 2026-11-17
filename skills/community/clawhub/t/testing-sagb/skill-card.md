## Description:

Bags is a Solana launchpad skill for authenticating agents, managing wallets, claiming fees, trading tokens, and launching tokens for agents or humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramyonsn](https://clawhub.ai/user/ramyonsn)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to connect an agent to Bags, manage Solana wallet workflows, claim launch fees, request token trades, and create token launches with fee sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over real Solana assets, including trades, fee claims, launches, posts, and signed transactions.

Mitigation: Review each financial or posting action before approval, and do not allow unattended trades, launches, fee claims, or transaction submissions.

Risk: The skill handles long-lived Bags credentials, API keys, and exported private keys that can compromise accounts or wallets if exposed.

Mitigation: Use a wallet or signer that does not export raw private keys when possible, protect ~/.config/bags/credentials.json and signing material, and rotate credentials after any suspected exposure.

Risk: Heartbeat behavior and remote skill files can silently change or update operational instructions.

Mitigation: Do not run heartbeat auto-updates silently; pin and verify dependencies and remote files before using updated instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ramyonsn/skills/testing-sagb)
- [Bags homepage](https://bags.fm)
- [Bags API documentation](https://docs.bags.fm)
- [Bags skill manifest](https://bags.fm/skill.json)
- [Bags authentication guide](https://bags.fm/auth.md)
- [Bags wallet guide](https://bags.fm/wallets.md)
- [Bags fee claiming guide](https://bags.fm/fees.md)
- [Bags trading guide](https://bags.fm/trading.md)
- [Bags token launch guide](https://bags.fm/launch.md)
- [Bags public API base](https://public-api-v2.bags.fm/api/v1)
- [Bags agent API base](https://public-api-v2.bags.fm/api/v1/agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, API calls, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for Bags API calls, credential setup, transaction signing, fee claiming, trading, token launches, and heartbeat checks.]

## Skill Version(s):

2.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
