## Description:

Generates Chinese bid proposal drafts from tender documents by extracting requirements, organizing standard bid sections, and producing editable Word-oriented content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengcheng8632](https://clawhub.ai/user/chengcheng8632)

### License/Terms of Use:

MIT-0

## Use Case:

External proposal, procurement, and business development users use this skill to parse Chinese tender documents and draft bid responses with project details, qualification requirements, technical specifications, commercial terms, scoring criteria, and standard bid sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated bid content may contain incorrect qualifications, pricing, legal commitments, deadlines, or tender responses.

Mitigation: Manually review all generated bid content against the source tender, company records, pricing approvals, and legal requirements before submission.

Risk: Tender parsing reads user-provided PDF, DOCX, or TXT files and may handle sensitive procurement or company information.

Mitigation: Run the skill locally on files the user explicitly provides and avoid processing confidential tenders in unapproved environments.

Risk: Generic dependency installation prompts could install unpinned document parsing packages into a shared environment.

Mitigation: Install PyPDF2 and python-docx in a dedicated virtual environment with pinned versions before running the scripts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chengcheng8632/skills/tender-bid-generator)
- [Publisher Profile](https://clawhub.ai/user/chengcheng8632)
- [Writing Guide](references/writing-guide.md)
- [Bid Template](assets/bid-template.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON tender extraction output, and editable bid document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided PDF, DOCX, or TXT tender files locally and relies on manual review before bid submission.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
