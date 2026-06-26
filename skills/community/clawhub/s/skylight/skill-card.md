## Description: <br>
Interact with Skylight Calendar frame - manage calendar events, chores, lists, task box items, and rewards. Use when the user wants to view/create calendar events, manage family chores, work with shopping or to-do lists, check reward points, or interact with their Skylight smart display. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yurybubnov](https://clawhub.ai/user/yurybubnov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and household administrators use this skill to ask an agent for Skylight Calendar operations such as viewing calendar events, managing chores, working with shopping or to-do lists, checking rewards, and creating task box items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Skylight account credentials and bearer tokens. <br>
Mitigation: Use a secret manager where possible, keep credentials and tokens out of logs and commits, and rotate or regenerate tokens if exposed. <br>
Risk: The integration is unofficial and reverse-engineered, so Skylight API behavior may change without notice. <br>
Mitigation: Review generated API calls before use and update authentication or endpoints when Skylight returns authorization, redirect, or response-format errors. <br>
Risk: The skill can create or change shared household calendar events, chores, lists, rewards, and task box items. <br>
Mitigation: Confirm write actions before execution, especially for shared household resources. <br>
Risk: Manual HTTPS proxy token capture can expose account traffic, credentials, or bearer tokens. <br>
Mitigation: Avoid proxy capture unless necessary and only use trusted local tooling and certificates. <br>


## Reference(s): <br>
- [ClawHub Skylight skill page](https://clawhub.ai/yurybubnov/skylight) <br>
- [Skylight web app](https://app.ourskylight.com) <br>
- [Skylight website](https://ourskylight.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run Skylight API calls that require SKYLIGHT_FRAME_ID and authentication environment variables; Skylight API responses use JSON:API when commands are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
