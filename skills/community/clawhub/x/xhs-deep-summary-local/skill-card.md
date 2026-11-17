## Description:

本地免费一键深度总结小红书视频笔记：使用 yt-dlp 拉取视频、faster-whisper 本地转写，输出元数据和逐字稿，再由 LLM 生成结构化深度总结。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanming0007](https://clawhub.ai/user/yuanming0007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to process Xiaohongshu video notes locally, generate transcript files and metadata, and produce a structured deep summary for personal knowledge management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network fetching can download media or metadata from Xiaohongshu links that the user has not fully inspected.

Mitigation: Use only trusted Xiaohongshu video links and run the skill in a contained working directory.

Risk: Browser cookies, if supplied for gated videos, can expose account-access material.

Mitigation: Avoid providing cookies unless required, understand the account risk, and use a least-privileged browser session where possible.

Risk: Transcript and summary archives may persist sensitive or unauthorized platform content.

Mitigation: Confirm Obsidian or IMA write targets before archival and keep downloaded, transcribed, or summarized content private unless authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanming0007/skills/xhs-deep-summary-local)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with local JSON and transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces xhs_meta.json and xhs_temp.txt from a Xiaohongshu video URL; temporary media files may be created during processing.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
