## Description:

Automates setup guidance for TDengine 3.3.6.0, including download, installation, service startup, and basic database validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnnyhou327](https://clawhub.ai/user/johnnyhou327)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to prepare a Linux host for TDengine by following download, installation, service management, and basic validation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run an external TDengine installer.

Mitigation: Verify the downloaded package with a trusted checksum or signature and inspect the installer before using elevated privileges.

Risk: The setup enables TDengine as a persistent system service.

Mitigation: Use it only on a host intended to run TDengine and confirm how to stop and disable the service before proceeding.

Risk: The setup may expose TDengine database ports 6030-6041.

Mitigation: Restrict those ports to trusted networks only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnnyhou327/skills/tdengine-setup)
- [TDengine 3.3.6.0 Linux x64 server package](https://www.taosdata.com/assets-download/TDengine-server-3.3.6.0-Linux-x64.tar.gz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux command-line tools: taos, systemctl, wget, and tar.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
