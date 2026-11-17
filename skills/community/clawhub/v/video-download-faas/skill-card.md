## Description:

Download videos in MP4 format using yt-dlp with FaaS (Firecracker/Container) isolation. Start downloads, check status, and kill processes. Videos are automatically converted to MP4 format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lasurvivor](https://clawhub.ai/user/lasurvivor)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to start long-running video downloads, monitor progress, and stop active downloads on remote or headless systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised Firecracker/container isolation is not backed by the packaged files.

Mitigation: Use the skill only inside separately verified low-privilege isolation, or correct the isolation documentation before deployment.

Risk: Shared /tmp session, PID, and log files may expose URLs or let the wrong process be terminated.

Mitigation: Avoid private, signed, or token-bearing URLs until session files are stored in a private directory with restrictive permissions and PID/session validation is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lasurvivor/skills/video-download-faas)

## Skill Output:

**Output Type(s):** [shell commands, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands and command output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Starts background yt-dlp jobs and returns session identifiers, process identifiers, log paths, progress text, and termination status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
