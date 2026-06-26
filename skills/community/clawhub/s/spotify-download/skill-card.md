## Description: <br>
Helps an agent guide users through downloading MP3 files from Spotify playlists with spotify-download, ffmpeg, yt-dlp, and optional Spotify API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wgzesg](https://clawhub.ai/user/wgzesg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need command guidance for exporting Spotify playlist metadata, finding matching audio sources, and saving converted MP3 files to a chosen directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses network services, external tools, and writes downloaded audio files to disk. <br>
Mitigation: Verify the spotify-download package before use, install ffmpeg from a trusted source, prefer uvx or pipx isolation, and choose an intended output directory. <br>
Risk: Optional Spotify client secrets may be exposed through shell history, logs, or agent output. <br>
Mitigation: Avoid placing secrets in reusable commands, prefer careful environment handling, and redact credentials from generated output and transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wgzesg/spotify-download) <br>
- [Publisher profile](https://clawhub.ai/user/wgzesg) <br>
- [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include installation commands, credential-handling guidance, output-directory options, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
