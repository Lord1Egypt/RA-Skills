## Description:

Helps developers discover received public libraries and run bounded, caller-supplied checks for integration repair, tool input compatibility, and task distribution without sending payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[epistemedeus](https://clawhub.ai/user/epistemedeus)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to discover and run received library contracts or their own task inputs, check compatibility and repair classifications, and share bounded task referrals. A successful check does not by itself establish real-world usefulness or payment eligibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetched third-party packages and their CLIs execute in a caller-chosen directory.

Mitigation: Review pinned sources, use a disposable work directory, and run only if Node, tar, npm, and the listed public downloads are acceptable.

Risk: Caller-mode requests can contain sensitive task inputs or authorize unwanted local work.

Mitigation: Review requests before execution and keep credentials out of request files.

Risk: A matched description or successful contract replay can be mistaken for a completed real-world task.

Mitigation: Verify the caller's actual output and record usefulness separately; do not interpret a classification as a payment demand.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/epistemedeus/skills/received-useful-work)
- [Skill documentation](https://neomorphic.io/.well-known/skills/received-useful-work/SKILL.md)
- [Caller input contract](references/caller-input-contract.json)
- [Task distribution input contract](references/taREDACTED-SECRET.json)
- [Library delivery pins](references/library-delivery.json)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands]

**Output Format:** [JSON decisions and event logs, with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decisions distinguish completed checks from missing inputs, refusals, and unverified usefulness; no payment is sent.]

## Skill Version(s):

0.1.1 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
