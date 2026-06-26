## Description: <br>
Summarizes YouTube videos without subtitles by using local ASR with yt-dlp, faster-whisper, and ffmpeg to produce transcripts, timeline bullets, and optional frames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yifany-github](https://clawhub.ai/user/yifany-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to summarize YouTube videos when subtitles are missing or empty and no external API keys should be used. It supports local transcript generation, deterministic summary output, time-range bullets, and optional extracted video frames. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow contacts YouTube and writes downloaded media-derived transcripts, summaries, and frames to a local output folder. <br>
Mitigation: Use a dedicated output directory and delete transcripts or frames when they are no longer needed. <br>
Risk: ASR output can contain homophone errors or incorrect names, numbers, and other details. <br>
Mitigation: Review transcript and timeline details before sharing or relying on the summary. <br>
Risk: The skill depends on local execution of yt-dlp, ffmpeg, and faster-whisper. <br>
Mitigation: Install those tools from trusted sources and run the workflow only in an environment where local media processing is acceptable. <br>


## Reference(s): <br>
- [Workflow notes](references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/yifany-github/youtube-asr-summarize) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated artifacts include summary.md, transcript.txt, transcript.srt, and optional JPEG frames.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with yt-dlp, ffmpeg, and faster-whisper; contacts YouTube for video metadata, subtitles, audio, and optional video frames.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
