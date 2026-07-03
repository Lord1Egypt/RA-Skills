## Description: <br>
Controls a remote Chrome browser through an HTTP API for permitted web automation, form filling, navigation, page inspection, screenshots, DOM actions, and VNC actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vasyaod](https://clawhub.ai/user/vasyaod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI-agent operators use this skill to control authenticated remote browser sessions for web automation, form filling, navigation, and page inspection on sites they own or have permission to access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated remote browser sessions can retain logged-in state and stored browser profile data. <br>
Mitigation: Install only when the user trusts the remote browser service provider, treat stored sessions like logged-in browser profiles, and delete stored sessions when they are no longer needed. <br>
Risk: Credentials or payment details entered through ordinary chat or direct browser typing may expose sensitive values to the agent workflow. <br>
Mitigation: Use the request-fill flow for secrets and payment fields, avoid asking users to paste credentials into chat, and fall back to user-driven VNC sign-in when request-fill is unavailable. <br>
Risk: State-changing browser actions can report success without producing the intended page change. <br>
Mitigation: Verify the page state after actions using the lowest-cost suitable read method, such as status, text, accessibility snapshots, or a clipped screenshot when visual confirmation is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vasyaod/skills/remote-browser-service) <br>
- [Publisher profile](https://clawhub.ai/user/vasyaod) <br>
- [Remote Browser Service API base URL](https://rb.all-completed.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes HTTP endpoint examples, session lifecycle guidance, token-cost guidance, and safety notes for secrets and persistent browser sessions.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
