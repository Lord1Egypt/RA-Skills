## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to extract readable Markdown from Word, PowerPoint, and Excel documents supplied as local files or URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents processed with flash-extract are uploaded to MinerU's cloud API.

Mitigation: Use the skill only for documents the user is comfortable sending to MinerU, and avoid sensitive or restricted files unless that transfer is approved.

Risk: The skill depends on installing and running the mineru-open-api CLI from package sources.

Mitigation: Prefer pinned or trusted installation sources and review the generated command before execution.

Risk: The converter may replace embedded images with placeholders or omit detail from larger documents.

Mitigation: Review the returned Markdown against the source document when completeness matters, and use authenticated precision extraction for larger files.

## Reference(s):

- [Xlsx To Markdown on ClawHub](https://clawhub.ai/tanis90/skills/xlsx-to-markdown)
- [MinerU](https://mineru.net)
- [MinerU CLI downloads](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports DOCX, PPTX, XLS, and XLSX inputs; flash extraction is limited to 10MB or 20 pages per document.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
