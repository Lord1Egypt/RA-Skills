## Description:

将提供的 YouTube 视频链接转录成完整中文稿，包含内容摘要和视频核心亮点，便于快速理解和复习。

This skill is ready for commercial/non-commercial use.

## Publisher:

[webguhui](https://clawhub.ai/user/webguhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a YouTube video link into a structured Chinese transcript, short summary, and key highlights for review or note-taking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may access YouTube using browser cookies or a cookies.txt file, exposing sensitive account data.

Mitigation: Avoid browser:chrome unless necessary, treat exported cookies as sensitive, and remove cookies files after use.

Risk: The download helper may run a mutable yt-dlp binary from /tmp.

Mitigation: Prefer an already installed, trusted yt-dlp binary or verify the downloaded binary before running the skill.

## Reference(s):

- [YouTube to Chinese ClawHub Skill Page](https://clawhub.ai/webguhui/skills/youtube-to-chinese)
- [yt-dlp latest release download](https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp)
- [Get cookies.txt LOCALLY Chrome extension](https://chrome.google.com/webstore/detail/get-cookiestxt-locally)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Chinese transcript sections, summary, highlights, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single structured Chinese-language response after audio download and transcription.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
