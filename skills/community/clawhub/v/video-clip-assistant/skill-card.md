## Description: <br>
视频自动剪辑助手 uses FFmpeg-based scripts to cut clips, burn subtitles, export social-video formats, and extract highlight segments from local video files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyongliang-eccom](https://clawhub.ai/user/xuyongliang-eccom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to generate video-editing shell commands and local script workflows for clipping videos, adding subtitles, exporting short-form formats, and extracting highlights. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local FFmpeg commands can overwrite output files when overwrite mode is used. <br>
Mitigation: Use a dedicated output folder and avoid output names that already matter. <br>
Risk: Optional ASR tools may process private recordings when generating subtitles. <br>
Mitigation: Verify the selected ASR tool or provider before using it with private recordings. <br>
Risk: The skill runs local media-processing scripts against user-selected files. <br>
Mitigation: Run the scripts in a controlled working directory and inspect input and output paths before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuyongliang-eccom/video-clip-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and Python script references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local FFmpeg-oriented workflows and file outputs selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
