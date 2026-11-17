## Description:

Control and monitor Ring doorbells and cameras by listing devices, capturing snapshots, and viewing recent events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlmoment](https://clawhub.ai/user/zlmoment)

### License/Terms of Use:

MIT-0

## Use Case:

External users with Ring devices use this skill to authenticate locally, check doorbell and camera status, capture snapshots, and review recent motion or doorbell events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Ring account credentials and reusable Ring tokens for home-surveillance access.

Mitigation: Use it only from a trusted local terminal, protect or delete saved tokens when no longer needed, and prefer restrictive permissions on credential files.

Risk: Camera snapshots and derived media can contain sensitive household imagery and are saved locally.

Mitigation: Store media only on trusted devices, review access to ~/.openclaw/media/ring/, and delete snapshots when they are no longer needed.

Risk: The security guidance notes that dependency pinning and terminal credential handling could be hardened.

Mitigation: Pin dependencies for deployment, review updates before use, and prefer an authentication flow that does not visibly echo or persist password and 2FA input.

## Reference(s):

- [Ring Doorbell & Camera on ClawHub](https://clawhub.ai/zlmoment/skills/ring-doorbell)
- [python-ring-doorbell library](https://github.com/tchellomello/python-ring-doorbell)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime commands return JSON status, event data, or saved snapshot file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Snapshots are saved under ~/.openclaw/media/ring/ when capture succeeds.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
