## Description:

KasmVNC-based virtual desktop for headless Linux with AI-first automation and human handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxin15435](https://clawhub.ai/user/zhangxin15435)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to start and operate a headless Linux KasmVNC desktop when browser automation needs short human handoff for captcha, risk-control, MFA, login approval, or mobile and desktop rendering checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a remote desktop service over the network, including an optional public 0.0.0.0 binding.

Mitigation: Prefer the default 127.0.0.1 binding with an SSH tunnel, and only use public binding behind firewall, VPN, and trusted TLS controls.

Risk: Screenshots and browser profiles can include sensitive user data.

Mitigation: Avoid running the desktop around sensitive screens unless screenshot capture and profile persistence are acceptable for the workflow.

Risk: Installation downloads and installs a KasmVNC package with sudo privileges.

Mitigation: Review or pin the KasmVNC package source before allowing privileged installation.

Risk: The security assessment flags unsafe install, state-loading, and public-exposure choices.

Mitigation: Treat this release as requiring maintainer review and fixes for shell-safe state storage and safer privilege handling before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxin15435/skills/virtual-remote-desktop)
- [KasmVNC releases API](https://api.github.com/repos/kasmtech/KasmVNC/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and runtime text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Screenshots may be returned as base64-encoded PNG data by the action scripts.]

## Skill Version(s):

1.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
