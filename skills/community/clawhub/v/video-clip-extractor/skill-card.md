## Description: <br>
Extract frames or short clips from videos using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utromaya-code](https://clawhub.ai/user/utromaya-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content reviewers use this skill to extract representative frames from local video files for inspection, sharing, or documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper writes to the requested output path and can overwrite an existing file. <br>
Mitigation: Choose an output path that is safe to create or replace before running the command. <br>
Risk: The skill processes local video files with ffmpeg. <br>
Mitigation: Use videos you intend to process and keep ffmpeg installed from a trusted source. <br>


## Reference(s): <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated image file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and writes image files to the user-provided output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
