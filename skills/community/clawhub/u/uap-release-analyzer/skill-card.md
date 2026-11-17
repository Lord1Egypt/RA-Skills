## Description:

Analyze declassified UAP/UFO/FOIA PDF releases and generate inventory, text extraction analytics, redaction/entity summaries, and an 11-section report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and analysts use this skill to process folders of declassified UAP, UFO, and FOIA documents into an auditable inventory, extraction analytics, redaction/entity summaries, and a standardized report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the bundled scripts against a broad or unintended folder may process more local documents than intended.

Mitigation: Install and run the skill only on release folders the user chooses, preferably in a dedicated workspace.

Risk: Dependency versions may change if installed without pins, which can affect reproducibility.

Mitigation: Use a dedicated virtual environment and review or pin pdfplumber and pypdf versions for repeatable runs.

Risk: Persistent edits to agency vocabulary or scripts can change future analysis behavior.

Mitigation: Review and approve vocabulary or script changes before letting an agent persist them.

Risk: Scanned PDFs and image files can leave content-level gaps because the default workflow does not run OCR or vision analysis.

Mitigation: Review the report caveats and run OCR or vision analysis only as an explicit follow-up when needed.

## Reference(s):

- [UAP Release Analyzer on ClawHub](https://clawhub.ai/harrylabsj/skills/uap-release-analyzer)
- [OpenClaw Usage Notes](references/openclaw_usage.md)
- [Agency Filename Vocabulary](references/agency_vocab.md)
- [FOIA Exemptions and Classification Markers](references/foia_codes.md)
- [war.gov/UFO PURSUE Page Quirks](references/war_gov_quirks.md)
- [war.gov UFO Source Page](https://www.war.gov/UFO/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, CSV files, JSON analytics, text extracts, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local analysis outputs under the user-selected release directory, including inventory.csv, text extracts, analytics files, and REPORT.md.]

## Skill Version(s):

1.0.1 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
