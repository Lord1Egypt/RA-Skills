## Description: <br>
A scheduling and booking management platform with Google Calendar integration, event type management, availability rules, and time slot booking capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use Scheduly to create event types, manage availability, book time slots, maintain public booking pages, and coordinate Google Calendar-connected scheduling workflows for service providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate booking, Google Calendar, renewal, and account actions that may affect real schedules or connected accounts. <br>
Mitigation: Install only when the publisher is trusted, verify OAuth scopes and token handling before connecting Google Calendar, and require explicit user approval before account or calendar changes. <br>
Risk: Delete, cancel, disconnect, renewal, auto-renewal, scheduler, and 500-coin event creation actions may be destructive or cost-incurring. <br>
Mitigation: Require explicit confirmation before these actions and show the affected booking, event type, account, renewal state, or coin charge before execution. <br>
Risk: Public booking pages and user_id or object ID parameters can expose or modify scheduling data if ownership and visibility are not checked. <br>
Mitigation: Verify the intended user, object identifiers, and public booking-page visibility before reading, changing, or publishing scheduling information. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-scheduly) <br>
- [Scheduly API Base](https://api.toolweb.in/tools/scheduly) <br>
- [Scheduly API Docs](https://api.toolweb.in:8160/docs) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include booking, event type, availability, Google Calendar, renewal, and public booking page operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
