## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to extract Markdown content from Word documents, PowerPoint presentations, and Excel spreadsheets supplied as local files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external MinerU CLI distribution.

Mitigation: Install only from a trusted distribution path and review the installed CLI before use in managed environments.

Risk: The documented flash extraction path uploads documents to MinerU's cloud API for processing.

Mitigation: Use it only with documents suitable for cloud processing; for sensitive business, legal, or personal files, prefer an isolated environment or a local processing alternative.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)
- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/word-to-markdown)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Document conversion output is Markdown; embedded images may be replaced with placeholders, and flash extraction is documented for files up to 10MB or 20 pages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
