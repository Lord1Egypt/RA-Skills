## Description:

Xiaohongshu (Little Red Book) comment scraper that reacts to Xiaohongshu profile URLs, scrapes comments from the profile's notes, saves local JSON files, and can generate an HTML analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liteli1987gmail](https://clawhub.ai/user/liteli1987gmail)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect Xiaohongshu note comments from a profile they provide, store per-note comment data locally, and optionally produce a local analysis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad authenticated browser automation against Xiaohongshu.

Mitigation: Use it only for profiles and comments the user is authorized to collect, and confirm the scraping scope before starting.

Risk: Generated JSON files and reports may contain personal or sensitive user-generated content.

Mitigation: Store outputs only where appropriate, restrict sharing, and delete generated files when they are no longer needed.

Risk: Generated HTML reports could expose users to unsafe rendering if untrusted comments are not escaped.

Mitigation: Avoid opening generated HTML reports from untrusted comment data unless the report generator safely escapes displayed content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liteli1987gmail/skills/xhs-comment)
- [Xiaohongshu profile URL pattern](https://www.xiaohongshu.com/user/profile/{userId})

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with browser actions, Python snippets, JSON output files, and optional local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one JSON file per note under the user's Downloads folder and may generate local analysis assets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
