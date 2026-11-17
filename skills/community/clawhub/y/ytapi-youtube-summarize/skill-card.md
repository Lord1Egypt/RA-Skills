## Description:

Summarize a YouTube video, or the latest videos of a channel, into notes with key points, quotes and timestamped links, using transcripts from the YTAPI API. Use when the user shares a YouTube link and asks what it says, wants a TL;DR, notes, chapters, key takeaways or a digest of a creator's new uploads. Works on servers and cloud agents where direct YouTube fetching is blocked. 中文：总结 YouTube 视频、生成笔记。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ytapi](https://clawhub.ai/user/ytapi)

### License/Terms of Use:

MIT-0

## Use Case:

People reviewing YouTube content can turn a video or recent channel uploads into concise notes, timestamped key points, notable quotes, and digests using YTAPI transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saving the API key for future sessions can let those sessions use the key and consume credits.

Mitigation: Use the key for the current session only, or explicitly approve a protected credential store and which future sessions may access it.

Risk: Optional account creation sends the user's email address and verification code to YTAPI.

Mitigation: Create an account only with the user's approval and a user-selected email address.

## Reference(s):

- [YTAPI documentation](https://docs.ytapi.dev)
- [YTAPI](https://ytapi.dev)
- [auth-setup.md](artifact/references/auth-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown notes with key points, timestamped links, and notable quotes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Channel digests cover selected recent uploads; summaries follow the user's language.]

## Skill Version(s):

1.2.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
