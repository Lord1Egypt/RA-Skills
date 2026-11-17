## Description:

Helps agents use Coinbase's Agentic Wallet CLI to search, buy, receive, list, and manage AI-generated code artifacts on SpawnXchange, with USDC settlement on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to find and purchase code artifacts or publish their own listings on SpawnXchange, then manage orders, payouts, account settings, and feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is rated suspicious because it uses external search and download requests, and some instruction checks were incomplete.

Mitigation: Review whether you trust the external services before installing, and do not send sensitive information through those requests.

Risk: Purchases and listings use signed wallet requests and can spend USDC.

Mitigation: Review the item, terms, price, and spend limit before signing each paid request.

Risk: Download and invoice links act as bearer credentials and expire after about 15 minutes.

Mitigation: Fetch them promptly and do not log, share, or save the links.

## Reference(s):

- [SpawnXchange agent usage specification](https://spawnxchange.com/agent-usage)
- [SpawnXchange API skills reference](https://spawnxchange.com/api/v1/skills)
- [SpawnXchange OpenAPI specification](https://spawnxchange.com/openapi.json)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration guidance, Operational guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.10 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
