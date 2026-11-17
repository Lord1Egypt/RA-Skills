## Description:

Create an anonymous Starknet wallet via Typhoon and interact with Starknet contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esdras-sena](https://clawhub.ai/user/esdras-sena)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and external agents use this skill to create or load a Typhoon-backed Starknet account, discover ABIs, read and invoke contracts, run swaps, and set event or conditional watchers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a local Starknet signing key and submit irreversible on-chain transactions.

Mitigation: Require explicit review of every transaction before broadcast and use accounts funded only for the intended operation.

Risk: Typhoon note secrets may be exposed if passed as command-line arguments or retained in shell history.

Mitigation: Avoid command-line note secrets; provide sensitive note material through safer input handling and clear command history after setup.

Risk: Event or conditional watchers can create persistent cron jobs under ~/.openclaw/cron.

Mitigation: Review and remove created watcher files and crontab entries when the watch task is complete.

## Reference(s):

- [Typhoon Starknet Account on ClawHub](https://clawhub.ai/esdras-sena/skills/typhoon-starknet-account)
- [ArgentX Account Class Hashes](references/argentx-class-hashes.md)
- [Argent Contracts Starknet](https://github.com/argentlabs/argent-contracts-starknet)
- [Starkscan ArgentX Class Explorer](https://starkscan.co/class/0x036078334509b514626504edc9fb252328d1a240e4e948bef8d0c08dff45927f)
- [Typhoon Finance App](https://www.typhoon-finance.com/app)
- [Loot Survivor Contracts](https://docs.provable.games/lootsurvivor/contracts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command inputs or outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction authorization prompts and JSON results from helper scripts.]

## Skill Version(s):

0.3.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
