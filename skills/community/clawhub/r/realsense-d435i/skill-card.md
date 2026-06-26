## Description: <br>
Intel RealSense D435i depth camera skill for capturing depth photos, 3D point clouds, IMU data, and RGBD videos with date-organized local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zh1fen](https://clawhub.ai/user/zh1fen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and robotics engineers use this skill to operate a local Intel RealSense D435i camera for depth images, point-cloud capture, IMU recordings, and synchronized RGBD video collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Captured camera, depth, point-cloud, video, and IMU files may contain private physical-environment data. <br>
Mitigation: Keep the output path under user control, use short intentional recordings, and handle saved files according to the user's data-retention and privacy requirements. <br>
Risk: The skill requires local hardware access and external runtime dependencies such as pyrealsense2, OpenCV, NumPy, and ffmpeg. <br>
Mitigation: Install dependencies only from trusted sources and run the capture commands only on systems intended to operate the RealSense device. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zh1fen/realsense-d435i) <br>
- [MeshLab](https://www.meshlab.net/downloads) <br>
- [3D Viewer](https://3dviewer.net/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; camera runs produce JPG, PNG, MP4, PLY, and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Captured outputs are written to a local output directory organized by content type and date.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
