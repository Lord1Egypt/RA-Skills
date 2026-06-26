## Description: <br>
Downloads audio (MP3) and video (MP4) from YouTube URLs for offline viewing, music extraction, educational content, playlists, and batch downloads with quality options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XanderRey](https://clawhub.ai/user/XanderRey) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to download YouTube audio, video, playlists, or URL batches for offline use, music extraction, content archiving, and educational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scripts automatically download and persist yt-dlp and FFmpeg executables from GitHub without pinned versions, checksum verification, or a separate opt-in step. <br>
Mitigation: Review the scripts before running them, or preinstall trusted pinned versions of yt-dlp and FFmpeg so the scripts use those tools instead. <br>
Risk: Playlist or batch downloads can consume significant disk space and bandwidth. <br>
Mitigation: Choose output folders deliberately and use range or maximum-download options for large playlists. <br>


## Reference(s): <br>
- [YouTube Download Patterns & Best Practices](references/download-patterns.md) <br>
- [ClawHub release page](https://clawhub.ai/XanderRey/youtube-media-downloader) <br>
- [yt-dlp release download used by scripts](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp) <br>
- [FFmpeg builds release download used by scripts](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and downloaded media files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create MP3 or MP4 files in user-selected output directories and may download helper executables into the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
