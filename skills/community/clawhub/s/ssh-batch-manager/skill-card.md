## Description:

Batch SSH key management. Distribute/remove SSH keys to/from multiple servers with intelligent connectivity pre-check and source tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stj001](https://clawhub.ai/user/stj001)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and administrators use this skill to manage SSH key distribution and removal across configured servers, check connectivity, and maintain source comments for auditability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent Web UI service that can expose SSH management functions.

Mitigation: Review the post-install service before installation, disable auto-start when not needed, and bind or access the UI through loopback only.

Risk: The skill handles SSH credentials and server access, including password-based SSH flows.

Mitigation: Prefer key-based authentication, verify host keys, restrict credential/configuration file access, and avoid storing broad administrative credentials.

Risk: Batch enable or disable operations can change access across multiple servers at once.

Mitigation: Require explicit confirmation, review the target server list, and test on non-production targets before using enable-all or disable-all.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/stj001/skills/ssh-batch-manager)
- [SKILL.md](artifact/SKILL.md)
- [README.en.md](artifact/README.en.md)
- [WEB-UI-GUIDE.md](artifact/WEB-UI-GUIDE.md)
- [RELEASE-NOTES.md](artifact/RELEASE-NOTES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown/text guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local SSH management configuration and remote authorized_keys when execution commands are run.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
