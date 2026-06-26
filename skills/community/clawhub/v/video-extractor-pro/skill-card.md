## Description: <br>
Video Extractor Pro helps agents extract still frames, frame sequences, short clips, GIFs, and metadata from local video files using ffmpeg and ffprobe. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SxLiuYu](https://clawhub.ai/user/SxLiuYu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content analysts, and video reviewers use this skill to extract representative frames, short clips, GIF previews, and video metadata from local videos for analysis, review, and material collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on local ffmpeg and ffprobe binaries to process media. <br>
Mitigation: Install ffmpeg and ffprobe from a trusted source and keep them updated. <br>
Risk: Output commands may overwrite existing files at the requested output path. <br>
Mitigation: Review output filenames and directories before running extraction commands, especially when reusing paths. <br>
Risk: The artifact documentation and command labels are primarily in Chinese. <br>
Mitigation: Confirm command intent and arguments before execution when the operator is not fluent in Chinese. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SxLiuYu/video-extractor-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, JSON] <br>
**Output Format:** [Terminal text plus generated media files such as JPG or PNG frames, video clips, GIFs, and JSON video metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local ffmpeg and ffprobe; selected commands may overwrite existing output paths.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
