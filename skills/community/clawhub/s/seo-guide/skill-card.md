## Description:

Lesishu SEO Guide helps agents provide SEO guidance for site diagnosis, on-page optimization, technical SEO, content strategy, keyword research, structured data, local SEO, link building, and optional PDF reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lesishu](https://clawhub.ai/user/lesishu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, content teams, and developers use this skill to plan, diagnose, and improve SEO workflows using bundled Google, Moz, Ahrefs, and local reference material. The skill can also guide optional local generation of SEO audit PDF reports when explicitly requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SEO recommendations may be inaccurate, outdated, or misleading if applied without checking the target site and current search guidance.

Mitigation: Review recommendations against the bundled official references and the site's current data before implementation.

Risk: PDF report generation requires a local dependency and writes a local output file.

Mitigation: Install ReportLab in a virtual environment and generate PDFs only when the user explicitly requests a report.

Risk: SEO audits, outreach, email collection, or third-party domain inspection can create privacy, platform, authorization, or anti-spam concerns.

Mitigation: Inspect only authorized domains and do not collect emails or send outreach unless the user has authorization and complies with applicable rules.

## Reference(s):

- [SEO Guide Skill Source](artifact/SKILL.md)
- [Google Search Central Reference Index](artifact/references-google/INDEX.md)
- [Moz Beginner's Guide Reference Index](artifact/references-moz/INDEX.md)
- [Ahrefs Academy Reference Index](artifact/references-ahrefs/INDEX.md)
- [SEO Diagnostic PDF Report Instructions](artifact/scripts/README.md)
- [Ahrefs Content Marketing Course](https://ahrefs.com/academy/content-marketing-course)
- [Ahrefs Digital Marketing Course](https://ahrefs.com/academy/digital-marketing-course)
- [Ahrefs Video Marketing Course](https://ahrefs.com/academy/video-marketing-course)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files]

**Output Format:** [Markdown guidance with optional Python or shell command snippets and optional PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [PDF report generation is optional, local, and should run only when explicitly requested; ReportLab may be installed in a virtual environment.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
