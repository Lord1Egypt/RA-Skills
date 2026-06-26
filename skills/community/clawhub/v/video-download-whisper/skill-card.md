## Description: <br>
Downloads videos from sites such as Bilibili and YouTube, extracts audio, and uses Whisper to produce text transcripts for analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohanyang92](https://clawhub.ai/user/haohanyang92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve video content they are permitted to download, convert it to audio, and generate transcripts for downstream review or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downloading videos with browser cookies can expose account-scoped access if used broadly. <br>
Mitigation: Use cookies only when intentionally scoped to the exact account, browser profile, and site needed for allowed content. <br>
Risk: Downloaded media, extracted audio, or transcripts may be written to shared temporary locations or overwrite existing files. <br>
Mitigation: Write outputs to a private folder and check destination filenames before rerunning commands. <br>
Risk: The workflow can download content from many sites, including content the user may not have rights to copy. <br>
Mitigation: Use the skill only for videos the user is allowed to download and process. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haohanyang92/video-download-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated transcript text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp, ffmpeg, and Whisper; scripts can write downloaded media, extracted audio, and transcript files to a selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
