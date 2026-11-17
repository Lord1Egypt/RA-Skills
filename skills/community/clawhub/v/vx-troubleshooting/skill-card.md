## Description:

Provides guidance for diagnosing and resolving vx installation, version, PATH, runtime, and configuration problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support agents use this guide to diagnose vx failures and choose appropriate troubleshooting steps for local environments and CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installation commands may execute unreviewed code.

Mitigation: Require explicit approval and inspect downloaded scripts before running them.

Risk: Elevated installation commands can make unwanted system changes.

Mitigation: Do not run sudo commands automatically; review permissions and prefer user-level installation.

Risk: A complete vx reset can delete local configuration and installed tools.

Mitigation: Back up ~/.vx and require explicit approval before deleting it.

## Reference(s):

- [ClawHub vx-troubleshooting release](https://clawhub.ai/loonghao/skills/vx-troubleshooting)
- [vx documentation](https://github.com/vx-org/vx#readme)
- [Managed command shim guide](https://github.com/vx-org/vx/blob/main/docs/guide/managed-command-shims.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Troubleshooting steps require human review before executing high-impact commands.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
