## Description:

Installs and configures a Trojan proxy client on Linux, including proxychains4 setup and Chrome APT source configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[salebender249-del](https://clawhub.ai/user/salebender249-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to prepare an Ubuntu or Debian Linux host for Trojan proxy client usage, including package installation, local proxy routing through proxychains4, and browser setup guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer performs root-level system changes, including package installation, file writes under system directories, and service setup.

Mitigation: Review install.sh before running it and back up existing Chrome APT and proxychains configuration.

Risk: The Trojan binary download is not pinned to a checksum or verified signature in the artifact.

Mitigation: Verify the downloaded Trojan release with a pinned checksum or signature before installation.

Risk: The documented default proxy configuration exposes the local listener on 0.0.0.0 and disables TLS certificate and hostname verification.

Mitigation: Bind the proxy listener to 127.0.0.1 unless LAN exposure is intentional, and enable TLS certificate and hostname verification where possible.

Risk: Enabling the Trojan systemd service can make proxy behavior persistent across reboots.

Mitigation: Inspect the service unit and its privileges before running systemctl enable.

## Reference(s):

- [Trojan GitHub](https://github.com/trojan-gfw/trojan)
- [Proxychains-ng](https://github.com/rofl0r/proxychains-ng)
- [Google Chrome](https://www.google.com/chrome/)
- [ClawHub Skill Page](https://clawhub.ai/salebender249-del/skills/trojan-setup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privileged Linux installation and service-management commands that require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
