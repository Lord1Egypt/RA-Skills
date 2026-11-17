## Description:

Advanced AI voice assistant for phone calls. Capable of persuasion, sales, restaurant bookings, reminders, and notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmorillas99-cyber](https://clawhub.ai/user/cmorillas99-cyber)

### License/Terms of Use:

MIT

## Use Case:

External users and developers can use this skill to initiate authorized Vapi-powered phone calls for voice interaction tasks such as bookings, reminders, notifications, and sales workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place autonomous phone calls that may be inappropriate or unlawful without authorization, notice, or consent.

Mitigation: Use only for lawful, authorized calls where recipients have appropriate notice or consent, and review call missions before execution.

Risk: The skill exposes a local webhook publicly to receive real-time call updates.

Mitigation: Use a secured HTTPS tunnel only when needed, restrict access where possible, and avoid reusing or sharing webhook URLs unnecessarily.

Risk: Call transcripts and summaries may contain sensitive personal or business information.

Mitigation: Treat saved transcripts as sensitive data, restrict log access, and delete, redact, or retain them according to applicable policy.

Risk: Vapi calls may incur service charges and related data processing.

Mitigation: Confirm Vapi billing, phone number, assistant configuration, and expected call duration before use.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [JSON call results with transcript, summary, cost, duration, status, and optional log file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Vapi credentials, a configured assistant and phone number, and a reachable HTTPS webhook endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
