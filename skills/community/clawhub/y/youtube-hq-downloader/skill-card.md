## Description: <br>
Downloads high-quality silent video and pure audio from YouTube, then merges them into a video with sound using ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[accidwar](https://clawhub.ai/user/accidwar) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and end users can use this skill to download separate high-quality YouTube video and audio streams and combine them into a local playable media file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports local downloader scripts that run user-influenced shell commands and overwrite predictable output files. <br>
Mitigation: Review before installation, run only with trusted URLs, filenames, and output directories, and prefer a hardened version that validates paths and avoids shell-based command execution. <br>
Risk: The scripts can install or reuse yt-dlp and write downloaded media into user-selected folders. <br>
Mitigation: Approve dependency installation separately, use a controlled virtual environment, and verify the selected output directory before running the downloader. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/accidwar/youtube-hq-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown instructions with shell command examples; scripts produce local MP4 media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a YouTube URL and optional output name and output directory; writes downloaded and merged media to a local folder.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
