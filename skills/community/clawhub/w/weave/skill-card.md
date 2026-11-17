## Description:

Create crypto invoices and stablecoin invoices, generate payment quotes, and monitor invoice payment status with the Weave CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aryanj-nyc](https://clawhub.ai/user/aryanj-nyc)

### License/Terms of Use:

AGPL-3.0-or-later

## Use Case:

Developers and operations teams use this skill to create Weave crypto or stablecoin invoices, quote payer instructions, and track settlement status through JSON-first CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment workflows can be affected by unpinned third-party CLI or helper-tool installs.

Mitigation: Use pinned, reviewed versions of the Weave CLI and helper tools before using the skill in wallet, payment, or release environments.

Risk: Incorrect wallet, refund, or deposit addresses can cause payment loss or misrouting.

Mitigation: Manually verify wallet, refund, and deposit addresses before acting on generated payment instructions.

Risk: Publishing or release scripts may run with credentials available in the local environment.

Mitigation: Run helper scripts only from a clean environment with minimal credentials.

## Reference(s):

- [Weave homepage](https://www.weavecash.com)
- [ClawHub skill listing](https://clawhub.ai/aryanj-nyc/skills/weave)
- [Weave CLI Contract Snapshot](references/cli-contract.md)
- [Weave Skill Scenarios](references/scenarios.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers machine-readable JSON output from the Weave CLI and explicit handling of non-zero exits.]

## Skill Version(s):

0.1.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
