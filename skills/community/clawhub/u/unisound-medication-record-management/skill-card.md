## Description:

Helps patients manage long-term medication records by organizing medication lists, dose history, active and stopped medications, and history summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Patients and care-support users use this skill to maintain personal medication lists and review dose history, active medications, stopped medications, and summary counts. Developers can integrate it into OpenClaw workflows that need structured medication-record management without prescription review or treatment-plan adjustment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medication names, doses, dates, statuses, and notes are sent to a mandatory external model service.

Mitigation: Use the skill only with appropriate consent and data-handling approval, minimize submitted data, and avoid real patient data unless the external service is approved for that use.

Risk: Document, spreadsheet, PDF, and image preprocessing can expose the runtime to untrusted files and optional external tools.

Mitigation: Prefer JSON or trusted structured inputs, scan files before processing, and run the skill in a restricted environment when non-JSON inputs are necessary.

Risk: Security evidence reports an unsafe fallback that can execute code outside the reviewed package.

Mitigation: Remove, disable, or explicitly review the fallback path before deployment, and restrict filesystem access during execution.

Risk: The generated text may include medication guidance that users could mistake for clinical advice.

Mitigation: Present outputs as record-management summaries only and require clinical review for medication decisions, interactions, or treatment changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-medication-record-management)
- [MedTimer F-Droid package](https://f-droid.org/en/packages/com.futsch1.medtimer/)
- [HiVoice medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [UTF-8 JSON containing structured data and Markdown natural-language text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an app key for the external u2-med model service; JSON-only input has no third-party package requirement, while document, spreadsheet, PDF, and image inputs may require optional parsers or external tools.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
