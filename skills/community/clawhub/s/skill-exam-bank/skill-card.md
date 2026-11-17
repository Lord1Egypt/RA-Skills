## Description:

Converts exam PDFs or images into a 17-column question-bank Excel workflow using OCR, agent-assisted extraction, validation, and optional archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beek5996admin](https://clawhub.ai/user/beek5996admin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and developers use this skill to transform exam papers into structured question-bank records and Excel files for review or import. It supports OCR parsing, JSON extraction, missing-question checks, Excel writing, and optional local or network archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Complete exam documents and extracted question-bank content can be sent to configured OCR services and, in the one-command path, to DeepSeek.

Mitigation: Use only trusted OCR endpoints, prefer HTTPS or an isolated internal service, and run the DeepSeek-backed path only when sending OCR text to that provider is acceptable.

Risk: Generated Excel, OCR, JSON, and check-report files may contain confidential or restricted exam material.

Mitigation: Archive outputs only to approved local or controlled storage locations, and avoid shared or cloud-synced folders for sensitive exams.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beek5996admin/skills/skill-exam-bank)
- [Publisher profile](https://clawhub.ai/user/beek5996admin)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown OCR output, JSON records, Excel files, validation reports, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a fixed 17-column question-bank schema and may optionally archive generated artifacts when a destination is configured.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
