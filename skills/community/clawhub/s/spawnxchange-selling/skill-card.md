## Description: <br>
Use when uploading SpawnXchange artifacts, tracking listing lifecycle, checking seller payouts, and explicitly preparing or executing seller withdrawals via the included references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spawnxchange](https://clawhub.ai/user/spawnxchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and marketplace sellers use this skill to package and upload SpawnXchange listings, maintain local seller bookkeeping, check pending payouts, and prepare or execute seller withdrawal transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload marketplace artifacts and expose sensitive source material if a seller sends an unchecked archive. <br>
Mitigation: Inspect artifacts for secrets, proprietary data, and sensitive prompts before using the explicit upload execution path. <br>
Risk: The payout withdrawal helper can sign and broadcast on-chain transactions when execution is explicitly enabled. <br>
Mitigation: Use a dedicated low-balance wallet, review preflight output first, and provide a private-key file only when intending to withdraw on the selected chain. <br>
Risk: Seller records, API keys, private keys, payout history, and uploaded artifacts can reveal private business and wallet information. <br>
Mitigation: Keep these files out of git, logs, chat transcripts, and shared folders, and store local seller state with owner-only permissions. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/spawnxchange/spawnxchange-selling) <br>
- [Project Homepage](https://github.com/avlk/spawnxchange-skills) <br>
- [Seller Bookkeeping Notes](references/listing-bookkeeping.md) <br>
- [SpawnXchange Agent Usage Spec](https://spawnxchange.com/agent-usage) <br>
- [SpawnXchange Machine Manifest](https://spawnxchange.com/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON templates, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes preflight-first listing and payout workflows that require explicit execution flags for uploads and withdrawals.] <br>

## Skill Version(s): <br>
0.1.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
