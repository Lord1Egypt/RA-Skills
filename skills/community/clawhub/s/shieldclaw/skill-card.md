## Description: <br>
Security suite for OpenClaw. Provides security scanning, real-time protection, audit logging, and sensitive data encryption. Use this skill when users need security-related operations, threat detection, or data protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jzming9](https://clawhub.ai/user/jzming9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use ShieldClaw to scan skills for security issues, enable file and operation protection, encrypt sensitive data, and review audit logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release requests broad storage, network, and filesystem permissions for security-control behavior. <br>
Mitigation: Review the referenced @shieldclaw dependencies and confirm how OpenClaw enforces Guard hooks before enabling protection. <br>
Risk: The security evidence says key behavior is under-scoped or delegated to unreviewed external packages. <br>
Mitigation: Install only after reviewing those dependencies and keep a clear disable path for protection features. <br>
Risk: Vault and audit features can handle sensitive data, local logs, and keychain-managed encryption keys. <br>
Mitigation: Avoid storing high-value secrets until the vault implementation is reviewed, verify logging and retention settings, and confirm local data can be deleted. <br>
Risk: Default protected paths and strictness may not match the user's environment. <br>
Mitigation: Narrow protected paths and tune Guard settings before relying on runtime protection. <br>


## Reference(s): <br>
- [ClawHub ShieldClaw listing](https://clawhub.ai/jzming9/shieldclaw) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jzming9) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and natural-language guidance with configuration snippets and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local security scans, guard configuration, audit reports, and vault usage; runtime behavior depends on OpenClaw integration and ShieldClaw packages.] <br>

## Skill Version(s): <br>
1.0.4 (source: server evidence, artifact clawhub.json, README.md, and CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
