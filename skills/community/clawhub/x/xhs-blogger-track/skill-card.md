## Description:

Searches public Xiaohongshu notes, retrieves note details and comments, and collects public creator posts as structured data for trend research, competitor analysis, KOL screening, and comment insight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, marketers, data analysts, and agents use this skill to collect public Xiaohongshu search results, note details, comments, and creator post lists before summarizing trends, comparing competitors, screening KOLs, or preparing reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Xiaohongshu keywords, target URLs, and the GUAIKEI_API_TOKEN to the Guaikei service.

Mitigation: Install only if that data sharing is acceptable, use a scoped or disposable token when possible, and monitor quota use.

Risk: Generated logs may contain research targets, comments, author data, and xsec_token URLs.

Mitigation: Protect or delete generated logs after use and avoid sharing them outside the intended team.

Risk: The skill is intended for public Xiaohongshu data and does not support private, hidden, logged-in, or non-public content.

Mitigation: Use only public keywords, public note URLs, and public creator profile URLs; decline requests for private or restricted data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/xhs-blogger-track)
- [Guaikei service](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Structured JSON command output, optional Markdown summaries, shell commands, and saved JSON log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; command results may be saved under logs/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package metadata report 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
