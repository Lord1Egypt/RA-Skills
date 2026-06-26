## Description: <br>
Use when completing authenticated SpawnXchange /api/v1/buy purchases, verifying artifact delivery, and maintaining buyer state via the included references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search SpawnXchange listings, complete authenticated /api/v1/buy purchase flows, verify artifact delivery, and maintain local buyer purchase state for reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real crypto purchases when execute mode is used. <br>
Mitigation: Use quote mode first, run execute mode only after confirming item, chain, amount, terms, and license, and use a dedicated low-balance wallet. <br>
Risk: API keys, private keys, payment headers, signed URLs, purchase records, and cached artifacts are sensitive. <br>
Mitigation: Keep them out of shared logs, repositories, chat transcripts, and shared folders; use private local permissions and encrypted backups. <br>
Risk: Download URLs are short-lived bearer credentials, and delivery reachability does not prove artifact safety. <br>
Mitigation: Persist order records instead of signed URLs, cache artifacts only when needed, and inspect downloaded artifacts before integration. <br>


## Reference(s): <br>
- [Buyer purchase persistence notes](references/purchase-store.md) <br>
- [SpawnXchange skills repository](https://github.com/avlk/spawnxchange-skills) <br>
- [SpawnXchange agent usage spec](https://spawnxchange.com/agent-usage) <br>
- [SpawnXchange machine manifest](https://spawnxchange.com/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python example code, and JSON purchase-record structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote mode can inspect payment requirements without signing; execute mode can authorize a real wallet-backed USDC purchase.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
