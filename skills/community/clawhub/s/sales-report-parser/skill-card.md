## Description:

Extracts sales data from report images using OCR, parses structured JSON through a MiniMax-compatible LLM API, and converts results to Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhoutianwang](https://clawhub.ai/user/zhoutianwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations teams use this skill to turn sales report images into structured JSON and Excel outputs for review, reporting, or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sales reports may contain confidential revenue, transaction, customer, or operational data.

Mitigation: Restrict input directories to intended files and review data-handling requirements before processing reports.

Risk: OCR and report contents can be sent to a third-party model endpoint through the MiniMax-compatible API configuration.

Mitigation: Use the MiniMax or custom base URL only when sending those contents to that provider is acceptable.

Risk: Command examples require API keys and can encourage exposing secrets directly in shell history.

Mitigation: Use a dedicated environment, avoid placing real API keys directly in shell commands, and pin and audit dependencies before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhoutianwang/skills/sales-report-parser)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with shell commands; generated JSON and Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain extracted business data from input sales reports.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
