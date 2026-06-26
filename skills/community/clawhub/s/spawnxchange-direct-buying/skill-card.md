## Description: <br>
Use when completing public SpawnXchange direct purchases through /api/v1/items/{uuid}/acquire, verifying artifact delivery, and maintaining buyer state via the included references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to search SpawnXchange listings, inspect x402 payment quotes, complete direct USDC purchases with explicit consent, verify delivery URLs, and maintain durable local purchase records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can assist with real wallet-backed USDC purchases when the executable example is run with --execute. <br>
Mitigation: Use quote-only mode first, inspect the payment quote, execute only with explicit approval, and use a dedicated low-balance wallet. <br>
Risk: Plaintext private keys, payment headers, signed download URLs, purchase records, and cached artifacts can expose funds or purchase history. <br>
Mitigation: Keep these materials out of git, logs, chat transcripts, shared folders, and unencrypted backups; use owner-only permissions for local purchase state. <br>
Risk: A completed purchase returns a short-lived download URL and downloaded artifacts may still need review before use. <br>
Mitigation: Verify delivery reachability, cache artifacts only in private local storage, and inspect downloaded content before integrating it into a project. <br>
Risk: Missing durable buyer state can cause duplicate purchases or weak license and audit tracking. <br>
Mitigation: Maintain the local purchase ledger described in references/purchase-store.md and check it before executing a new purchase. <br>


## Reference(s): <br>
- [Buyer purchase persistence notes](references/purchase-store.md) <br>
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage) <br>
- [SpawnXchange machine manifest](https://spawnxchange.com/api/v1/skills) <br>
- [ClawHub skill page](https://clawhub.ai/spawnxchange/spawnxchange-direct-buying) <br>
- [Source homepage](https://github.com/avlk/spawnxchange-skills) <br>
- [Hermes raw source](https://raw.githubusercontent.com/avlk/spawnxchange-skills/main/skills/spawnxchange-direct-buying/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python example code, requirements, and JSON purchase-record template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote-only by default; execute mode can authorize a wallet-backed USDC purchase.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
