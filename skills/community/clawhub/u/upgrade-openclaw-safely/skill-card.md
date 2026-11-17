## Description:

Assess OpenClaw releases, upgrade an installation, or recover a failed update using verified backups, official durable handoff and runtime evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skillmelody](https://clawhub.ai/user/skillmelody)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators and developers use this skill to assess a release, carry out an authorized upgrade, or recover from an interrupted update. It guides target selection, recovery preparation, runtime checks, and reporting of verified results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Upgrade work can interrupt services or leave the installation only partially verified.

Mitigation: Confirm the exact target, interruption plan, recovery limits, permitted checks, and stability window; report incomplete critical verification clearly.

Risk: Recovery backups can contain credentials and other sensitive local state.

Mitigation: Keep backups local and protected, verify their scope and integrity, and follow the agreed retention policy.

## Reference(s):

- [Native updater and target selection](references/native-updater.md)
- [Migration, backup coverage, and runtime](references/migration-and-runtime.md)
- [Verification and retention](references/verification-and-retention.md)
- [Transaction contract](references/transaction-contract.md)
- [Recovery contract](references/recovery-contract.md)
- [OpenClaw update CLI documentation](https://docs.openclaw.ai/cli/update)
- [OpenClaw updating guide](https://docs.openclaw.ai/install/updating)
- [OpenClaw backup CLI documentation](https://docs.openclaw.ai/cli/backup)
- [ClawHub release page](https://clawhub.ai/skillmelody/skills/upgrade-openclaw-safely)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown operational report with verification findings and commands where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Context-dependent upgrade or recovery status, evidence, and remaining actions]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
