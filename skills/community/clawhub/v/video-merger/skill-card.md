## Description: <br>
多片段短视频自动拼接工具，支持按文件名排序、统一音视频参数、淡入淡出转场、分块/完整拼接，适合短剧、分镜头视频批量拼接 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[machunlin](https://clawhub.ai/user/machunlin) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, video editors, and short-form content producers use this skill to merge numbered MP4 segments into complete or chunked videos with consistent encoding, frame rate, resolution, and fade transitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local ffmpeg and ffprobe binaries for video processing. <br>
Mitigation: Install ffmpeg from a trusted source and review custom binary paths before using --ffmpeg-path or --ffprobe-path. <br>
Risk: The output path may be created or overwritten during merging. <br>
Mitigation: Choose an output file or directory that is intended for generated video artifacts and keep backups of important files. <br>
Risk: The skill processes every matching MP4 file in the selected input directory. <br>
Mitigation: Point --input only at the intended segment folder and verify numeric filename prefixes before running a merge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/machunlin/video-merger) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python examples; runtime output is MP4 video files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local ffmpeg and ffprobe binaries; can produce one merged MP4 file or multiple chunked MP4 files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact package files report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
