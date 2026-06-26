## Description: <br>
Zoho Calendar API integration with managed OAuth for reading, creating, updating, and deleting calendars and events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect an agent to Zoho Calendar through Maton-managed OAuth, inspect calendars, schedule meetings, and manage events after user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Maton API key and OAuth-backed access to Zoho Calendar data. <br>
Mitigation: Install only if you trust Maton with calendar access, keep MATON_API_KEY private, and remove unused OAuth connections. <br>
Risk: Calendar create, update, and delete operations can modify or remove user scheduling data. <br>
Mitigation: Confirm the target calendar or event and intended effect with the user before every write or delete action. <br>
Risk: When multiple Zoho Calendar accounts are connected, requests may target the wrong account. <br>
Mitigation: Use the Maton-Connection header when more than one account is connected. <br>


## Reference(s): <br>
- [ClawHub Zoho Calendar skill page](https://clawhub.ai/byungkyu/zoho-calendar) <br>
- [Zoho Calendar API Introduction](https://www.zoho.com/calendar/help/api/introduction.html) <br>
- [Zoho Calendar Events API](https://www.zoho.com/calendar/help/api/events-api.html) <br>
- [Zoho Calendar Calendars API](https://www.zoho.com/calendar/help/api/calendars-api.html) <br>
- [Zoho Calendar Create Event](https://www.zoho.com/calendar/help/api/post-create-event.html) <br>
- [Zoho Calendar Get Events List](https://www.zoho.com/calendar/help/api/get-events-list.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, API calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline Python, JavaScript, HTTP, Bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY; use Maton-Connection to select a specific OAuth connection when multiple accounts are connected.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
