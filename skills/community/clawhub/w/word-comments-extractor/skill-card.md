## Description:

Extract comments from Word documents and format them into standardized review opinions. Auto-matches page numbers, agent-powered semantic polishing. Designed for investment banking QC, legal review, and document audit scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomyan-zhang](https://clawhub.ai/user/tomyan-zhang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and document review teams use this skill to extract Word document comments, anchor text, and page numbers, then turn those comments into standardized review opinions for investment banking quality control, legal review, and document audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening and parsing untrusted DOCX files can expose users to unsafe document content or oversized archive behavior.

Mitigation: Use the extractor only on trusted documents or in an isolated environment until archive size and member validation are added.

Risk: The skill depends on Microsoft Word COM for page number lookup, so page data can be unavailable outside supported Windows and Word environments.

Mitigation: Run on Windows with Microsoft Word installed and review any comments whose page field is reported as unknown.

Risk: Agent-side polishing can change tone or omit nuance if the original comment and anchor text are ambiguous.

Mitigation: Review the generated opinion list against the extracted JSON before using it in a formal document review workflow.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Install in an isolated Python environment and pin pywin32 where operational reproducibility is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomyan-zhang/skills/word-comments-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown-formatted review opinion list, with JSON produced by the local extraction script as an intermediate input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes physical page numbers when Microsoft Word COM page lookup succeeds; page numbers may differ from displayed document numbering.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
