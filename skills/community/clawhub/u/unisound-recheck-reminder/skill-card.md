## Description:

Generates a structured recheck reminder from a health exam report by identifying follow-up items, urgency windows, recommended exams, departments, venues, and preparation notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Health exam centers and health management organizations use this skill to turn report findings into a follow-up checklist and recipient-facing reminder. It supports post-exam recheck coordination, while final medical decisions remain with the receiving clinician.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health exam report contents are sent to a remote model endpoint.

Mitigation: Remove names, IDs, phone numbers, addresses, and other direct identifiers before use, and only process reports whose disclosure to the configured service is approved.

Risk: The documented de-identification posture is stronger than the artifact behavior.

Mitigation: Add or require local redaction before invoking the model, then verify the redaction path with representative reports before deployment.

Risk: The API base URL can be changed at runtime.

Mitigation: Restrict --base to an approved HTTPS endpoint for the exact app key and environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/unisound-recheck-reminder)
- [Publisher profile](https://clawhub.ai/user/unisound-llm)
- [Configured medical model endpoint](https://maas-api.hivoice.cn/v1/chat/completions)

## Skill Output:

**Output Type(s):** [text, JSON, files, guidance]

**Output Format:** [JSON followed by plain-language reminder text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print to stdout or write the combined output to a user-specified file path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
