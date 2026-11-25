## Description:

使用用户指定的浏览器环境读取 YouTube 视频页面中实际可见的字幕，按目标语言与学习目标交付摘要、术语表和时间锚点；适用于单个章节、场景或短文学习，并在字幕关闭、缺失或语言不匹配时保留来源、报告限制，不根据音频或猜测补写内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Learners and educators use this skill to turn subtitles visible on a YouTube page into reviewable notes for language study, lesson review, or short video learning. It records missing subtitles and coverage limits instead of filling gaps from audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious because its setup uses an unpinned CLI and repository and reports a mismatch between the stated purpose and installation behavior; the scan did not inspect all content.

Mitigation: Before installing, verify the CLI and repository source and revision, and review the installation steps.

## Reference(s):

- [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee mirror](https://gitee.com/xxjrq/easy-webbridge)
- [OpenCLI YouTube browser adapter documentation](https://github.com/jackwener/OpenCLI/blob/main/docs/adapters/browser/youtube.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown study notes or a limitations report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in visible subtitles; one chapter, scene, or short passage per run, with at most 100 table rows.]

## Skill Version(s):

1.0.2 (source: server release metadata, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
