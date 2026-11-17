## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and other external users use this skill to extract content from Word, PowerPoint, and Excel documents into Markdown for review, summarization, analysis, or reuse.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to MinerU's cloud API for processing, which may expose confidential content to an external service.

Mitigation: Use only with documents appropriate for third-party cloud processing, review MinerU privacy terms before handling sensitive material, and prefer a pinned or reviewed CLI version.

Risk: The basic extraction path has documented file size and page limits.

Mitigation: Keep basic extraction inputs within the 10 MB or 20 page limit, or use the authenticated extraction workflow only after confirming its terms and requirements.

## Reference(s):

- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)
- [ClawHub Skill Page](https://clawhub.ai/tanis90/skills/slides-to-markdown)
- [Publisher Profile](https://clawhub.ai/user/tanis90)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs converted document text, tables, and document structure; embedded images may be replaced with placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
