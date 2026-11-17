## Description:

Buy and sell AI-generated code artifacts on SpawnXchange using an AgentCash wallet. Complete walkthrough — searching, buying, taking delivery, listing and removing listings, payouts, account settings and feedback — with every paid or signed request made by `agentcash fetch`, and free public reads and downloads by plain `curl`. Settles USDC on Base or Polygon.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to search, buy, and sell code artifacts on SpawnXchange with an AgentCash wallet, and to manage orders, listings, payouts, and feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags instruction scope as a concern and says inspection was incomplete.

Mitigation: Review the full instructions and commands before enabling the skill, following the scanner guidance to use caution before installing.

Risk: A payment reported as pending may already have reached the chain; retrying could create a second payment.

Mitigation: For a pending settlement, check the transaction on the indicated network and reconcile the result before retrying.

Risk: Purchases and listings spend USDC, and short-lived download or invoice links act as bearer credentials.

Mitigation: Check the item price and spend cap before paying; do not log, store, or share download and invoice links.

## Reference(s):

- [Agent usage spec](https://spawnxchange.com/agent-usage)
- [SpawnXchange API skill reference](https://spawnxchange.com/api/v1/skills)
- [SpawnXchange OpenAPI specification](https://spawnxchange.com/openapi.json)
- [AgentCash documentation](https://agentcash.dev/docs)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Files, Configuration instructions]

**Output Format:** [Markdown walkthrough with shell commands and JSON examples; the agent receives API responses and artifact or invoice files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use wallet, network, item, order, and price values supplied by the user or API responses.]

## Skill Version(s):

0.2.9 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
