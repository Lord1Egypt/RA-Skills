## Description: <br>
Use when interacting with TeamApp club admin JSON endpoints on teamapp.com to create/read/update News articles and Schedule events, and to resolve Team and Access Group IDs needed for visibility, roster, and targeting fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thed000d](https://clawhub.ai/user/thed000d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site administrators use this skill to operate TeamApp club admin JSON endpoints for News articles, Schedule events, Teams, and Access Groups. It helps resolve required IDs, inspect form schemas, construct write payloads, and verify changes through TeamApp list endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad TeamApp club administration authority through an authenticated session. <br>
Mitigation: Use a least-privileged admin session and manually confirm every write, archive, delete, or notification-sending action before execution. <br>
Risk: TA_AUTH_TOKEN and cached session files are sensitive session material. <br>
Mitigation: Keep TA_AUTH_TOKEN out of chats and logs, and remove /tmp/teamapp_cookies.txt and /tmp/teamapp_csrf.txt after use. <br>
Risk: The wrapper accepts full URLs and curl options, which could be misdirected if used outside the intended service. <br>
Mitigation: Restrict wrapper calls to TeamApp URLs and verify the target club, resource, and endpoint before sending requests. <br>


## Reference(s): <br>
- [Endpoint and Payload Map](references/api-map.md) <br>
- [TeamApp Admin on ClawHub](https://clawhub.ai/thed000d/teamapp-admin) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and TeamApp JSON endpoint details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a TA_AUTH_TOKEN environment variable and routes TeamApp requests through the bundled wrapper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
