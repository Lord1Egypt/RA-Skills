## Description:

Fix garbled text in PDF/SVG vector graphics caused by font encoding issues, making files editable in AI tools. Supports batch processing and JSON export for manual correction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-repair workflows use this skill to analyze PDF or SVG vector files with garbled text, run local repair commands, and export editable JSON for manual correction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install dependencies are ambiguous.

Mitigation: Review requirements before installation and replace ambiguous packages with pinned canonical packages such as PyMuPDF and beautifulsoup4.

Risk: The repair command can report success without creating repaired PDF or SVG files.

Mitigation: Verify that expected output files were created and inspect the repair report before treating the run as successful.

Risk: JSON exports can contain extracted document text and file paths.

Mitigation: Handle exported JSON as sensitive data and limit sharing to approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/vector-text-fixer-1)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report repaired, skipped, and unresolved text blocks with confidence values and manual review recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
