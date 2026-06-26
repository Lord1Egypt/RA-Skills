## Description: <br>
Manage and secure local high-privilege storage serving workflows for creating, starting, stopping, or hardening a full-drive file server and related operational controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manlight87](https://clawhub.ai/user/manlight87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run a local storage manager with token authentication, loopback binding, root path controls, and file listing, reading, or download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local file exposure can make sensitive files browseable or downloadable if the configured root is too wide. <br>
Mitigation: Set GOD_MODE_ROOT to a narrow dedicated folder, keep the host bound to 127.0.0.1, and stop the server when finished. <br>
Risk: Tokens in URLs may be shared or logged unintentionally. <br>
Mitigation: Prefer header-based authentication, avoid sharing UI URLs, and rotate GOD_MODE_TOKEN if it appears in logs or messages. <br>
Risk: Disabling token authentication removes the primary access control for the local file server. <br>
Mitigation: Keep GOD_MODE_TOKEN_REQUIRED enabled and use a strong token for normal operation. <br>


## Reference(s): <br>
- [Ops Runbook](artifact/references/ops.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/manlight87/telegrambot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, configuration values, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local HTTP endpoints, token-auth setup steps, and filesystem path configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
