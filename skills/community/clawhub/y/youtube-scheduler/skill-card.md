## Description:

Analyzes a YouTube channel's upload history to identify high-performing posting days and hourly windows based on views and engagement signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, channel operators, and agents supporting content planning use this skill to analyze recent YouTube videos for statistically stronger posting times. It produces a local schedule report with best weekdays, best hourly windows, a day-by-time heatmap, top videos, and a recommended posting slot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence marks the release suspicious because the documented install commands pull executable agent files from an unpinned GitHub main branch.

Mitigation: Review the exact downloaded files before installing and prefer a reviewed release package or pinned commit instead of main-branch download commands.

Risk: The analyzer processes user-provided YouTube channel URLs through a local command-line downloader.

Mitigation: Run it only on trusted channel URLs and in an environment where invoking yt-dlp on external media URLs is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/youtube-scheduler)
- [Publisher profile](https://clawhub.ai/user/mcbaivn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and a local Markdown-style text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under Youtube_Schedule/[Channel]_schedule_DD_MM_YYYY.txt; results are statistical estimates from recent channel history, not guaranteed outcomes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
