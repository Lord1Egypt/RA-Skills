## Description: <br>
Rdk X5 Media helps agents guide RDK X5 users through audio recording and playback, video encoding and decoding, RTSP or WebSocket preview, HDMI and LCD display setup, and VNC desktop configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and field engineers working with RDK X5 boards use this skill to generate command-oriented guidance for configuring media devices, streaming camera or video output, setting display targets, and troubleshooting common audio or preview issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RTSP examples can expose camera credentials if real passwords are pasted into commands, shell history, logs, or shared transcripts. <br>
Mitigation: Use placeholders or environment-specific secret handling, avoid pasting real camera passwords into reusable commands, and rotate credentials if they are exposed. <br>
Risk: Preview, WebSocket, VNC, or camera services can expose device video or desktop access when run on an untrusted network. <br>
Mitigation: Run preview and remote access services only on trusted networks, restrict access where possible, and stop camera or web services when testing is complete. <br>
Risk: The guidance targets RDK X5 media hardware and installed tools, so commands may fail or change local audio, camera, display, or desktop settings on the wrong device. <br>
Mitigation: Confirm the board model, connected peripherals, and required binaries before execution, and review proposed commands before running them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/rdk-x5-media) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for RDK X5 media workflows and may need adaptation to the connected audio, camera, display, or network setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
