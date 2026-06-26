## Description: <br>
Manage a Talkspresso business using the Talkspresso REST API for services, appointments, products, clients, earnings, calendar settings, profile updates, scheduling, and related account tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baron-talkspresso](https://clawhub.ai/user/baron-talkspresso) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Talkspresso account owners and operators use this skill to manage bookings, services, products, client records, earnings, profile settings, availability, files, and customer communications through authenticated Talkspresso API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform broad account-changing Talkspresso API actions, including booking, cancellation, profile, calendar, service, product, pricing, messaging, and deletion changes. <br>
Mitigation: Require explicit user confirmation before any mutating action and show the exact target record, payload, recipient, message text, price, or schedule change before execution. <br>
Risk: The skill can upload local files to Talkspresso endpoints. <br>
Mitigation: Confirm the exact local file path, upload endpoint, intended destination, and attachment target before uploading. <br>
Risk: The skill depends on a Talkspresso API key with access to client, transaction, scheduling, and account data. <br>
Mitigation: Use the least-privileged API key available, avoid exposing it in logs or shared output, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Talkspresso API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/baron-talkspresso/talkspresso) <br>
- [Talkspresso API Key Settings](https://app.talkspresso.com/settings/api-keys) <br>
- [Talkspresso Signup](https://talkspresso.com/signup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses TALKSPRESSO_API_KEY and jq .data for Talkspresso REST API responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
