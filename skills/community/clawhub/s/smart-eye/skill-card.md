## Description: <br>
Controls and analyzes configured ONVIF PTZ IP cameras so an agent can capture frames, open live streams, search across camera snapshots, and perform pan-tilt-zoom movements through camera aliases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lubingshun](https://clawhub.ai/user/lubingshun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent interact with trusted internal IP cameras: capture still images for visual analysis, open local VLC live streams, locate objects across configured cameras, and issue PTZ movement commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Camera access can expose private scenes through snapshots or live streams. <br>
Mitigation: Install only where camera access is intended, restrict configured cameras to trusted internal IPs, and treat saved snapshots as private data. <br>
Risk: Broad natural-language triggers can cause real PTZ movement or live-stream access without enough confirmation. <br>
Mitigation: Avoid broad automatic invocation and require human review or scoped routing before commands that move cameras or open live streams. <br>
Risk: Camera credentials in camera-devices.json and VLC RTSP process arguments can be exposed locally. <br>
Mitigation: Protect camera-devices.json with appropriate file permissions, replace template credentials, and avoid using shared systems for VLC live-stream sessions. <br>


## Reference(s): <br>
- [ClawHub SmartEye skill page](https://clawhub.ai/lubingshun/smart-eye) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, File paths, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text or Markdown responses with snapshot paths and camera action status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save JPG snapshots locally and may launch VLC for live RTSP viewing when configured.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
