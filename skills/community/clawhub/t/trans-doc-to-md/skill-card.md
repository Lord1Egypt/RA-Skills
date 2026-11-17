## Description:

Convert PDFs, Lexiang document links, or prepared Markdown packages into faithful bilingual Markdown work packages that preserve source paragraphs, local image paths and order, rich document structure, and produce source.md, optional images/, meta.json, and a final Markdown file named from the original title.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajaxhe](https://clawhub.ai/user/ajaxhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document maintainers use this skill to convert PDFs, Lexiang documents, or prepared Markdown packages into bilingual Markdown work packages while preserving source text, images, metadata, and rich document structure. It also provides validation commands for checking paragraph and image preservation before optional publication through a separate uploader skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Lexiang fetch workflow handles credentials and private document contents.

Mitigation: Run it only in a trusted environment, use a narrowly scoped Lexiang token, and do not set MCP_BASE_URL to an untrusted host.

Risk: Optional Gemini translation can send document text to Google.

Mitigation: Use the Gemini path only when external processing of the document is acceptable; otherwise use the default local agent translation workflow.

Risk: The skill contains behavior that can persistently update its own lessons and guidance.

Mitigation: Require trusted maintainer review before self-updated guidance affects future runs.

## Reference(s):

- [Extraction: Text, Charts, Tables, and Cards](references/extraction.md)
- [Translation to Bilingual Markdown](references/translation.md)
- [Rich Element Recognition and Portable Expression](references/rich-elements.md)
- [Lessons Learned](references/lessons-learned.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, JSON, Shell commands, Configuration]

**Output Format:** [Markdown work package with source.md, optional images/, meta.json, validation JSON, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Final bilingual Markdown keeps source paragraphs and local image paths/order; optional Gemini translation requires GEMINI_API_KEY; optional publishing is delegated to upload-markdown-to-lexiang.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
