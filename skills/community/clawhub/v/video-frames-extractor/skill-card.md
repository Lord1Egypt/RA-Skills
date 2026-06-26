## Description: <br>
Extract frames or short clips from videos using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, media reviewers, and content teams use this skill to extract a selected frame or quick thumbnail from a local video for inspection, sharing, or UI review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ffmpeg command can overwrite the output file specified by the user. <br>
Mitigation: Choose a fresh output filename or use a disposable output folder before running the frame extraction command. <br>
Risk: The skill depends on a local ffmpeg installation. <br>
Mitigation: Install ffmpeg only from a trusted package source and confirm the binary is available before processing videos. <br>


## Reference(s): <br>
- [Video Frames on ClawHub](https://clawhub.ai/utromaya-code/video-frames-extractor) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash code blocks and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The frame script writes a requested JPG or PNG output file and prints the output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
