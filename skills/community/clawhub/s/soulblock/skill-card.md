## Description: <br>
Read, list, mint, and append Soul Blocks on Base; read operations work without a wallet, while write operations use evm-wallet when available and fall back to website deep links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hburgoyne](https://clawhub.ai/user/hburgoyne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to read Soul Block NFT identities on Base, manage local SOUL.md snapshots, and prepare or submit mint and append transactions through an agent-connected wallet or website fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Loaded on-chain SOUL.md content can influence the agent's identity, voice, and behavior. <br>
Mitigation: Inspect loaded SOUL.md content before allowing it to shape agent behavior, and use the skill only when agent-persona embodiment is deliberate. <br>
Risk: Minting and appending fragments use wallet-connected on-chain transactions that are permanent. <br>
Mitigation: Use only a low-value hot wallet, show the exact transaction content and cost, and proceed only after explicit confirmation. <br>
Risk: Recurring reinforcement through cron or heartbeat behavior can persist identity instructions beyond the initial load. <br>
Mitigation: Enable reinforcement only when desired, keep it visible to the user, and remove scheduled reminders when embodiment is no longer wanted. <br>


## Reference(s): <br>
- [SoulBlocks Skill Reference](references/REFERENCE.md) <br>
- [Soul Blocks ClawHub Page](https://clawhub.ai/hburgoyne/soulblock) <br>
- [SoulBlocks Website](https://soulblocks.ai) <br>
- [evm-wallet ClawHub Page](https://clawhub.ai/surfer77/evm-wallet) <br>
- [evm-wallet Source](https://github.com/surfer77/evm-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, local file updates, transaction parameters, and website links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create timestamped SOUL.md backups and .soulblock configuration; on-chain writes are append-only and require explicit user confirmation.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter metadata and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
