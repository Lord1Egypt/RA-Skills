## Description:

Complete Ryot media tracker with progress tracking, reviews, collections, analytics, calendar, and automated daily/weekly reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[f-liva](https://clawhub.ai/user/f-liva)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to manage a self-hosted Ryot media tracker from an agent, including search, progress updates, reviews, collections, analytics, calendars, and optional reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Ryot API token stored in /home/node/clawd/config/ryot.json.

Mitigation: Use a trusted HTTPS Ryot URL, restrict file permissions on the config file, and rotate the token if it may have been exposed.

Risk: Completion, review, collection, and bulk episode commands can modify Ryot account data.

Mitigation: Search first, verify the metadata ID and title details, and confirm the intended change before running write operations.

Risk: Optional cron and WhatsApp automation can continue sending report output after setup.

Mitigation: Review the scheduled jobs before enabling them, use dry-run mode when available, and remove jobs that are no longer needed.

## Reference(s):

- [ClawHub Ryot skill page](https://clawhub.ai/f-liva/skills/ryot)
- [Publisher profile](https://clawhub.ai/user/f-liva)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke Ryot API operations and optional scheduled notification setup when the user provides credentials and confirms changes.]

## Skill Version(s):

1.2.0 (source: package.json, CHANGELOG, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
