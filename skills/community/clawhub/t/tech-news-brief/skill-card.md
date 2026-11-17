## Description:

Discovers recent AI, large-model, semiconductor, and frontier-technology news, then produces Chinese summaries, Markdown source files, DOCX reports, ZIP archives, and optional email delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scienlot](https://clawhub.ai/user/scienlot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to compile recent technology news into Chinese daily briefings. It supports article discovery, source capture, summary drafting, DOCX conversion, ZIP packaging, and email delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send generated report archives by email using stored SMTP credentials.

Mitigation: Use a dedicated SMTP account or app password, confirm the recipient before use, and avoid passing passwords on the command line.

Risk: The workflow can download external news pages and write generated report files.

Mitigation: Constrain report and download output paths, review generated files before delivery, and keep fallback download credentials scoped.

Risk: The artifact intentionally applies a Chinese and China-focused editorial framing.

Mitigation: Use it only where that editorial posture is appropriate and review generated summaries for factual accuracy and neutrality requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scienlot/skills/tech-news-brief)
- [ClawHub publisher profile](https://clawhub.ai/user/scienlot)
- [Recommended news sources](artifact/references/sources.md)
- [Summary writing guide](artifact/references/writing-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, DOCX files, Shell commands, Configuration guidance]

**Output Format:** [Chinese Markdown reports, DOCX documents, ZIP archives, and email status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SMTP environment variables for email delivery and may use Firecrawl as a fallback content-download path.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
