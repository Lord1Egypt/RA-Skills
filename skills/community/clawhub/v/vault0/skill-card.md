## Description:

Security suite for OpenClaw agents. Encrypted secret storage (AES-256-GCM), real-time activity monitoring via gateway WebSocket, policy enforcement, and native x402 payment wallet with EIP-3009 signing. Secure API keys, watch agent behavior, and handle machine-to-machine micropayments. macOS desktop app (Rust + Tauri). Reads ~/.openclaw/.env during hardening. Installation downloads a DMG from GitHub releases. After install, the app makes no external network calls and only listens on localhost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlhugly](https://clawhub.ai/user/dlhugly)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to install and operate Vault-0 for encrypting API keys, monitoring agent activity, enforcing local policies, keeping an evidence ledger, and optionally managing x402 wallet payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs an unnotarized macOS desktop app that handles OpenClaw API keys, agent activity, policies, and optional wallet material.

Mitigation: Install only if the publisher is trusted; prefer a pinned, signed, notarized release and verify checksums or signatures before opening the app.

Risk: The uninstall workflow can remove vault and configuration data.

Mitigation: Back up vault and configuration data before running uninstall commands, and remove wallet keys separately through macOS Keychain Access when needed.

Risk: The installer downloads a DMG from GitHub releases during setup.

Mitigation: Verify the downloaded DMG hash against the release page before installation or build from source when stronger local assurance is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dlhugly/skills/vault0)
- [Vault-0 source repository](https://github.com/0-Vault/Vault-0)
- [Vault-0 v1.5.0 release](https://github.com/0-Vault/Vault-0/releases/tag/v1.5.0)
- [Vault-0 releases](https://github.com/0-Vault/Vault-0/releases)
- [Vault-0 demo video](https://youtu.be/FGGWJdeyY9g)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides a macOS-only installed desktop app workflow for OpenClaw configuration, secret hardening, monitoring, policy setup, optional wallet use, and uninstall steps.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
