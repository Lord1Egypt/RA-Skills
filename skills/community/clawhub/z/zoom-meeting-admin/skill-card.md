## Description: <br>
Manage Zoom meetings, cloud recordings, and account users through a fixed set of Zoom Server-to-Server OAuth REST actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mebusw](https://clawhub.ai/user/mebusw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Zoom account administrators and operators use this skill from an agent to list, inspect, create, or delete scheduled meetings, query cloud recordings, and look up account users. It is intended for environments where a dedicated Zoom Server-to-Server OAuth app can be configured with only the scopes needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Zoom Server-to-Server OAuth credentials and caches access tokens locally, so leaked files or logs could expose account-level access. <br>
Mitigation: Use a dedicated Zoom app, grant only required scopes, keep .env and ~/.zoom-s2s-token.json private with restrictive permissions, and verify .env is ignored by git. <br>
Risk: Meeting creation and deletion can change live Zoom account state. <br>
Mitigation: Require explicit human approval before creating or deleting meetings, and keep delete permissions disabled unless they are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mebusw/zoom-meeting-admin) <br>
- [Zoom Marketplace](https://marketplace.zoom.us/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.7+, network access to Zoom APIs, and local Zoom Server-to-Server OAuth credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
