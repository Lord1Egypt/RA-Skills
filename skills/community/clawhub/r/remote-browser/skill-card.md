## Description: <br>
Controls a remote Chrome browser via HTTP API for permitted web automation, form filling, navigation, page inspection, screenshots, VNC-native interaction, and DOM actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vasyaod](https://clawhub.ai/user/vasyaod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a remote Chrome session for web navigation, form filling, page inspection, and visual or VNC-based workflows on sites they own or have permission to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can navigate pages and perform browser actions that affect accounts, forms, or other web state. <br>
Mitigation: Use it only on sites the user owns or has permission to access, review planned actions, and verify state changes after each meaningful action. <br>
Risk: Credentials, login codes, or payment details could be exposed if entered directly into chat, commands, or logs. <br>
Mitigation: Use the documented request-fill flow for sensitive values and avoid placing secrets in review bundles or command examples. <br>
Risk: Stored browser sessions can preserve cookies, local storage, IndexedDB, service workers, and cache data across reconnects. <br>
Mitigation: Delete stored sessions when they are no longer needed and limit access to authenticated users who are expected to operate the browser session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vasyaod/skills/remote-browser) <br>
- [Remote Browser Service API base URL](https://rb.all-completed.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, API calls] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active remote browser session; authentication may use a bearer token or API key.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
