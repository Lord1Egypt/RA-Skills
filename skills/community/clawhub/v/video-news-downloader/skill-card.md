## Description:

Automated daily news video downloader with AI subtitle proofreading for CBS Evening News and BBC News at Ten, including subtitle extraction, DeepSeek proofreading task preparation, HTTP video serving, and scheduled cron updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyberpsychosissss](https://clawhub.ai/user/cyberpsychosissss)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to automate downloading daily CBS and BBC news videos, extract subtitles, prepare AI proofreading tasks, serve local web players, and schedule recurring updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded videos and subtitles may be exposed over the network when the HTTP servers bind to all interfaces.

Mitigation: Bind the HTTP server to 127.0.0.1 unless LAN access is intentional, and review exposed directories before starting the server.

Risk: Cron installation creates persistent scheduled jobs that run download and proofreading scripts automatically.

Mitigation: Inspect the proposed crontab entries before installation and run the skill as an unprivileged user.

Risk: Subtitle text sent to DeepSeek or another AI provider may disclose downloaded transcript content to a third party.

Mitigation: Treat subtitle proofreading as third-party data sharing and review transcript sensitivity before submitting text to an AI provider.

Risk: Unpinned tools and Python dependencies can change behavior across installs.

Mitigation: Pin dependencies in a virtual environment and review tool versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyberpsychosissss/skills/video-news-downloader)
- [Video News Downloader workflow](references/workflow.md)
- [Cron Job Setup Guide](references/cron-setup.md)
- [CBS Evening News YouTube playlist](https://www.youtube.com/playlist?list=PLotzEBRQdc0cMXjf4FKw6_1Pu8in6rzBQ)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python and shell scripts, cron configuration, local media files, WebVTT subtitles, proofreading task text, and correction reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or manages MP4 videos, VTT subtitle files, backup subtitles, AI proofreading prompt files, corrected subtitle text, correction reports, cron entries, logs, and HTTP player endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
