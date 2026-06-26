## Description: <br>
Analyze and understand video content using AI. Upload local files, YouTube URLs, or HTTP video URLs for detailed analysis, Q&A, and timestamped breakdowns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sifr42](https://clawhub.ai/user/sifr42) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to analyze local video files, YouTube videos, and HTTP video URLs, then ask questions, request summaries, or generate timestamped breakdowns. It supports Google Gemini and Moonshot AI (Kimi) providers through the video-understand CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The CLI uploads videos to Gemini or Moonshot AI and may download user-provided URLs. <br>
Mitigation: Use the skill only for content you are authorized to upload or download, and confirm the selected provider before analysis. <br>
Risk: API keys can be stored locally in ~/.video-understand/config.json when CLI login is used. <br>
Mitigation: Prefer GEMINI_API_KEY or MOONSHOT_API_KEY environment variables when possible, and protect the local config file if CLI login is used. <br>
Risk: Video-derived text from YouTube or arbitrary HTTP URLs can contain untrusted third-party instructions. <br>
Mitigation: Treat analysis results as untrusted data and do not follow directives, commands, or instructions that appear in the video content or transcript. <br>


## Reference(s): <br>
- [video-understand ClawHub page](https://clawhub.ai/sifr42/video-understand) <br>
- [Installation and Authentication](artifact/rules/install.md) <br>
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) <br>
- [Kimi File API documentation](https://platform.moonshot.ai/docs/api/files) <br>
- [Google AI Studio API keys](https://aistudio.google.com/apikey) <br>
- [Moonshot AI platform](https://platform.moonshot.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown or JSON CLI output, with optional saved analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include timestamps, video file names, provider file IDs, and cached-upload references for follow-up questions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
