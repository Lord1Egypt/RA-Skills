## Description: <br>
把srt字幕文件转换成markdown笔记333 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fafeidou](https://clawhub.ai/user/fafeidou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert SRT subtitles into Chinese Markdown notes while preserving the transcript text, adding punctuation, structuring short sections, and inserting screenshot markers when visual context helps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local screenshot post-processing may operate on unintended Markdown or MP4 files in the current directory. <br>
Mitigation: Run the skill in a dedicated folder containing only the intended Markdown and video files. <br>
Risk: The screenshot script invokes ffmpeg to process local video files. <br>
Mitigation: Review the script before running it and use ffmpeg from a trusted source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown notes with optional screenshot placeholders and generated local screenshot links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can read local Markdown and MP4 files, invoke ffmpeg for screenshots, and write processed Markdown and image files under output/.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
