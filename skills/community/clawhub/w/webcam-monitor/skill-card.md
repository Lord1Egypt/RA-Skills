## Description: <br>
Webcam motion detection and monitoring system for WSL2 with USB/IP passthrough. Use when setting up motion detection on a USB webcam, monitoring camera snapshots, auto-analyzing images with AI, or managing webcam-based security/activity monitoring. Supports Insta360 Link and other UVC cameras via usbipd on Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jadegaul](https://clawhub.ai/user/jadegaul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure webcam motion detection, snapshot capture, local cleanup, live preview, and queued image analysis in WSL2 environments with USB/IP camera passthrough. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture identifiable webcam images and queue them for analysis. <br>
Mitigation: Run it only where camera capture is authorized, obtain consent for people in view, keep retention short, and avoid storing identifying traits unless they are necessary and consented. <br>
Risk: The web preview can expose a live camera feed on the local network without authentication. <br>
Mitigation: Bind the preview server to 127.0.0.1 before use, or add firewall and authentication controls before exposing it beyond the local machine. <br>
Risk: Snapshots, queue files, and logs may leave sensitive camera data on disk. <br>
Mitigation: Review cleanup settings before deployment, restrict filesystem access to the camera workspace, and confirm old snapshots and queue files are deleted as intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jadegaul/webcam-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, configuration notes, and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local camera setup and operating guidance; runtime scripts may create snapshots, logs, and analysis queue files under the user's OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
