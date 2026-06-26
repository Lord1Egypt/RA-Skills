## Description: <br>
Video summarization. Trigger: 1.User provides a video link (Bilibili/YouTube/Douyin/Twitter/TikTok etc.), 2.Summarize this video <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yilsonyan](https://clawhub.ai/user/yilsonyan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other agent users use this skill to fetch subtitles or transcribe public videos from supported platforms, then summarize the resulting transcript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YouTube processing may read Chrome browser session cookies. <br>
Mitigation: Avoid YouTube mode unless cookie access is acceptable, or use an isolated browser profile for video processing. <br>
Risk: The installer can make broad system changes while installing local dependencies. <br>
Mitigation: Review the installer before running it and install dependencies manually when stricter system control is required. <br>
Risk: Cached transcripts and summary files may retain private or confidential video content. <br>
Mitigation: Delete cache/ and summarize_result/ after processing sensitive videos. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yilsonyan/video-summarize) <br>
- [Whisper base model download](https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.bin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and generated transcript or summary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates cached transcript text and summary markdown files under local skill directories.] <br>

## Skill Version(s): <br>
1.0.2026050302 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
