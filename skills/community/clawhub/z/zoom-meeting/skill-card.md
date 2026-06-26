## Description: <br>
Creates, retrieves, lists, and deletes Zoom meetings through the Zoom REST API, supporting natural language requests and structured JSON commands while returning human-readable text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Neuyazvimyi](https://clawhub.ai/user/Neuyazvimyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, and developers use this skill to schedule Zoom meetings, retrieve join details, list upcoming meetings, and cancel meetings for the configured Zoom account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete Zoom meetings using stored account credentials without a documented confirmation step. <br>
Mitigation: Require explicit user confirmation before delete requests and verify the meeting ID and account context before execution. <br>
Risk: Stored Zoom OAuth credentials can act on the configured Zoom account. <br>
Mitigation: Use least-privilege Zoom app scopes and protect ~/.openclaw/credentials/zoom.json. <br>
Risk: Timezone defaults may schedule meetings at an unintended local time. <br>
Mitigation: Confirm the start time and timezone before creating scheduled meetings. <br>


## Reference(s): <br>
- [Zoom API Reference](references/zoom_api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, guidance] <br>
**Output Format:** [Human-readable plain text; no JSON output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zoom Server-to-Server OAuth credentials; meeting create and delete actions affect the configured Zoom account.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
