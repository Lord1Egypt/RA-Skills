## Description:

Tracks post-operative rehabilitation progress for patient-facing use by analyzing task completion records, pain scores, functional self-assessments, and phase progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External patient-facing care teams and developers use this skill to summarize rehabilitation task completion, pain trends, functional trends, phase progress, and items needing attention for post-operative recovery tracking. It supports record summarization and progress visualization, not treatment-effect diagnosis or replacement of a rehabilitation professional's assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive rehabilitation records are sent to the disclosed hivoice medical-model API.

Mitigation: Avoid patient identifiers and unnecessary free text, provide the minimum JSON fields needed for progress analysis, and confirm external API handling requirements before use.

Risk: The API credential is accepted as a command-line argument.

Mitigation: Provide credentials through a secret manager or controlled runtime injection and avoid exposing keys in shell history, logs, or shared scripts.

Risk: Document conversion and OCR for untrusted files can process complex external content.

Mitigation: Run preprocessing for PDFs, office documents, and images in a sandbox and keep optional parsers and external tools patched.

Risk: Generated rehabilitation commentary could be mistaken for a clinical assessment.

Mitigation: Use the output for record summaries and trend display only, and require rehabilitation professional review for treatment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-rehab-progress-tracking)
- [Referenced rehabilitation-analyzer progress analysis source](https://agent-skills.md/skills/huifer/WellAlly-health/rehabilitation-analyzer)
- [Disclosed hivoice medical-model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Files]

**Output Format:** [UTF-8 JSON containing structured trend data and Markdown narrative text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write an output JSON file and, when requested, a prepared JSON input artifact for debugging.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
