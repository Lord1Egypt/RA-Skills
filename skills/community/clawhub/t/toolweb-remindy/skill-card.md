## Description:

Email and browser push notification reminders delivered 15 minutes before scheduled events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and web application builders use Remindy to create, list, and delete time-zone-aware reminders and manage browser push subscriptions for email or push notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API contract exposes user-scoped reminder and push-notification actions without documented authentication or authorization controls.

Mitigation: Do not use it for sensitive schedules, private task details, or real user notification subscriptions unless the publisher confirms authentication, ownership checks, and deletion behavior.

## Reference(s):

- [OpenAPI contract](artifact/openapi.json)
- [Remindy API documentation](https://api.toolweb.in:8198/docs)
- [Remindy API route](https://api.toolweb.in/tools/remindy)
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-remindy)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API calls may include user IDs, reminder details, email addresses, timezone strings, and browser push subscription values.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
