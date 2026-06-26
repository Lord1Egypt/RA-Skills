## Description: <br>
Universal Video Analyzer Zh analyzes video files with configurable multimodal models, combining extracted key frames and speech transcription to generate structured Chinese Markdown and HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lantianbaicai](https://clawhub.ai/user/lantianbaicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze video files through OpenClaw or the command line. It produces Chinese summaries that combine visual scene analysis, key information, and speech transcription. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video frames and transcribed speech are sent to the AI provider configured by VIDEO_ANALYZER_BASE_URL. <br>
Mitigation: Use only a trusted provider or private endpoint, and avoid sensitive or regulated videos unless that provider is approved for the data. <br>
Risk: The required VIDEO_ANALYZER_API_KEY grants access to the configured model provider. <br>
Mitigation: Keep the API key private, store it outside shared files, and rotate it if exposure is suspected. <br>
Risk: Generated Markdown, HTML, and key-frame files may contain private video content. <br>
Mitigation: Store, share, and delete generated reports and frame folders according to the user's data-handling requirements. <br>
Risk: Dependencies are specified without a lockfile, which can make installs less reproducible. <br>
Mitigation: Install in an isolated environment and prefer pinned dependency versions or a lockfile for production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lantianbaicai/universal-video-analyzer-zh) <br>
- [Multi-model configuration example](references/config_example.md) <br>
- [Volcengine](https://www.volcengine.com/) <br>
- [Zhipu AI](https://open.bigmodel.cn/) <br>
- [DashScope](https://dashscope.console.aliyun.com/) <br>
- [FFmpeg downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration] <br>
**Output Format:** [Console text plus generated Markdown and HTML report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local video file, ffmpeg, Python dependencies, and VIDEO_ANALYZER_API_KEY; saves extracted key frames locally.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
