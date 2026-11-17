## Description:

Uses Playwright to help an agent back up Weibo favorites, personal posts, or other users' posts as Markdown with optional images, videos, and long articles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hhjin](https://clawhub.ai/user/hhjin)

### License/Terms of Use:

MIT-0

## Use Case:

Users and agents use this skill to preserve Weibo favorites, personal timelines, or selected public creator posts for local review and archival workflows. It is intended for personal data backup or focused content backup, not large-scale commercial data collection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Weibo login cookies and account-linked browsing data.

Mitigation: Use an isolated browser profile, keep cookies.json and output folders out of shared or synced locations, and prefer --no-save-cookies when persistent cookies are not needed.

Risk: Connecting to a normal browser over CDP can expose broader browser state than the backup task requires.

Mitigation: Avoid connecting the skill to a regular personal browser; use a dedicated profile or browser session for Weibo backup work.

Risk: Video downloads can fetch large media files and currently depend on page-provided media URLs.

Mitigation: Use conservative download limits, review available storage before large runs, and avoid --download-video on untrusted pages until URL and redirect allowlisting is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hhjin/skills/weibo-backup)
- [ModelScope skill package](https://www.modelscope.cn/skills/hhjinhh/weibo-data-backup)
- [Weibo](https://weibo.com)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown files and downloaded media files, with agent-facing setup guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local output directories for Markdown, pictures, videos, articles, browser profile data, and cookies depending on selected options.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
