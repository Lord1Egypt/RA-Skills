## Description: <br>
Zoom Admin provides managed OAuth access to the Zoom Admin API for managing users, meetings, webinars, recordings, and account settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Workspace administrators and developers use this skill to administer an authorized Zoom account through Maton's OAuth gateway, including user, meeting, webinar, recording, and account-setting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise broad Zoom administrator authority after OAuth authorization. <br>
Mitigation: Install only when Zoom administration through Maton is intended, authorize the correct Zoom account, review OAuth permissions, and revoke the Maton connection when it is no longer needed. <br>
Risk: Create, update, and delete operations can alter Zoom users, meetings, webinars, recordings, or account settings. <br>
Mitigation: Require explicit confirmation of the target account, resource, and intended effect before any write or delete request. <br>
Risk: The MATON_API_KEY is a sensitive credential used to authenticate requests to Maton. <br>
Mitigation: Keep the key in the MATON_API_KEY environment variable, avoid exposing it in prompts or logs, and rotate or remove it if access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/zoom-admin-api) <br>
- [Maton](https://maton.ai) <br>
- [Zoom API Overview](https://developers.zoom.us/docs/api/) <br>
- [Zoom Meeting API Reference](https://developers.zoom.us/docs/api/rest/reference/zoom-api/methods/) <br>
- [Zoom User API Reference](https://developers.zoom.us/docs/api/rest/reference/user/methods/) <br>
- [Zoom Account API Reference](https://developers.zoom.us/docs/api/rest/reference/account/methods/) <br>
- [Zoom Rate Limits](https://developers.zoom.us/docs/api/rest/rate-limits/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP endpoint descriptions, Python and JavaScript examples, shell commands, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an authorized Zoom Admin OAuth connection; write and delete actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
