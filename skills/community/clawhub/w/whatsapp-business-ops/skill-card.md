## Description:

Guides agents through WhatsApp Business inbound replies, opted-in outbound templates, follow-ups, duplicate guards, and recap reporting while preserving quality score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbloch-ia](https://clawhub.ai/user/alexbloch-ia)

### License/Terms of Use:

MIT-0

## Use Case:

Business operations teams and agent operators use this skill to manage opted-in WhatsApp Business leads, answer inbound conversations within the 24-hour window, send approved follow-up templates, and hand qualified leads to humans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles lead names, phone numbers, case types, message timing, and local state that may contain personal data.

Mitigation: Operate it only for numbers and leads you control, keep consent records, scope the API token to one business number, restrict memory directory access, and apply the configured retention windows.

Risk: Outbound messaging can create duplicate sends, closed-window free-form replies, quality-score drops, or account pauses.

Mitigation: Use the 24-hour window checks, approved templates, phase gates, quota limits, duplicate registers, and stop-and-review behavior described by the artifact before sending.

Risk: Alert destinations may expose lead contact details beyond the local workspace.

Mitigation: Limit alert channels to approved staff and send only the minimal qualified-lead payload instead of conversation transcripts.

Risk: Legal, medical, or financial lead handling may require additional privacy review.

Mitigation: Avoid those use cases unless counsel, privacy, or DPO review confirms the workflow and retention settings are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexbloch-ia/skills/whatsapp-business-ops)
- [ClawHub homepage metadata](https://clawhub.ai/alexbloch-ia/whatsapp-business-ops)
- [Whatchimp API base URL](https://app.whatchimp.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML and bash examples plus fixed recap text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational procedures, configuration placeholders, local-state file conventions, API call examples, and mandatory run recaps.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
