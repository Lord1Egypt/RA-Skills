## Description:

Helps authorized Vanderbilt students use OneVU sessions, academic records, GPA projections, degree and schedule planning, and Microsoft Graph through a separately installed toolkit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goatinahat](https://clawhub.ai/user/goatinahat)

### License/Terms of Use:

MIT-0

## Use Case:

Authorized Vanderbilt students and their agents use the skill to access their own university and Microsoft accounts, check academic records, explore grades and degree requirements, and plan schedules. The toolkit runtime must be installed separately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: University and Microsoft sessions can expose sensitive account data or usable authentication material.

Mitigation: Use only the account holder's authorized account and a trusted runtime; keep passwords, passkeys, cookies, and tokens in the host vault and out of chat and logs.

Risk: Microsoft Graph write actions can change real mailbox or calendar data.

Mitigation: Default to the smallest read needed and obtain the account holder's approval before POST, PATCH, PUT, or DELETE actions.

Risk: Passkey enrollment or recovery changes account authentication, and cached sessions do not prove a passkey works.

Mitigation: Require explicit account-holder confirmation for enrollment or recovery, verify the signed-in identity, and report partial setup or unverified access accurately.

## Reference(s):

- [vutoolkit source installation guide](https://github.com/GoatInAHat/vutoolkit#quick-start-from-source)
- [vutoolkit feature acceptance record](https://github.com/GoatInAHat/vutoolkit/blob/main/docs/ACCEPTANCE.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with tool calls and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a separately installed toolkit and the account holder's authorization; this skill does not supply credentials or a runtime.]

## Skill Version(s):

0.4.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
