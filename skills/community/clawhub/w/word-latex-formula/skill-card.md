## Description:

Converts manually typed formulas in Word documents (.doc, .docx, .wps) into editable Word equations while preserving layout through local Microsoft Word or LibreOffice conversion and direct OOXML edits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianyedavid](https://clawhub.ai/user/tianyedavid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and document-preparation teams use this skill to convert academic manuscripts or batches of Word documents from typed formula text into editable Word equations, with optional staged review or AI-assisted classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local web UI exposes and rewrites AI API keys through unauthenticated browser-accessible endpoints.

Mitigation: Prefer the CLI rule-based workflow for sensitive manuscripts, avoid entering real AI API keys into the web UI until the web API issues are fixed, and rotate any key already used with this web service.

Risk: Optional AI review may send formula candidates and nearby text snippets to a configured model endpoint.

Mitigation: Use local rule-based conversion or a self-hosted model endpoint for sensitive manuscripts, and disclose the candidate-text sharing before enabling AI review.

## Reference(s):

- [Security and Privacy Notes](references/SECURITY_AND_PRIVACY.md)
- [Usage Reference](references/USAGE.md)
- [ClawHub Skill Page](https://clawhub.ai/tianyedavid/skills/word-latex-formula)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command blocks and local output file paths when conversion workflows are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled workflows can produce .docx outputs, Word review documents, candidate or decision JSON files, and conversion reports.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
