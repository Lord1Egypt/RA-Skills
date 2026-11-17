## Description:

A cybersecurity intelligence crawler that collects security community RSS articles hourly, gathers daily CVE intelligence, translates English vulnerability descriptions into Chinese, and writes daily IMA notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fallenqu](https://clawhub.ai/user/fallenqu)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers use this skill to collect daily security news and vulnerability intelligence from configured feeds and APIs, deduplicate items, and publish Chinese daily notes in IMA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports unsafe credential practices around IMA note-write credentials and MiniMax credentials.

Mitigation: Use dedicated limited-scope credentials, avoid hardcoded secrets, and remove the global openclaw.json credential fallback before deployment.

Risk: The security review reports scheduled-operation risk, including system-wide cron execution.

Mitigation: Run it under a controlled user-level schedule and do not use the system-wide cron command unless it has been reviewed and approved.

Risk: The security review reports transport risk for feed collection.

Mitigation: Require TLS verification for all feeds before relying on collected intelligence.

Risk: The skill needs network access, local state files, logs, and credentials capable of writing IMA notes.

Mitigation: Install only in an environment where those permissions are expected, monitored, and scoped to this crawler's notebooks.

## Reference(s):

- [RSS source status reference](references/rss-sources.md)
- [ClawHub skill page](https://clawhub.ai/fallenqu/skills/sec-news-crawler)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown notes with inline source links and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily security-news and vulnerability-intelligence notes to IMA and maintains local state and log files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
