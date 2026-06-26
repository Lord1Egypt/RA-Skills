## Description: <br>
YouTube 视频处理助手 - Gemini 智能分析 + 下载 + 剪辑 + 配音 + 硬字幕合成 + 局域网 HTTP 分享 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoyta](https://clawhub.ai/user/zhaoyta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and developers use this skill to turn YouTube videos into short narrated remix clips with planned timestamps, generated Chinese voiceover, hard subtitles, and local-network sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a browser profile that may already be signed in and can send URLs or generated text to external AI and TTS services. <br>
Mitigation: Run it in an isolated environment or disposable browser profile, and avoid sensitive or private videos. <br>
Risk: The skill can download third-party video content and create derivative media. <br>
Mitigation: Confirm you have the right to reuse the source media before processing or sharing outputs. <br>
Risk: The skill can expose generated files on the local network through an HTTP server. <br>
Mitigation: Serve only non-sensitive outputs and stop or disable the HTTP server when sharing is complete. <br>
Risk: The skill may install or require media tooling such as ffmpeg, yt-dlp, and Python packages. <br>
Mitigation: Install dependencies in a controlled environment and review package sources before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoyta/video-remix) <br>
- [Gemini web app](https://gemini.google.com/) <br>
- [YouTube](https://www.youtube.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Files] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and generated media files such as MP4, MP3, and SRT outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow expects a Gemini-generated JSON plan and can start a local HTTP server for generated output files.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
