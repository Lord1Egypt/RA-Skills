## Description:

OTPly helps agents use ToolWeb's OTPLY API to register accounts, retrieve credentials, send and verify email one-time passwords, and review usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and integration agents use this skill to add email OTP flows for authentication, account recovery, transaction checks, and usage monitoring through the OTPLY service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles account passwords, API keys, API secrets, JWTs, OTPs, and email addresses.

Mitigation: Treat these values as sensitive credentials, avoid logging or pasting production secrets into casual prompts, and rotate exposed credentials.

Risk: Using the skill sends email addresses and OTP verification data to ToolWeb's OTPLY service.

Mitigation: Confirm that ToolWeb is acceptable for the application's email verification flow and applicable data handling requirements before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-otply)
- [OTPLY API Docs](https://api.toolweb.in:8168/docs)
- [OTPLY Kong Route](https://api.toolweb.in/tools/otply)
- [ToolWeb](https://toolweb.in)
- [OpenAPI Specification](artifact/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include HTTP headers, request bodies, credential handling reminders, and endpoint-specific response fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
