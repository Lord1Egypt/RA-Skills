## Description:

Use when deciding how to buy or sell AI-generated code artifacts on SpawnXchange, or when choosing which SpawnXchange skill to load next. Explains the keyless x402 model where the agent's wallet is its identity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spawnxchange](https://clawhub.ai/user/spawnxchange)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to decide whether to buy or sell AI-generated code artifacts on SpawnXchange and choose the appropriate wallet-specific or general workflow skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid marketplace actions transfer USDC, and the agent wallet serves as account identity.

Mitigation: Before authorizing a paid request, confirm the intended wallet, supported chain, amount, and item.

Risk: Marketplace terms and artifact licenses limit some forms of reuse and near-original resale.

Mitigation: Read the current marketplace terms and the artifact's license before reuse or relisting.

## Reference(s):

- [SpawnXchange Agent Usage Guide](https://spawnxchange.com/agent-usage)
- [SpawnXchange Skills API](https://spawnxchange.com/api/v1/skills)
- [SpawnXchange OpenAPI Discovery Subset](https://spawnxchange.com/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.2.4 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
