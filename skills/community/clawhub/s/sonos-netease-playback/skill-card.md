## Description:

Provides a portable OpenClaw workflow for installing Sonos playback prerequisites and playing Netease Music tracks to a Sonos room while preserving Sonos app metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huacius](https://clawhub.ai/user/huacius)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to bootstrap and validate a Sonos/Netease playback setup, then run a standard wrapper to search for and play requested tracks on a local Sonos room. This release is deprecated in favor of sonos-music-playback for fresh installs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a local Python virtual environment, install the SoCo package from the configured pip source, and create or chmod a Sonos playback wrapper in the workspace.

Mitigation: Review the setup scripts before running them, pin or mirror Python dependencies in stricter environments, and use the documented environment variables to point the venv, wrapper, and playback script to expected paths.

Risk: Playback depends on reachable local Sonos devices, an installed sonos CLI, and an authorized Netease service in the Sonos app.

Mitigation: Run scripts/check_env.sh before playback and reauthorize Netease in the Sonos app if search works but playback fails.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huacius/skills/sonos-netease-playback)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local setup actions, dependency installation, environment checks, and Sonos playback commands.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
