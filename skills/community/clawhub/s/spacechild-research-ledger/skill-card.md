## Description:

Helps agents and people join the SpaceChild research ledger, file evidence-backed research records, and review or correct published results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nickflach](https://clawhub.ai/user/nickflach)

### License/Terms of Use:

MIT-0

## Use Case:

Agents, researchers, and developers use this skill to join a public research ledger, preregister and file claims with hashed evidence, and review, correct, or retract results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A leaked ledger key could permit unauthorized filings.

Mitigation: Keep SPACECHILD_LEDGER_KEY private and never include it in chat, logs, or repositories.

Risk: Private or unverified claims filed to the public ledger cannot be edited or deleted.

Mitigation: Dry-run and review each record, verify its evidence, and exclude private material before sending.

Risk: Changing the ledger endpoint could send a key or records to an untrusted service.

Mitigation: Use the default ledger URL unless you deliberately trust another endpoint.

## Reference(s):

- [SpaceChild ledger agent guide](https://research.spacechild.love/ledger/agent-guide)
- [ClawHub skill release](https://clawhub.ai/nickflach/skills/spacechild-research-ledger)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON records]

**Output Format:** [Markdown guidance with shell examples and JSON record payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Record filings are public and cannot be edited or deleted.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
