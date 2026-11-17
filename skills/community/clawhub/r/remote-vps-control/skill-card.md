## Description:

Use when onboarding, connecting to, inspecting, maintaining, rotating access for, or revoking access to another VPS over SSH from an agent-controlled host. Enforces per-host keys, source-IP restrictions, out-of-band host-key verification, staged lockout-safe hardening, least privilege, and verified remote operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xinian5216](https://clawhub.ai/user/xinian5216)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to securely connect to and maintain authorized VPS hosts over SSH, including onboarding, access rotation, revocation, and troubleshooting. It guides staged changes with host identity checks, least privilege, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An exposed controller private key or overly broad sudo access could enable unauthorized server changes.

Mitigation: Keep private keys on the controller with restricted permissions, use a separate key per server, and grant only the sudo commands required.

Risk: Accepting an unverified SSH host key or tightening access before a new path works could expose a connection or lock out an operator.

Mitigation: Compare the Ed25519 host fingerprint through the provider console, retain the recovery path, and confirm a separate new connection before removing old access.

Risk: SSH access remains active until its credentials and network allowances are revoked; controller IP discovery sends its public IP to ipify.

Mitigation: Revoke the public key on the server when access is no longer needed, then remove related firewall rules and local credentials; account for the disclosed IP lookup during setup.

## Reference(s):

- [Remote VPS Control on ClawHub](https://clawhub.ai/xinian5216/skills/remote-vps-control)
- [Remote VPS control setup guide](references/remote-vps-control-setup.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and examples use placeholders that must be replaced with values confirmed for the authorized target host.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
