## Description:

Convert trusted web pages and web-based slide decks into multi-page PDF files using a headless browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pearyj](https://clawhub.ai/user/pearyj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to convert trusted public webpages, articles, and web slide decks into PDF files for offline review, archiving, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security review marks this PDF-conversion skill as suspicious and recommends review before installation.

Mitigation: Review the skill before installing it and run it only in a sandbox or other low-trust environment.

Risk: The skill fetches user-supplied webpages with a headless browser and writes PDFs from captured page content.

Mitigation: Use only trusted public URLs and verify the generated PDF before sharing or relying on it.

Risk: The server security guidance calls out unresolved concerns around shell invocation, URL restrictions, temporary-file handling, and dependency pinning.

Mitigation: Use simple user-chosen output filenames, keep dependency installation isolated, and avoid high-trust environments until those issues are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pearyj/skills/webpage-to-pdf)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown status text with shell commands and a generated PDF file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports output path, file details, and verification notes when available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
