## Description:

Generate daily vulnerability briefings from NIST NVD, CISA KEV, and security advisories. Aggregates, scores, and formats CVE data into actionable reports. No API key needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urianpaul94](https://clawhub.ai/user/urianpaul94)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts, developers, and operations teams use this skill to fetch public vulnerability feed data and generate concise daily CVE and CISA briefing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The diagnostics step writes to C:\Temp\clawhub_skills.txt and includes the local hostname in generated reports.

Mitigation: Make diagnostics explicit opt-in, document the file write, and omit host-identifying details unless the user requests them.

Risk: Briefings can be incomplete or misleading if public feeds are unavailable, rate-limited, or not checked against primary vendor advisories.

Mitigation: Respect the documented rate limits, retry transient feed errors, and verify critical findings against primary vendor advisories before acting.

## Reference(s):

- [Feed API Reference](references/feeds.md)
- [CVE Program](https://cve.mitre.org)
- [Feed Monitor API](https://feed-monitor.security-feeds.workers.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown briefing with tables and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public vulnerability feeds; summaries are intended to stay concise unless the user requests detail.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
