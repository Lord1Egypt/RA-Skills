## Description:

Installs and manages an OpenClaw Weixin connection through admin chat commands, including QR refresh, status checks, and pairing cancellation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donotwannatry](https://clawhub.ai/user/donotwannatry)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators use this skill in private admin chats to install or enable the Weixin channel plugin, start pairing, refresh or inspect QR login state, and cancel pairing tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow performs high-impact local actions, including OpenClaw plugin state changes and a gateway restart after successful pairing.

Mitigation: Install and run it only on a controlled admin host where gateway interruptions and plugin changes are expected.

Risk: The workflow writes QR and login artifacts that may expose pairing state on shared systems.

Mitigation: Use it only where file permissions and host access are controlled, and avoid shared systems until artifact handling is hardened.

Risk: The scanner guidance calls out implementation concerns around file permissions, PID validation, and restart scheduling.

Mitigation: Review those areas before deployment and validate the Weixin plugin version before use.

## Reference(s):

- [Weixin Plugin Installer on ClawHub](https://clawhub.ai/donotwannatry/skills/weixin-plugin-installer)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [JSON script results interpreted as concise chat responses, with optional MEDIA path output or Markdown QR fallback.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, python3, openclaw, and an OpenClaw host where the administrator can install plugins and manage gateway restarts.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
