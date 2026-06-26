## Description: <br>
Manage Zoom meetings via OAuth API. Create, list, delete, and update events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vnagin](https://clawhub.ai/user/vnagin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to manage Zoom meetings from an agent workflow, including creating, listing, updating, inspecting, and deleting scheduled meetings through Zoom OAuth API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use broad Zoom meeting administration privileges, including creating, updating, and deleting meetings. <br>
Mitigation: Use a dedicated least-privilege Zoom Server-to-Server OAuth app and require human confirmation before update or delete commands run. <br>
Risk: Meeting creation enables cloud recording by default, which may trigger privacy, consent, or organizational compliance obligations. <br>
Mitigation: Grant recording access only when needed and confirm applicable legal and organizational consent requirements before use. <br>
Risk: The skill requires Zoom OAuth credentials and account identifiers. <br>
Mitigation: Store credentials only as environment variables or managed secrets and avoid committing credential files such as config.json. <br>


## Reference(s): <br>
- [Zoom Manager ClawHub Page](https://clawhub.ai/vnagin/zoom-manager-clawd) <br>
- [Publisher Profile](https://clawhub.ai/user/vnagin) <br>
- [Zoom App Marketplace](https://marketplace.zoom.us/) <br>
- [Zoom OAuth Token Endpoint](https://api.zoom.us/oauth/token) <br>
- [Zoom Meetings API](https://api.zoom.us/v2/users/{user_id}/meetings) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from Zoom API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and Zoom Server-to-Server OAuth credentials in environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
