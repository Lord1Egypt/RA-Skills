## Description: <br>
Control a remote Chrome browser via HTTP API for web automation, form filling, navigation, page inspection, accessibility-tree snapshots, text extraction, screenshots, DOM actions, and VNC actions on sites the user owns or has permission to access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vasyaod](https://clawhub.ai/user/vasyaod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to drive a remote browser session for permitted web automation, navigation, form workflows, page inspection, and visual or VNC-level verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote browser use sends browsing activity through rb.all-completed.com. <br>
Mitigation: Install only if that backend is acceptable for the intended work and use the skill only on sites the user owns or has permission to access. <br>
Risk: Stored sessions can preserve authenticated browser profiles and sensitive state. <br>
Mitigation: Prefer ephemeral sessions for sensitive work, delete stored sessions when finished, and avoid retaining logged-in profiles unless reuse is intentional. <br>
Risk: State-changing browser actions can succeed at the API layer without changing the page as intended. <br>
Mitigation: Verify important actions with the cheapest suitable follow-up check, such as status, text extraction, accessibility snapshots, or a targeted screenshot. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vasyaod/skills/remote-browser) <br>
- [Remote Browser Service Base URL](https://rb.all-completed.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with HTTP API examples and curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an active browser session and may use RBS_BASE_URL and AC_API_KEY configuration.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
