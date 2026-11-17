## Description:

Generates 5-6 minute industry AI short videos from natural-language prompts through outline, narration, HTML, TSX, TTS, timing, and Remotion rendering steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwiw](https://clawhub.ai/user/liwiw)

### License/Terms of Use:

MIT

## Use Case:

Developers and content-production engineers use this skill to turn a natural-language topic into a short industry explainer video, including generated slide content, narration, audio, TSX/Remotion components, timing alignment, and an MP4 render.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DashScope credentials may be exposed, stale, or over-scoped.

Mitigation: Rotate or remove the embedded DashScope key, then provide a scoped credential only through a trusted credential file or secret path.

Risk: Generated HTML can include untrusted model-produced content that is later opened or rendered.

Mitigation: Sanitize generated HTML and review rendered content before opening it in a browser or passing it to Remotion.

Risk: User prompts and generated narration may be sent to external DashScope services.

Mitigation: Avoid sensitive input and keep base_url on the official HTTPS DashScope host.

Risk: Generated narration or visuals may contain unsupported claims, especially numeric or industry-specific assertions.

Mitigation: Review generated script, slide text, and benchmark outputs before publishing a video.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liwiw/skills/video-pipeline)
- [Setup Guide](artifact/setup_guide.md)
- [Bug Log](artifact/references/buglog.md)
- [Node.js](https://nodejs.org/)
- [Python](https://python.org/)
- [FFmpeg](https://ffmpeg.org/download.html)
- [DashScope Compatible Mode Endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with JSON snippets, generated Python/TSX/HTML artifacts, MP3 audio, timing JSON, and MP4 video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Node.js, FFmpeg, Remotion, Edge TTS, and a DashScope API credential; generated HTML should be reviewed before rendering.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
