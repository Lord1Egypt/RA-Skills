## Description: <br>
Email and browser push notification reminders delivered 15 minutes before scheduled events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use Remindy to create, list, and delete scheduled reminders, manage browser push subscriptions, and send email or push notifications before scheduled events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service stores and changes personal reminder, email, and push-notification data without documenting authentication or ownership checks. <br>
Mitigation: Confirm provider authentication and userId access controls before production use, and test that users cannot list, modify, or delete another user's reminders. <br>
Risk: Push subscription secrets and notification email addresses may be sensitive personal data. <br>
Mitigation: Use non-sensitive reminders until storage, retention, deletion, consent, and secret-protection controls are documented and accepted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-remindy) <br>
- [API Documentation](https://api.toolweb.in:8198/docs) <br>
- [Kong Route](https://api.toolweb.in/tools/remindy) <br>
- [OpenAPI Specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with JSON request and response examples plus OpenAPI 3.1 schema.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reminder, push subscription, status, and health-check interactions; no token cap is specified.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; OpenAPI service version reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
