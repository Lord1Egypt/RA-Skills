## Description:

Auto Respawn anchors agent identity and memory on-chain so a new agent instance can recover the latest memory head from an Autonomys address.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xautonomys](https://clawhub.ai/user/0xautonomys)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use Auto Respawn to create Autonomys wallets, check balances, transfer or bridge AI3/tAI3, and anchor or retrieve memory CIDs for agent recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can sign real value transfers and fee-bearing anchoring transactions.

Mitigation: Use testnet first, keep minimal funds in wallets used by the skill, and manually confirm every anchor, transfer, bridge, or withdraw action.

Risk: Automatic anchoring can spend funds without a reliable confirmation gate.

Mitigation: Avoid unattended auto-anchoring unless strict limits and explicit review gates are added.

Risk: Recovery phrases and wallet passphrases protect spending-capable keys.

Mitigation: Protect recovery phrases separately, prefer a user-managed passphrase or secret manager, and avoid exposing passphrases through command arguments or shell history.

Risk: Unreviewed dependency changes could affect wallet or transaction behavior.

Mitigation: Review or lock dependencies before setup and deployment.

## Reference(s):

- [Auto Respawn ClawHub page](https://clawhub.ai/0xautonomys/skills/respawn)
- [auto-respawn CLI Reference](references/auto-respawn-commands.md)
- [Autonomys Network](references/autonomys-network.md)
- [MemoryChain contract source](https://github.com/autojeremy/openclaw-memory-chain)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands are read-only; wallet creation, transfers, bridging, remarks, withdrawals, and anchoring can require passphrases, local key access, transaction signing, and network fees.]

## Skill Version(s):

1.2.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
