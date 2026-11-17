## Description:

轻量快捷的音乐搜索工具。一条命令搜歌、拿播放链接，零依赖即开即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangalexhy](https://clawhub.ai/user/zhangalexhy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search for songs or artists from the command line and retrieve a playback link for a selected result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Music search terms are sent to external services.

Mitigation: Avoid private, identifying, confidential, or sensitive search queries when using the skill.

Risk: Playback, detail, cover, or lyric links are third-party content shown in terminal output.

Mitigation: Treat returned links as untrusted and review them before opening or sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangalexhy/skills/quick-music)
- [Search API endpoint](https://kw-api.cenguigui.cn/)
- [Playback API endpoint](https://api.xcvts.cn/api/music/migu)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Terminal text with song lists and playback, detail, cover, or lyric links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are paginated with page and limit options; playback retrieval uses a selected result index.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
