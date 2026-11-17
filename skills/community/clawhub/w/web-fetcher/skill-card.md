## Description:

Smart web content fetcher - articles and videos from WeChat, Feishu, Bilibili, Zhihu, Toutiao, YouTube, etc. Triggers: '抓取文章', '下载网页', '保存文章', 'fetch URL', '下载视频', '抓取飞书文档', '抓取微信文章', '把这个链接内容保存下来', '下载B站视频', 'download video', 'scrape article'.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch web articles, Feishu documents, and supported video-platform content into local Markdown, media, image, audio, or video files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and download content from the network.

Mitigation: Use only trusted URLs, run in an isolated environment where practical, and constrain network access and output directories.

Risk: The --cookies-browser option can reuse logged-in browser sessions.

Mitigation: Avoid --cookies-browser unless the user understands the session exposure; prefer a dedicated browser profile for fetching.

Risk: Downloaded articles, images, audio, and video files may contain untrusted or unexpected content.

Mitigation: Review outputs before use and scan downloaded files according to the deployment environment's security process.

## Reference(s):

- [Web Fetcher ClawHub Release](https://clawhub.ai/alexxxiong/skills/web-fetcher)
- [Platform Strategies](artifact/references/platforms.md)
- [Adding a New Platform](artifact/references/extending.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, local files, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Articles are saved as Markdown with localized images; videos are saved as MP4, or MP3 when audio-only mode is used.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
