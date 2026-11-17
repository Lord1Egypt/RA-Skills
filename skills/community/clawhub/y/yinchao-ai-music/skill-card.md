## Description:

帮助用户通过音潮创作可试听的歌曲、纯音乐和 BGM，也支持歌词谱曲、参考音频创作及纯歌词创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[joeydqyuan](https://clawhub.ai/user/joeydqyuan)

### License/Terms of Use:

MIT-0

## Use Case:

创作者和其他外部用户可将文字提示或已有歌词变成歌曲、纯音乐或配乐，也可使用有权分享的参考音频创作新作品，或只创作歌词。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill requires an API key and sends generation requests to YinChao's external service.

Mitigation: Use it only if you accept the external service; keep the API key private and avoid unrelated secrets in configured key files.

Risk: Locally supplied reference audio may be uploaded to YinChao for generation.

Mitigation: Share only audio you have rights to use and inform the user before uploading a local file.

## Reference(s):

- [音潮开放平台](https://platform.yinchaoyongxian.com/?register_channel=clawhub)
- [ClawHub skill listing](https://clawhub.ai/joeydqyuan/skills/yinchao-ai-music)
- [歌曲生成接口](https://platform.yinchaoyongxian.com/docs/api-reference/song/song-generate-post)
- [纯音乐生成接口](https://platform.yinchaoyongxian.com/docs/api-reference/song/song-instrumental-post)
- [歌词生成接口](https://platform.yinchaoyongxian.com/docs/api-reference/lyric/lyric-generate-post)
- [参考音频创作指南](https://platform.yinchaoyongxian.com/docs/guides/reference-generate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with listening links and lyrics, or lyrics-only text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Music generation can return multiple versions; instrumental results omit lyrics.]

## Skill Version(s):

1.6.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
