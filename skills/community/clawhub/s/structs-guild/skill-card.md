## Description: <br>
Manages guild operations in Structs. Covers creation, membership, settings, and Central Bank token operations. Use when creating a guild, joining or leaving a guild, managing guild settings, minting or redeeming guild tokens, managing Central Bank collateral, or coordinating guild membership. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs players and guild operators use this skill to plan and execute guild creation, membership, rank, permission, identity, and Central Bank token operations with the structsd CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill helps prepare wallet-signed on-chain guild actions, including rank, ownership, permission, and token operations that may be permanent or hard to reverse. <br>
Mitigation: Before approving a transaction, confirm the signer, chain, entity IDs, permission bits, rank ranges, token amounts, collateral ratio, and reversibility. <br>
Risk: Using non-interactive approval flags can suppress CLI confirmation prompts for sensitive transactions. <br>
Mitigation: Use interactive TX_FLAGS by default and reserve prompt-suppressing approval flags for commander-approved actions. <br>
Risk: Broad rank-based permissions can grant operational authority to many guild members at once. <br>
Mitigation: Prefer narrow rank ranges or per-player grants, then verify permissions with guild-rank permission queries after changes. <br>


## Reference(s): <br>
- [Structs Guild on ClawHub](https://clawhub.ai/abstrct/structs-guild) <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [Structs guild banking](https://structs.ai/knowledge/economy/guild-banking) <br>
- [Structs permissions](https://structs.ai/knowledge/mechanics/permissions) <br>
- [Structs UGC moderation](https://structs.ai/knowledge/mechanics/ugc-moderation) <br>
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline structsd CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.] <br>

## Skill Version(s): <br>
1.3.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
