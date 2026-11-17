## Description:

Provides a JavaScript document-processing API that claims to parse, extract, summarize, analyze, classify, and convert common document formats, but the implementation evidence shows mocked outputs rather than real file parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders can use this skill as a document-processing interface for document parsing, information extraction, text analysis, summarization, classification, and conversion workflows. Review carefully before operational use because the security review identifies fabricated processing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill materially misrepresents document-processing results by returning fabricated content instead of reading files.

Mitigation: Do not use the skill for real contracts, reports, compliance documents, or decisions until the publisher replaces mocked outputs with real parsing and documents limits.

Risk: The security guidance identifies the implementation as mock or incomplete.

Mitigation: Review behavior in a controlled environment and require explicit documentation for file access, privacy handling, and conversion constraints before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/skills/smart-document-processing)
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [JavaScript objects, JSON-like results, Markdown examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns simulated document metadata, extracted text, tables, summaries, classifications, conversion status, and analysis objects.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
