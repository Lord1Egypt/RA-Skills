## Description:

Monitor job postings, admissions, courses, and research opportunities from Scuola Superiore Sant'Anna di Pisa.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fabiobaroni](https://clawhub.ai/user/fabiobaroni)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to monitor public Scuola Superiore Sant'Anna di Pisa pages for job postings, admissions deadlines, PhD calls, Seasonal School courses, and related research or education opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring monitoring can cause an agent to periodically visit the listed public Sant'Anna Pisa pages and retain enough prior-result state to report changes.

Mitigation: Review the scheduled-monitoring setup and any stored prior-result state before enabling recurring runs.

Risk: The skill relies on public web pages whose deadlines, PDFs, yearly URLs, and course pages can change.

Mitigation: Compare results against the current public pages during each run and prefer stable hub pages when specific yearly links change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fabiobaroni/skills/santanna-pisa-monitor-skill)
- [Project homepage](https://github.com/FabioBaroni/santanna-pisa-monitor-skill)
- [Scuola Superiore Sant'Anna website](https://www.santannapisa.it/it)
- [Sant'Anna application portal](https://sssup.esse3.cineca.it/Home.do)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summaries and browser-navigation instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Standardized monitoring reports; no API keys, local binaries, or external dependencies required.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
