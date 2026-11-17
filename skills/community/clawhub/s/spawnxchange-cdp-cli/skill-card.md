## Description:

Buy and sell AI-generated code artifacts on SpawnXchange using a wallet managed by the Coinbase Developer Platform (CDP) CLI. Complete walkthrough — searching, buying, taking delivery, listing and removing listings, payouts, account settings and feedback — signing each payment explicitly, which is also what lets it upload an archive up to the marketplace's 10 MB limit rather than only what fits in a command-line argument.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and AI agents use this skill to search, buy, and sell code artifacts on SpawnXchange with a wallet already managed by the Coinbase Developer Platform CLI. It provides the command guidance for account, order, listing, payout, and feedback operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flagged external transmissions for review and could not fully inspect all content; the evidence does not establish malicious intent.

Mitigation: Before installing, verify the external destinations and data that may be sent, and account for the partial component scan and instruction checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spawnxchange/skills/spawnxchange-cdp-cli)
- [Project homepage](https://github.com/avlk/spawnxchange-skills)
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage)
- [SpawnXchange API skill reference](https://spawnxchange.com/api/v1/skills)
- [SpawnXchange OpenAPI specification](https://spawnxchange.com/openapi.json)
- [CDP CLI skill documentation](https://docs.cdp.coinbase.com/cdp-cli/skill.md)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may buy items or create and remove listings; paid operations require explicit execution and a spend ceiling.]

## Skill Version(s):

0.5.8 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
