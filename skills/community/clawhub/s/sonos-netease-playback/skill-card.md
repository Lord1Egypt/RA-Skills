## Description: <br>
Portable Sonos + Netease playback skill for OpenClaw environments that helps an agent install, validate, and use a reusable workflow for playing a specific song to a Sonos room while preserving Sonos App metadata display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huacius](https://clawhub.ai/user/huacius) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to set up a portable Sonos/Netease playback environment, verify required local dependencies, and invoke a standard playback wrapper for Sonos rooms. It is most useful after first install, migration, or repair of the local playback environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bootstrap script creates a local Python virtual environment and installs the SoCo dependency with pip. <br>
Mitigation: Run the installer only in environments where local dependency installation is acceptable, and review the generated virtual environment path before use. <br>
Risk: The package expects a separate Sonos/Netease playback Python script that is not included in the artifact. <br>
Mitigation: Review or provide the playback script at the configured path before using the wrapper to play media. <br>
Risk: Playback depends on the local sonos CLI, reachable Sonos devices, and a working linked Netease service authorization. <br>
Mitigation: Use the included environment check and confirm Sonos App service authorization before relying on playback results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huacius/sonos-netease-playback) <br>
- [Publisher Profile](https://clawhub.ai/user/huacius) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, validation, troubleshooting, and playback workflow guidance for a local Sonos/Netease setup.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
