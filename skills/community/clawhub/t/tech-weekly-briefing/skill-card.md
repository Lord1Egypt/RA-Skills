## Description:

Generates weekly technology news briefings by fetching major English-language technology RSS feeds, filtering and deduplicating articles, grouping multi-source stories, and organizing results by company and autonomous-driving coverage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to collect technology news from configured RSS feeds and produce a weekly briefing with hot stories, source links, autonomous-driving coverage, and company-focused navigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron jobs can keep fetching feeds and generating reports after installation.

Mitigation: Add cron entries only after review, keep a record of the installed entries, and remove or disable them when scheduled briefings are no longer needed.

Risk: The skill performs outbound RSS requests and stores local article snapshots, reports, and logs.

Mitigation: Review the configured feed list and local storage paths before use, and apply normal retention controls for generated data under the skill data directory and /tmp.

Risk: The generated briefing may be Chinese-oriented even when a different preferred language is expected.

Mitigation: Confirm the output language requirements before relying on the briefing, and adjust the report generation prompt or script behavior if a different language is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangzhe1991/skills/tech-weekly-briefing)
- [Publisher profile](https://clawhub.ai/user/yangzhe1991)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml)
- [Wired RSS feed](https://www.wired.com/feed/rss)
- [Ars Technica RSS feed](https://arstechnica.com/feed/)
- [MIT Technology Review RSS feed](https://www.technologyreview.com/feed/)
- [The Information RSS feed](https://www.theinformation.com/feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style briefing with source links, command guidance, and JSON article snapshots.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly reports are written to /tmp, article and company snapshots are stored as JSON under the skill data directory, and cron setup can create recurring fetch/report runs.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact version history agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
