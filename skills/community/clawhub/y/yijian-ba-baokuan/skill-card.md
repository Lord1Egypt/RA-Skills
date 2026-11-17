## Description:

A content rewriting skill for self-media creators that extracts text from Douyin, Bilibili, or Xiaohongshu video links, analyzes viral content patterns, and drafts publish-ready copy for Xiaohongshu, Toutiao, and Douyin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roseryztzhoutong](https://clawhub.ai/user/roseryztzhoutong)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, content operators, and marketing teams use this skill to turn reference video links or copied scripts into viral-structure analysis and platform-specific draft copy for social publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask for raw platform session cookies for Xiaohongshu or Bilibili download paths.

Mitigation: Prefer public links or manually pasted text, avoid providing raw browser cookies when possible, and only use cookies in an isolated environment.

Risk: Optional downloader dependencies and ASR fallback create unclear download and local media-processing boundaries.

Mitigation: Review optional XHS-Downloader source before installation and treat fallback video download, audio extraction, and Whisper transcription as local media processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roseryztzhoutong/skills/yijian-ba-baokuan)
- [Publisher profile](https://clawhub.ai/user/roseryztzhoutong)
- [Bilibili public video API example](https://api.bilibili.com/x/web-interface/view?bvid={bvid})
- [Bilibili player API example](https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid})
- [Hugging Face mirror endpoint mentioned for Whisper model downloads](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code blocks and generated plain-text copy files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write rewritten copy to an output directory as text files; may require cookies for some platform collection paths.]

## Skill Version(s):

0.6.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
