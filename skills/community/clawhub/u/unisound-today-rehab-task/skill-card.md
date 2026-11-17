## Description:

Provides a daily postoperative rehabilitation task workflow that filters an existing rehabilitation plan by date, reports completion status, and generates patient-facing reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External healthcare or rehabilitation applications use this skill to present today's postoperative rehab tasks from an existing plan and record completed, skipped, or pending status. It is not intended to adjust training intensity or create a new rehabilitation plan.

### Deployment Geography for Use:

Global, subject to local medical-data privacy, compliance, and data-residency review.

## Known Risks and Mitigations:

Risk: The skill may process sensitive rehabilitation or patient task data and send selected task data to a fixed external medical-model API.

Mitigation: Use only when that external processing is acceptable for privacy, compliance, and data-residency requirements; prefer structured JSON inputs with the minimum necessary data.

Risk: Broad document and image input support can expose document conversion or OCR paths to untrusted patient files.

Mitigation: Sandbox PDF, office-document, and OCR preprocessing, and restrict accepted file types when JSON input is sufficient.

Risk: The command-line appkey parameter can expose credentials through shell history or process listings.

Mitigation: Use platform-managed secrets or a wrapper that avoids placing real API keys directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-today-rehab-task)
- [CareKit daily tasks and scheduling reference](https://github.com/carekit-apple/CareKit)
- [Hivoice medical model API endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [UTF-8 JSON with structured task data and a Markdown reminder in the text field]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Filters tasks by date, summarizes completion counts, and uses an external medical-model API when generating reminders for scheduled tasks.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact _meta.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
