## Description:

Translate books (PDF/DOCX/EPUB) into any language using parallel sub-agents. Converts input -> Markdown chunks -> translated chunks -> HTML/DOCX/EPUB/PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deusyu](https://clawhub.ai/user/deusyu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate long-form books from PDF, DOCX, or EPUB into another language while preserving structure and producing publishable document and ebook outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted book content is processed by broadly empowered sub-agents and may be carried into generated HTML.

Mitigation: Use a reviewed release, run translations in a dedicated workspace, avoid confidential books unless policy permits, and treat generated book.html files as potentially unsafe when the source book is untrusted.

Risk: Existing temp manifests, glossaries, and translated chunks can influence merge and build results on resumed runs.

Mitigation: Review temporary manifests and glossaries before merging outputs from directories you did not create, and start from a fresh temp directory when prior state is not trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deusyu/skills/translate-book)
- [Declared project homepage](https://github.com/deusyu/translate-book)
- [Calibre](https://calibre-ebook.com/)
- [Pandoc](https://pandoc.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown chunks, JSON glossary and metadata files, plus generated HTML, DOCX, EPUB, and PDF book files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a resumable chunk pipeline with manifest validation; final outputs are written under a book-specific temporary directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
