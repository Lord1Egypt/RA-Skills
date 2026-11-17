## Description:

Universal Video Analyzer Zh analyzes video frames and speech transcripts with a configured multimodal model API to produce structured Chinese reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantianbaicai](https://clawhub.ai/user/lantianbaicai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to analyze uploaded or local video files, combining sampled frames and speech transcription into a structured Chinese summary and report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send video frames, speech transcripts, prompts, and the configured model API key to an external provider.

Mitigation: Use only trusted HTTPS model endpoints, confirm provider data-handling terms, and avoid analyzing sensitive or unknown attachments.

Risk: Generated HTML reports may include model or transcript content that is not escaped or sanitized.

Mitigation: Treat generated HTML reports as untrusted content until reviewed or sanitized before sharing or opening in sensitive environments.

Risk: Automatic chat-triggered analysis may process private videos unintentionally.

Mitigation: Disable auto-analysis for sensitive chats or require user confirmation before running on attachments.

## Reference(s):

- [Multi-model configuration example](references/config_example.md)
- [Volcengine](https://www.volcengine.com/)
- [Zhipu AI](https://open.bigmodel.cn/)
- [DashScope](https://dashscope.console.aliyun.com/)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Console text plus Markdown report, HTML report, and extracted JPEG frame files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated in Chinese and saved beside the source video unless an output path is supplied.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
