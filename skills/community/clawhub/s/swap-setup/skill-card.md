## Description:

Helps users add swap to a Linux VPS through chat without entering terminal commands, using a temporary SSH key for access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinhbuiii](https://clawhub.ai/user/thinhbuiii)

### License/Terms of Use:

MIT-0

## Use Case:

VPS owners who do not use a terminal can authorize an agent to create and enable a swap file, check that it persists after reboot, and revoke temporary access afterward.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary privileged SSH access could permit unauthorized changes to the VPS.

Mitigation: Confirm the VPS owner's authorization and consent, keep the private key confidential, and revoke the temporary key after the task.

Risk: An invalid swap configuration could disrupt startup after a reboot.

Mitigation: Back up and validate the swap configuration before rebooting, and restore the backup if validation fails.

## Reference(s):

- [Swap Setup release](https://clawhub.ai/thinhbuiii/skills/swap-setup)
- [Usage guide](artifact/references/usage.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports swap status, configuration validation, and key-revocation steps.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
