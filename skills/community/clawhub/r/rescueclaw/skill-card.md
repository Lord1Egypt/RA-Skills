## Description:

Provides automatic checkpoint creation and rollback to help recover from failures during risky operations like configuration changes or updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harman314](https://clawhub.ai/user/harman314)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use RescueClaw to create checkpoints before risky operations such as configuration changes, skill installation, or gateway updates, then clear them after success so rollback remains available if the operation leaves the agent unresponsive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation automatically places an unverified external native executable in a command path.

Mitigation: Install only from a trusted publisher and prefer a release that bundles the executable or verifies it with pinned checksums or signatures.

Risk: Rollback behavior can affect long-running operations if trigger and disable controls are unclear.

Mitigation: Avoid using checkpoints around long-running operations until rollback windows, trigger conditions, and disable controls are understood.

## Reference(s):

- [RescueClaw ClawHub page](https://clawhub.ai/harman314/skills/rescueclaw)
- [RescueClaw GitHub Releases](https://github.com/harman314/rescueclaw/releases)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript examples and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke the RescueClaw CLI for status checks and writes user-local checkpoint request data when used.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
