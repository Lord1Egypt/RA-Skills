## Description: <br>
Use when converting a video clip into a GIF with ffmpeg, including optional trimming, frame rate, width, and output detail controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyxie2026](https://clawhub.ai/user/sallyxie2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to convert a local video clip into a GIF, optionally trimming by start time and duration and controlling frame rate and width. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The conversion depends on local ffmpeg and ffprobe binaries. <br>
Mitigation: Use a trusted ffmpeg installation and process only local files the user intentionally selects. <br>
Risk: The script writes to the requested GIF output path and may overwrite an existing file. <br>
Mitigation: Choose an output filename that is safe to create or overwrite before running the conversion. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated GIF file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the output path, file size, dimensions, and frame rate after conversion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
