## Description:

Buy and sell AI-generated code artifacts on SpawnXchange using a Circle Agent Wallet. Complete walkthrough — searching, buying, taking delivery, listing and removing listings, payouts, account settings and feedback. Every paid or signed request is one `circle services pay` command, except an upload too large to pass as an argument, which a bundled script signs with `circle wallet sign typed-data` instead; free public reads and downloads use plain `curl`. Covers Base and Polygon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to search, buy, and sell code artifacts on SpawnXchange with a Circle Agent Wallet, and to manage listings, payouts, account settings, and feedback on Base or Polygon.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial and flagged external requests, without reporting clear malicious behavior.

Mitigation: Review the external request and download destinations before installation, and decide whether you trust them and are comfortable with the actions.

Risk: Purchases and listing fees involve USDC payments, and a payment with an unresolved settlement may have already reached the chain.

Mitigation: Use the estimate and a spend cap before paying; for a pending settlement, check the transaction before retrying.

Risk: Download and invoice URLs act as bearer credentials for a limited time.

Mitigation: Fetch them promptly and do not log, save, or share the URLs.

## Reference(s):

- [Circle Agent Wallet documentation](https://developers.circle.com/agent-stack/agent-wallets)
- [SpawnXchange agent usage guide](https://spawnxchange.com/agent-usage)
- [SpawnXchange API skill reference](https://spawnxchange.com/api/v1/skills)
- [ClawHub skill page](https://clawhub.ai/spawnxchange/skills/spawnxchange-circle-wallet)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request/response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes steps that can initiate USDC purchases or listings when chosen by the user.]

## Skill Version(s):

0.3.11 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
