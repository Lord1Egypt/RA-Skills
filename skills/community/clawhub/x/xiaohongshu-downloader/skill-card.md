## Description: <br>
Download and summarize Xiaohongshu (小红书/RedNote) videos, producing a resource pack with video, audio, subtitles, transcript, and optional AI summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smile7up](https://clawhub.ai/user/smile7up) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to download Xiaohongshu/RedNote videos, extract audio and subtitles, generate transcripts, and prepare structured Markdown summaries from downloaded video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses the user's logged-in browser cookies by default for Xiaohongshu downloads. <br>
Mitigation: Review before installation, prefer --browser none when possible, or use a dedicated Xiaohongshu browser profile. <br>
Risk: The skill saves downloaded videos, audio, transcripts, metadata, and summaries to a local output folder. <br>
Mitigation: Choose an appropriate output directory and review saved files before sharing or syncing them. <br>
Risk: Downloaded content may be subject to copyright restrictions or Xiaohongshu terms of service. <br>
Mitigation: Use only for content you are authorized to download and follow the platform's terms. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/smile7up/xiaohongshu-downloader) <br>
- [Publisher profile](https://clawhub.ai/user/smile7up) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [FFmpeg](https://ffmpeg.org/) <br>
- [uv](https://docs.astral.sh/uv/) <br>
- [Video Summary Prompt Template](reference/summary-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Text, Markdown] <br>
**Output Format:** [Markdown guidance with bash commands; local media, subtitle, transcript, metadata, and summary files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Downloads are saved locally, typically under the configured output directory; summary mode adds metadata and a Markdown summary.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
