## Description: <br>
Extract frames or short clips from videos using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and media workflows use this skill to extract a first frame, timestamped frame, or indexed frame from a local video for inspection, sharing, or UI documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The frame extraction script overwrites an existing file at the selected --out path. <br>
Mitigation: Choose a deliberate output path, avoid important existing files, and review the path before running the command. <br>
Risk: The skill depends on locally installed ffmpeg to process user-supplied video files. <br>
Mitigation: Install ffmpeg from a trusted source and run the skill only on video files you are comfortable processing locally. <br>


## Reference(s): <br>
- [FFmpeg](https://ffmpeg.org) <br>
- [Video Frames on ClawHub](https://clawhub.ai/steipete/video-frames) <br>
- [steipete ClawHub profile](https://clawhub.ai/user/steipete) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text] <br>
**Output Format:** [Shell script output plus an extracted image file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and writes the requested output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
