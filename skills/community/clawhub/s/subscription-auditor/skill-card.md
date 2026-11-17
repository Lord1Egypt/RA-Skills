## Description:

Tracks a local subscription ledger, estimates monthly and yearly spending, and flags upcoming or past-due renewals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals use this skill to manually record subscription costs and renewal dates, review spending totals, and check which renewals need attention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Subscription names, costs, notes, and renewal dates are stored in local files.

Mitigation: Use this skill only on a machine where local subscription records can be kept private.

Risk: Removing a subscription deletes its entry immediately without confirmation.

Mitigation: Check the entry identifier and back up the ledger before removing records you may need later.

## Reference(s):

- [Subscription Auditor on ClawHub](https://clawhub.ai/paradoxfuzzle/skills/subscription-auditor)
- [Publisher profile](https://clawhub.ai/user/paradoxfuzzle)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain text or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes subscription lists, estimated spending totals, and renewal reminders; records remain in a local ledger.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
