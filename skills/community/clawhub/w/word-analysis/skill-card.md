## Description:

Analyzes standard DOCX documents for summaries, questions, and comparisons with verifiable paragraph evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

People working with Word documents use this skill to summarize, ask questions about, or compare two to three DOCX files while tracing claims to their source paragraphs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted document text is sent to the AI Skills platform, even though the original DOCX stays local.

Mitigation: Confirm platform processing is acceptable before using sensitive documents.

Risk: A shared platform API key can grant access across enabled skills.

Mitigation: Use the product-specific WORD_ANALYSIS_API_KEY when tighter separation is needed; do not expose keys in conversation or logs.

## Reference(s):

- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/word-analysis/API-KEY.md)
- [Local Word extraction](https://ai-skills.open-idea.net/skill-docs/word-analysis/LOCAL-EXTRACTION.md)
- [HTTP requests](https://ai-skills.open-idea.net/skill-docs/word-analysis/HTTP-REQUESTS.md)
- [Word analysis operations](https://ai-skills.open-idea.net/skill-docs/word-analysis/OPERATIONS.md)
- [Evidence and safety rules](https://ai-skills.open-idea.net/skill-docs/word-analysis/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Paragraph-grounded answers and summaries; optional Markdown and JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports comparisons of two to three DOCX files; does not extract text from images.]

## Skill Version(s):

1.2.0 (source: frontmatter metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
