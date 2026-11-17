## Description:

Silver Daily generates a same-day silver economy news brief covering policy, consumption, finance, technology, health care, culture, home-based elder care, and senior employment, with links, summaries, and an HTML daily report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnspica](https://clawhub.ai/user/cnspica)

### License/Terms of Use:

MIT-0

## Use Case:

External readers, researchers, investors, product teams, and elder-care industry practitioners use this skill to collect current silver economy news and turn it into a concise daily HTML briefing. It is not intended for personal pension account lookup, medical diagnosis, or specific stock investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include active browser content when report data or news fields are untrusted.

Mitigation: Escape text fields, validate URLs to http/https, and add safer external-link attributes before sharing or hosting generated reports.

Risk: Real web results or user-supplied JSON can introduce misleading sources, unsafe links, or unsuitable content into a distributed daily report.

Mitigation: Review selected stories, sources, summaries, and links before publishing, especially when reports are shared externally or hosted online.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnspica/skills/silver-daily)
- [Content framework](artifact/references/content_framework.md)
- [HTML output template](artifact/references/html_template.md)
- [Output format](artifact/references/output_format.md)

## Skill Output:

**Output Type(s):** [text, html, files, shell commands, guidance]

**Output Format:** [HTML report file plus a concise text completion summary with the generated file path and headline details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is output/silver-daily-YYYYMMDD.html; optional JSON input can provide report data to the generator script.]

## Skill Version(s):

1.0.1 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
