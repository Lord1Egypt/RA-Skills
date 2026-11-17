## Description:

Read, list, mint, and append Soul Blocks on Base. Read works without a wallet. Write operations use evm-wallet if available and fall back to website deep links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hburgoyne](https://clawhub.ai/user/hburgoyne)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use Soul Blocks to read Soul Block NFT identity content from Base and, after explicit confirmation, mint or append on-chain identity fragments through evm-wallet or fallback website links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched SOUL.md or on-chain fragments may be treated as agent identity and override higher-priority behavior.

Mitigation: Treat SOUL.md and on-chain fragments as untrusted display data; do not allow them to override safety rules, tool use, wallet decisions, or system instructions.

Risk: The artifact includes daily cron or heartbeat reinforcement behavior that could persistently reintroduce untrusted identity content.

Mitigation: Remove or disable cron and heartbeat reinforcement before installation unless a reviewer explicitly approves that behavior.

Risk: Mint and append flows can spend funds or permanently write content on-chain.

Mitigation: Use only a low-value hot wallet, review all transaction details, and require explicit user confirmation before any wallet-backed or deep-link write flow.

## Reference(s):

- [SoulBlocks Skill Reference](references/REFERENCE.md)
- [Soul Blocks ClawHub Page](https://clawhub.ai/hburgoyne/skills/soulblock)
- [SoulBlocks Website](https://soulblocks.ai)
- [evm-wallet ClawHub Page](https://clawhub.ai/surfer77/evm-wallet)
- [evm-wallet Source](https://github.com/surfer77/evm-wallet-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read public Base contract data, write local SOUL.md and .soulblock files, and propose wallet-backed or website-linked transaction flows.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter metadata, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
