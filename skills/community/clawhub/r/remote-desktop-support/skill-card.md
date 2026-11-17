## Description:

Linux/Fedora-GNOME-first, early but safety-tested skill for short-lived browser-based remote desktop support links using local-only VNC/Guacamole and outbound tunnels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommyclawd](https://clawhub.ai/user/tommyclawd)

### License/Terms of Use:

MIT-0

## Use Case:

External support users and operators use this skill to open temporary browser-based access to a Linux/Fedora GNOME live desktop for troubleshooting. It is designed for supervised sessions with short TTLs, view-only default access, and explicit cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a live desktop session through a temporary public tunnel.

Mitigation: Run preflight and status before opening access, use view-only unless control is explicitly needed, supervise the session, and treat one-click URLs as password-equivalent.

Risk: A desktop backend, tunnel, credential, or container could remain active after support ends.

Mitigation: Use short TTLs, run close when the session ends, and manually verify status reports closed with no remaining skill-owned containers or listeners.

Risk: Unlocking the current session through the skill weakens local desktop protections.

Mitigation: Avoid unlock-current-session unless explicitly approved for the support task and the operator accepts the risk.

## Reference(s):

- [Remote Desktop Support Security Model](references/security-model.md)
- [ClawHub skill page](https://clawhub.ai/tommyclawd/skills/remote-desktop-support)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON command output from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux/Fedora GNOME, python3, and podman; open sessions are intended to be time-limited and view-only by default.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
