## Description:

Helps agents test x402 commerce, verify signed evidence, inspect endpoints, diagnose payments, and use SCVD's store and local cost-tracking tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seancrecord](https://clawhub.ai/user/seancrecord)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to run free receipt and endpoint checks, investigate commerce failures, compare dated observations, and navigate optional paid SCVD services with user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live purchases can spend real USDC.

Mitigation: Require the user's explicit choice of item, network and spending limit before signing; never request wallet secrets.

Risk: Posting entries, reserving work or submitting private endpoint URLs can disclose information or act on the user's behalf.

Mitigation: Obtain the user's decision before each action; keep confidential data out of memory anchors and request fields.

Risk: A passing free check or valid signature does not establish payment settlement, delivery or authorization to spend.

Mitigation: Report the observation's scope, date and missing checks; recover an uncertain purchase before authorizing another payment.

## Reference(s):

- [SCVD website](https://scvd.store)
- [Verification guide](references/verification.md)
- [Endpoint inspection guide](references/inspection.md)
- [Purchase and recovery guide](references/purchases.md)
- [Everyday agent tasks](references/agent-tasks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Plain text or Markdown with API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observation dates, evidence scope and unverified checks.]

## Skill Version(s):

3.19.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
