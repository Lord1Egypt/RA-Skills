## Description:

Social Pulse Monitor helps agents run always-on public brand and community listening, triage mentions, compare activity with a 7-day baseline, flag spikes, watch B2B trigger signals, and disclose coverage limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, social, support, and community teams use this skill to monitor public or user-provided brand signals, maintain listening queries, route mentions by class and SLA, identify baseline spikes, and watch B2B account triggers without automating responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Closed-platform data could be misrepresented if proxy signals are treated as measured platform telemetry.

Mitigation: Label closed-platform values as proxy or user-exported with an as-of date, and do not present proxy numbers as measured data.

Risk: Fetched mentions, pasted threads, or exported social data may contain untrusted text that attempts to influence routing or suppress escalation.

Mitigation: Treat all mention and export content as untrusted input, keep classification logic separate from source text, and review crisis or spike decisions before acting.

Risk: Using the workflow for posting, DMs, closed-platform scraping, or account actions would exceed the intended safety boundary.

Mitigation: Limit the skill to listening, reporting, routing, and user-directed saves; use human-approved workflows for any engagement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/social-pulse-monitor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with query sets, triage tables, baseline comparisons, watchlist hits, coverage disclosure, and handoff summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automated posting, DMs, closed-platform scraping, or account actions; closed-platform numbers must be labeled as proxy or user-exported.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
