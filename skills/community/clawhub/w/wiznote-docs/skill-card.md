## Description: <br>
Use when documents must be read from or maintained in a WizNote or 为知笔记 server, mirrored into a local repository, or organized under a configurable note category root. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[735140144](https://clawhub.ai/user/735140144) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small teams use this skill to connect an agent to a user-supplied WizNote server, list and fetch notes, create or update HTML notes, and keep repository-local document mirrors under a configured category root. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable agent or script access to private WizNote notes, including read and write operations. <br>
Mitigation: Install only for intended WizNote workflows, use a trusted HTTPS server URL, test note listing before writes, and verify updates in WizNote after write operations. <br>
Risk: WizNote credentials and mirrored private notes could be exposed if placed in shared files or repositories. <br>
Mitigation: Avoid hardcoding real passwords, prefer environment variables or explicit runtime secrets, consider a least-privileged account, and keep mirrored private notes out of shared repositories unless intended. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/735140144/wiznote-docs) <br>
- [README](artifact/README.md) <br>
- [README zh-CN](artifact/README.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance and helper usage patterns for user-configured WizNote read, write, and mirror workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
