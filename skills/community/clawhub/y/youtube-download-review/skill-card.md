## Description: <br>
Downloads YouTube videos, cover art, optional simplified Chinese hard subtitles, and a short music-media review into a per-video folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[copfee](https://clawhub.ai/user/copfee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and content reviewers use this skill to download YouTube media they are permitted to save, optionally burn simplified Chinese subtitles, and generate a concise music-focused recommendation note. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can download media from YouTube that the user may not have rights to save or reuse. <br>
Mitigation: Use the skill only for videos the user is allowed to download and process. <br>
Risk: The workflow depends on local yt-dlp and ffmpeg binaries. <br>
Mitigation: Install yt-dlp and ffmpeg from trusted sources before running the generated commands. <br>
Risk: Video downloads and subtitle burn-in can consume significant disk space and processing time. <br>
Mitigation: Run the skill from the intended output folder and confirm adequate disk space before transcoding. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/copfee/youtube-download-review) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Per-video folder containing MP4 video files, JPG cover art, optional SRT subtitles, a Markdown review, and a terminal summary.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local yt-dlp and ffmpeg; may create large media files during download and transcoding.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
