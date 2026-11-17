## Description:

Extract and analyze TikTok video, profile, sound, hashtag, comment, caption, and engagement metadata using local yt-dlp commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuya227939](https://clawhub.ai/user/xuya227939)

### License/Terms of Use:

MIT-0

## Use Case:

External users, social media analysts, content strategists, and researchers use this skill to extract structured TikTok content signals and present them as concise research summaries or tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using yt-dlp with browser cookies can expose TikTok or other browser session credentials to a local command-line tool.

Mitigation: Use the cookie option only when necessary, prefer a dedicated browser profile or minimal cookie export, and run yt-dlp in an isolated environment.

Risk: TikTok extraction may be rate limited, region restricted, blocked for private accounts, or unavailable for removed content, leading to incomplete analysis.

Mitigation: Treat extracted results as best-effort, surface access limits to users, and retry later or request accessible URLs when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuya227939/skills/tiktok-research-kit)
- [SnapVee](https://snapvee.com)
- [Support Issues](https://github.com/xuya227939/tiktok-research-kit/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables and concise text with inline shell commands and parsed JSON field guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TikTok captions, creator details, upload dates, engagement stats, comments, sound metadata, profile/video tables, and access-error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact/SKILL.md, artifact/clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
