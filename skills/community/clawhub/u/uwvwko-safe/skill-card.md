## Description:

Web browsing safety guard that identifies and blocks high-risk malicious instructions, sensitive information leakage, and unauthorized command execution while notifying the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to add browser-session safety checks that block requests for secrets, sensitive local information, destructive file operations, or unauthorized command execution and return a user-facing warning with suggested next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad override rules could allow users or web content to weaken protections for risky requests.

Mitigation: Require verified direct-user consent for overrides and do not allow overrides for secrets, destructive actions, or sensitive file access.

Risk: Logging and email reporting could retain or transmit sensitive security-event data.

Mitigation: Use redacted local-only logging by default and enable email reporting only when explicitly configured and protected.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or plain-text security warnings, notifications, and recommended actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk level, detected request, triggered rule, source URL, block status, and logging details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
