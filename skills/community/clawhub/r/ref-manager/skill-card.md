## Description:

Ref Manager collects bibliographic metadata from web pages, PDF files, folders of PDFs, or raw APA text, verifies DOI-backed records against Crossref, and generates EndNote import files plus an APA reconciliation workbook.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangmingqi2005-create](https://clawhub.ai/user/fangmingqi2005-create)

### License/Terms of Use:

MIT-0

## Use Case:

External users, researchers, students, and developers use this skill to turn URLs, PDFs, folders of PDFs, or raw APA strings into citation records for EndNote import and APA review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch supplied web URLs from the agent runtime.

Mitigation: Use trusted URLs, avoid sensitive networks, and add URL validation before broader deployment.

Risk: The Excel export is reported as unsanitized.

Mitigation: Review generated workbooks before opening them in high-trust environments, and add formula escaping for user-derived cell values.

Risk: The skill reads the PDFs and folders provided by the user and contacts Crossref for DOI verification.

Mitigation: Avoid sensitive documents when external DOI lookup is not acceptable, or run only on approved copies of the source files.

Risk: Dependencies are specified with lower bounds instead of pinned versions.

Mitigation: Pin and review dependency versions for repeatable installations.

## Reference(s):

- [APA 7th Edition Citation Rules](references/apa-7-rules.md)
- [Crossref API Reference](references/crossref-api.md)
- [EndNote Import Guide](references/endnote-import-guide.md)

## Skill Output:

**Output Type(s):** [text, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands; generated RIS, EndNote XML, XLSX, and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Primary deliverables are references.ris, references.xml, an Excel reconciliation workbook, and refs.json in the selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
