## Description: <br>
Play audio on Sonos with intelligent state restoration - pauses streaming, skips Line-In/TV/Bluetooth, resumes everything. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawdianova](https://clawhub.ai/user/clawdianova) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation users use this skill to play local audio announcements or sound effects on Sonos speakers while preserving prior playback state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill starts a local HTTP server for media files and can stop processes bound to the configured port. <br>
Mitigation: Use a dedicated media directory and port, confirm the port is not used by another service, and review process cleanup behavior before running. <br>
Risk: The security summary reports unsafe shell command usage around server start and stop operations. <br>
Mitigation: Prefer a fixed release that uses argument-list subprocess calls, validates paths, binds narrowly, and stops only the server process it started. <br>
Risk: Pointing media_dir at broad or private directories could expose local files through the temporary media server. <br>
Mitigation: Use only a trusted, minimal directory containing the intended audio files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawdianova/sonos-announce) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ffprobe, and the soco Python package; uses local network access to discover and control Sonos speakers.] <br>

## Skill Version(s): <br>
1.0.4 (source: server-resolved release metadata; SKILL.md frontmatter lists 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
