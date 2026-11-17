## Description:

SmartEye lets an agent control and inspect configured ONVIF PTZ IP cameras, including frame capture, VLC live stream viewing, multi-camera object search, and pan-tilt-zoom movement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lubingshun](https://clawhub.ai/user/lubingshun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to give an agent access to private camera feeds, save still frames for visual analysis, open configured RTSP streams in VLC, locate objects across multiple cameras, and issue PTZ control commands by camera alias or brand.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private camera feeds and PTZ controls.

Mitigation: Install only for intended cameras, use dedicated low-privilege camera accounts, and keep camera endpoints limited to trusted networks.

Risk: Camera credentials are stored in camera-devices.json and RTSP URLs can include those credentials.

Mitigation: Restrict permissions on the camera configuration file, avoid shared machines for VLC viewing, and replace bundled example credentials before use.

Risk: Snapshot capture and broad multi-camera search triggers can save sensitive images locally.

Mitigation: Review or narrow activation phrases, limit configured cameras, and periodically delete saved snapshots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lubingshun/skills/smart-eye)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-compatible text with camera status messages, snapshot file paths, VLC launch results, and follow-up image-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JPG snapshots and may launch VLC with configured RTSP camera streams.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
