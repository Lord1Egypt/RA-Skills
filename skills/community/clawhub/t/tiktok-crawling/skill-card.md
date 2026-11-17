## Description:

Use for TikTok crawling, content retrieval, and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romneyda](https://clawhub.ai/user/romneyda)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to retrieve TikTok videos and metadata with yt-dlp, export JSON or CSV data, and analyze creator, hashtag, search, or sound results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated TikTok access may expose browser session cookies or account data.

Mitigation: Prefer public-only scraping, avoid using a main Chrome profile, and keep cookie files out of shared or version-controlled folders.

Risk: Unattended scheduled scraping can continue running without enough monitoring or cleanup.

Mitigation: Do not enable the cron job unless the operator understands how to monitor logs, adjust cadence, and remove the schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romneyda/skills/tiktok-crawling)
- [yt-dlp supported sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
- [yt-dlp output template reference](https://github.com/yt-dlp/yt-dlp#output-template)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include yt-dlp commands that download media, write metadata files, use browser cookies, or run unattended cron jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
