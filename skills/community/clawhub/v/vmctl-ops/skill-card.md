## Description:

Use when vmctl is already installed and the agent must immediately run safe post-install checks and first lifecycle actions without guessing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bashrusakh](https://clawhub.ai/user/bashrusakh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill after vmctl installation to run health checks, perform a test VM lifecycle smoke run, clean up test artifacts, recover state drift when needed, and report concise operational status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run destructive cleanup and recovery operations through existing vmctl credentials.

Mitigation: Narrow activation to explicit vmctl smoke-test requests and require operator approval before `delete --force`, `purge`, or `recover --apply`.

Risk: Incorrect purge or recovery targets could affect VM state beyond the intended smoke-test resource.

Mitigation: Use test-only VM names, verify the deleted tombstone name before purge, and confirm recovery targets exactly match the intended test VM.

Risk: Existing ESXi/helper credentials may permit more than the minimum lifecycle actions needed for validation.

Mitigation: Limit credential scope to the vmctl helper workflow and test VM lifecycle operations: diagnostics, create/status, cleanup, and reconciliation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bashrusakh/skills/vmctl-ops)
- [ClawHub publisher profile](https://clawhub.ai/user/bashrusakh)
- [vmctl repository](https://github.com/bashrusakh/vmctl)
- [vmctl latest release](https://github.com/bashrusakh/vmctl/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status summaries with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise operator-facing pass/fail status, VM name, cleanup result, and residual recovery action count.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
