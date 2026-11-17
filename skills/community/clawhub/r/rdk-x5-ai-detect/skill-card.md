## Description:

Guides an agent through running individual AI inference workflows on RDK X5, including YOLO detection, image classification, segmentation-related models, face, gesture, pose, open-vocabulary detection, stereo depth, ASR, and lightweight on-device LLM launches through TogetheROS.Bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run or troubleshoot one RDK X5 AI inference algorithm at a time on the board's BPU using ROS 2 launch commands. It is also useful when assessing which pre-built models and lightweight LLM workflows are appropriate for RDK X5.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RTSP example includes an inline username and password pattern that users could copy with real credentials.

Mitigation: Use protected configuration or a secret source for camera credentials, prefer read-only camera accounts, and avoid committing or sharing RTSP URLs that contain credentials.

Risk: The workflows can access camera, audio, or RTSP streams and expose a local web viewer on port 8000.

Mitigation: Run the viewer only on trusted networks, restrict access to the device, and confirm that capture and streaming comply with local privacy and consent requirements.

Risk: The skill suggests installing Python inference packages as part of the workflow.

Mitigation: Pin package versions and verify package sources before installation, especially on devices used for production or shared demos.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/skills/rdk-x5-ai-detect)
- [Publisher profile](https://clawhub.ai/user/katherineedwards2475)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume an RDK X5 platform with ROS 2, TogetheROS.Bot, BPU-compatible model files, and any required camera or audio hardware already configured.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
