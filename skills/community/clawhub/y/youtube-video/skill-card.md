## Description:

Manage YouTube videos through the yutu CLI, including listing, uploading, updating, deleting, rating, and reporting videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openwaygate](https://clawhub.ai/user/openwaygate)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, channel operators, and developers use this skill to perform authenticated YouTube video management from an agent workflow after configuring Google OAuth credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform credentialed YouTube operations that upload, update, delete, rate, or report videos.

Mitigation: Require explicit confirmation before mutating channel or video state, and review video IDs, privacy settings, titles, descriptions, ratings, and report reasons before execution.

Risk: OAuth client secrets and cached YouTube tokens may be exposed through files, environment variables, repositories, or prompts.

Mitigation: Protect client_secret.json, youtube.token.json, YUTU_CREDENTIAL, and YUTU_CACHE_TOKEN; keep them out of repositories, logs, and prompts.

Risk: The CLI installation guidance can install an unpinned yutu release.

Mitigation: Use a pinned and verified yutu release where possible before running authenticated commands.

Risk: Uploads may unintentionally publish content or notify subscribers.

Mitigation: Prefer private uploads and disabled subscriber notifications unless public publication and notifications are intentional.

## Reference(s):

- [Yutu Project](https://github.com/eat-pray-ai/yutu)
- [Yutu README](https://github.com/eat-pray-ai/yutu#readme)
- [YouTube Data API v3](https://console.cloud.google.com/apis/api/youtube.googleapis.com/overview)
- [Setup Guide](references/setup.md)
- [Video Delete](references/video-delete.md)
- [Video GetRating](references/video-getRating.md)
- [Video Insert](references/video-insert.md)
- [Video List](references/video-list.md)
- [Video Rate](references/video-rate.md)
- [Video ReportAbuse](references/video-reportAbuse.md)
- [Video Update](references/video-update.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI flag tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local OAuth credential and token configuration required by yutu.]

## Skill Version(s):

0.10.7-dev (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
