## Description: <br>
Batch SSH key management. Distribute/remove SSH keys to/from multiple servers with intelligent connectivity pre-check and source tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[STJ001](https://clawhub.ai/user/STJ001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and system administrators use this skill to distribute, remove, and audit SSH public-key access across configured servers, with helper commands for encrypted credentials, key generation, and a local Web UI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change SSH access across many configured servers. <br>
Mitigation: Review the server list and credential files before use, and require explicit confirmation for both enable and disable operations. <br>
Risk: The release installs a persistent Web UI with unsafe defaults. <br>
Mitigation: Disable the Web UI unless needed, harden service access, and bind it to 127.0.0.1. <br>
Risk: Disabling SSH host key verification can hide server impersonation or misrouting. <br>
Mitigation: Avoid disabling SSH host key verification in production and maintain known-good host key records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/STJ001/ssh-batch-manager) <br>
- [Source homepage](https://gitee.com/subline/onepeace/tree/develop/src/skills/ssh-batch-manager) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.en.md](artifact/README.en.md) <br>
- [WEB-UI-GUIDE.md](artifact/WEB-UI-GUIDE.md) <br>
- [Release notes](artifact/RELEASE-NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for SSH key distribution, removal, encryption, and Web UI management.] <br>

## Skill Version(s): <br>
2.1.9 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
