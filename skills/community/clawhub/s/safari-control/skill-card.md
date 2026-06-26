## Description: <br>
Use Safari directly on macOS when work must happen in the user's real Safari session instead of a separate automation browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gordonynh](https://clawhub.ai/user/gordonynh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agents use this skill to inspect and operate the user's real Safari session on macOS when logged-in state, cookies, open tabs, Safari chrome, or live page content matter. It supports session inspection, native Safari controls, page reading, DOM actions, waits, screenshots, and page artifact export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate the user's real logged-in Safari profile, including active tabs and authenticated web sessions. <br>
Mitigation: Use it only for tasks where real Safari state is required, inspect session state before making changes, and avoid sensitive banking, healthcare, admin, email, work, or shopping sessions unless necessary. <br>
Risk: Cookie and browser-storage export or mutation can reveal or change active login and session data. <br>
Mitigation: Allow cookie or storage export and mutation only when the user explicitly requested that exact action and understands the session-data impact. <br>
Risk: Enabling Safari automation, Accessibility access, screenshots, or JavaScript from Apple Events gives the agent broader control over Safari. <br>
Mitigation: Enable only the permissions needed for the current workflow, confirm permission-dependent commands with the user when appropriate, and continue with reduced functionality if the user declines. <br>


## Reference(s): <br>
- [Safari Control ClawHub release](https://clawhub.ai/gordonynh/safari-control) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; commands can return JSON, text, screenshots, HTML, and saved page artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS Safari and may require Safari automation, Accessibility, screenshot, and JavaScript-from-Apple-Events permissions for full functionality.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
