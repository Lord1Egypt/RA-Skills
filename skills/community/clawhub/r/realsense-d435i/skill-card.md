## Description:

Intel RealSense D435i depth camera operation skill for depth photos, 3D point clouds, IMU data, and RGBD video recording with automatic date-based output organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh1fen](https://clawhub.ai/user/zh1fen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate an Intel RealSense D435i camera from an agent workflow and capture local RGB, depth, point-cloud, video, and IMU data for robotics, perception, or sensor-data collection tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a RealSense camera and save potentially sensitive RGB, depth, point-cloud, video, and IMU data locally.

Mitigation: Run it only in trusted capture environments, choose an approved local output directory, and review collected data before sharing or retaining it.

Risk: The security summary flags unsafe FFmpeg path handling for RGBD recording workflows.

Mitigation: Use a simple trusted output path without quotes or newlines, avoid shared or untrusted workflows until reviewed, and patch the FFmpeg manifest handling before broader use.

Risk: The capture script interacts with camera hardware and writes files to disk.

Mitigation: Use a virtual environment, avoid administrative privileges, and review the script and dependencies before installation.

## Reference(s):

- [MeshLab](https://www.meshlab.net/downloads)
- [CloudCompare](https://www.dashcamviewer.com/)
- [Online 3D Viewer](https://3dviewer.net/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python script usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can lead to local capture files including JPEG, PNG, MP4, PLY, and CSV outputs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
