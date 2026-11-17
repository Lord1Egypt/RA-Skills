## Description:

Chinese-language Sonos music playback skill for searching linked Sonos music services, queueing selected results, and starting playback while preserving Sonos App metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huacius](https://clawhub.ai/user/huacius)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a reusable Sonos on-demand playback workflow for NetEase Cloud Music and QQ Music through linked Sonos services. It is most useful in local-network Sonos environments where the required CLI, virtual environment, and playback wrapper scripts are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap flow installs an unpinned Python dependency from pip, which may reduce reproducibility across environments.

Mitigation: Review dependency behavior before deployment and pin package versions when stronger reproducibility is required.

Risk: The package relies on local workspace playback scripts that are referenced but not included in the release artifact.

Mitigation: Review or supply the expected playback scripts before using the skill, and validate the environment with the included check script.

Risk: The workflow accesses Sonos devices and linked music services on the local network.

Mitigation: Install only in trusted local-network environments where this device and service access is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huacius/skills/sonos-music-playback)
- [Publisher profile](https://clawhub.ai/user/huacius)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and environment configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Sonos network access, the sonos CLI, a Python virtual environment with soco, and workspace playback wrappers.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
