## Description:

Teneo Protocol CLI helps agents discover and query Teneo Protocol AI agents, manage rooms, and handle x402 USDC micropayments across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[np793](https://clawhub.ai/user/np793)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to install and operate a Teneo Protocol CLI for agent discovery, room management, direct agent commands, quotes, payment confirmation, wallet checks, and USDC withdrawals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote agent flows can request broadly scoped wallet spending without strong confirmation or limits.

Mitigation: Use a dedicated low-balance wallet, prefer manual quote and confirm payment flows, and constrain or remove the generic transaction signer before installation.

Risk: Using TENEO_PRIVATE_KEY with a real wallet could expose funds to unintended agent-initiated payments.

Mitigation: Do not set TENEO_PRIVATE_KEY to a real wallet; use only an isolated bot wallet funded with the minimum USDC needed for the task.

Risk: Withdrawal ownership is based on the first inbound transfer, which may not be sufficient proof of intended ownership.

Mitigation: Fund the wallet with a small controlled test transfer and verify withdrawal behavior before adding meaningful funds.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/np793/skills/teneoprotocolcli)
- [Teneo Protocol](https://teneo.pro)
- [Teneo Protocol SDK on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK](https://github.com/AIMadeScripts/teneo-agent-sdk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JavaScript code, and JSON CLI responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides setup and operation of a local CLI that connects to Teneo Protocol services and signs x402 payments from a dedicated wallet.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence, created 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
