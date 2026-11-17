## Description:

Creates and reviews SN94 BitSota competition proposals and replayable task repository skeletons for measurable agent research tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alveuslabs](https://clawhub.ai/user/alveuslabs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to turn measurable research competition ideas into SN94 BitSota proposals, replay contracts, launch checklists, and starter task repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated validator and benchmark code may follow miner-controlled symlinks outside the intended submission folder.

Mitigation: Before real validation use, reject symlinks, enforce resolved-path containment under submission/, stream file reads with size limits, and run benchmarks in a sandbox without wallets, API tokens, host secrets, or unnecessary filesystem mounts.

Risk: Implicit invocation could create task repository scaffolds during broad research or planning requests.

Mitigation: Narrow or disable implicit invocation in environments where general research prompts should not trigger repository creation.

## Reference(s):

- [SN94 Replay Contract](artifact/references/replay-contract.md)
- [SN94 Task Repo Spec](artifact/references/task-repo-spec.md)
- [Marketplace Packaging](artifact/references/marketplace-packaging.md)
- [SN94 BitSota competition proposal issue template](https://github.com/AlveusLabs/SN94-BitSota/issues/new?template=competition_proposal.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional generated repository files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold a starter task repository for SN94 replay validation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
