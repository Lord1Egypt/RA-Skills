## Description:

Voice Reminder helps an agent place immediate or delayed outbound voice reminder calls for named contacts or phone numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn reminder requests into outbound voice call tasks, including delayed reminders expressed in natural language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place outbound calls through a third-party service.

Mitigation: Install and use it only where outbound calling is expected, authorized, and reviewed by the user before execution.

Risk: The artifact includes hardcoded phone numbers and service identifiers and stores call history locally.

Mitigation: Review and replace contact data and service identifiers before deployment, and handle local call history as sensitive personal data.

Risk: The delayed-call feature may allow crafted reminder text to execute shell commands under the agent account.

Mitigation: Fix the scheduling implementation before use by avoiding shell invocation with user-controlled text and using argument-list subprocess calls instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallkeyboy/skills/voice-reminder)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, API Calls]

**Output Format:** [JSON task status with optional shell command execution by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store local call history and initiate outbound calls through a third-party service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
