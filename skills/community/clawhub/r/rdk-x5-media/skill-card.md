## Description:

Guides agents through RDK X5 media workflows for audio recording and playback, video codec use, RTSP streaming, HDMI and MIPI LCD configuration, WebSocket preview, and VNC setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and troubleshoot multimedia features on intended RDK X5 devices, including audio devices, camera streams, displays, and remote desktop access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: RTSP examples can expose or normalize camera credentials in command lines.

Mitigation: Use least-privileged camera accounts, avoid copying real credentials into shared commands, and prefer protected credential handling.

Risk: VNC remote desktop access can expose the device if enabled on untrusted networks.

Mitigation: Enable VNC only on trusted networks with strong authentication, and disable it when remote desktop access is no longer needed.

Risk: Media and display commands are device-specific and may not apply outside intended RDK X5 environments.

Mitigation: Use the skill only on intended RDK X5 devices and review commands before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires intended RDK X5 hardware and media tools such as arecord and ffmpeg where applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
