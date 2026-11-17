## Description:

Use when monitoring websites for content changes, comparing page snapshots with diff, scheduling periodic checks, or sending alerts via email and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site operators, and external users can use this skill to monitor web pages, compare snapshots, schedule checks, and receive change alerts. It is suited to page text, price, stock, status, and reporting workflows where local logs and snapshots are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release has a suspicious security verdict due to unsafe persistent cron and configuration handling.

Mitigation: Review carefully before installing and do not use scheduling until cron construction and shell-sourced configuration are fixed.

Risk: Website monitoring can expose sensitive URLs, query strings, tokens, or notification destinations.

Mitigation: Use only trusted URLs and notification targets, and avoid sensitive query strings or tokens.

Risk: Notification setup may send monitored content or metadata to external email or webhook services.

Mitigation: Do not use notify features until the unsafe configuration handling is fixed and destinations are reviewed.

Risk: The package stores snapshots, configuration, and logs under the home directory, and includes a nested logger that records arbitrary inputs locally.

Mitigation: Run in a controlled environment, review local data retention, and avoid submitting secrets or private content as inputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bytesagain3/skills/site-change-alert)
- [Publisher Profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Command-line text, diffs, local snapshot files, logs, and notification setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write watch lists, snapshots, configuration, logs, and exports under the user's home directory.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
