## Description:

One-step full-stack installer for OpenClaw WebChat voice input with local speech-to-text, orchestrating a local STT backend, HTTPS/WSS proxy, and voice UI controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neldar](https://clawhub.ai/user/neldar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install, verify, and operate a local voice input stack for WebChat. It is intended for agents helping with user-level setup, status checks, and configuration guidance for local speech-to-text, HTTPS/WSS proxying, and mic UI controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs mutable downstream installer scripts with the user's privileges.

Mitigation: Review and pin the three downstream skills before use, then run checksum verification before deployment.

Risk: The checksum workflow can be mistaken for proof of a safe download.

Mitigation: Treat rehash.sh only as a local trusted-baseline recorder after manual review, not as independent safety validation.

Risk: Deployment can install user-level services and modify OpenClaw gateway or UI behavior.

Mitigation: Review the planned local changes, run status checks after deployment, and use the documented uninstall path if changes are not acceptable.

## Reference(s):

- [Architecture](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include local service deployment, checksum verification, status checks, and uninstall steps.]

## Skill Version(s):

0.4.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
