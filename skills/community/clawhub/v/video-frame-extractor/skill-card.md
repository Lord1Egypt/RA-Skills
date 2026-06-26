## Description: <br>
This skill should be used when extracting frames from video files, such as generating keyframe sequences from videos, creating video thumbnails at intervals, or preparing video frames for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanghaoyu1997](https://clawhub.ai/user/huanghaoyu1997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to guide an agent through extracting sampled image frames from video files with FFmpeg, including parameter selection, command execution, output checks, and OpenCV fallback planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may run FFmpeg on local video files and write extracted frames to a selected folder. <br>
Mitigation: Confirm the input video path, output folder, frame rate, scale, and write permissions before execution. <br>
Risk: Installing FFmpeg or changing PATH can affect managed or shared machines. <br>
Mitigation: Require explicit user approval before installing FFmpeg, using package managers, or modifying PATH. <br>


## Reference(s): <br>
- [FFmpeg Windows builds](https://www.gyan.dev/ffmpeg/builds/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and parameter tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides creation of JPEG frame files in a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
