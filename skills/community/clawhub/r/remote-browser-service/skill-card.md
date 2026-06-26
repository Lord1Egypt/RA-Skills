## Description: <br>
Control a remote Chrome browser through an HTTP API for permitted web automation, form filling, navigation, page inspection, DOM actions, VNC actions, text extraction, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vasyaod](https://clawhub.ai/user/vasyaod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to create or resume remote browser sessions, inspect pages through text, accessibility snapshots, DOM data, screenshots, or VNC, and perform browser actions on sites the user owns or has permission to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent operate a remote browser, including on authenticated sessions and user-permitted sites. <br>
Mitigation: Install only when comfortable granting browser-control access, limit use to sites the user owns or has permission to access, and verify state after browser actions. <br>
Risk: Persistent browser profiles and saved auth-state files can contain sensitive session data. <br>
Mitigation: Treat stored session data like passwords: avoid highly sensitive accounts, do not commit session material, and delete session data when finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vasyaod/skills/remote-browser-service) <br>
- [Remote Browser Service API base](https://rb.all-completed.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls, text, JSON] <br>
**Output Format:** [Markdown guidance with curl examples, JSON request and response shapes, and browser-output references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active browser session; AC_API_KEY is optional for bearer or API-key authentication, and RBS_BASE_URL may override the default service URL.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
