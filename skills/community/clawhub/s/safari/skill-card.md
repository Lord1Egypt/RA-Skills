## Description: <br>
Control Safari on macOS with AppleScript, safaridriver, screenshots, tab navigation, and real-browser read, click, and type workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control Safari on macOS when a workflow depends on the user's real Safari session, Safari-specific rendering, AppleScript automation, screenshots, or isolated safaridriver sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to interact with a user's live Safari session, including tabs, cookies, logged-in pages, screenshots, typing, and clicking. <br>
Mitigation: Require explicit approval for live-session clicks, typing, screenshots, tab switching, and other sensitive browser actions. <br>
Risk: Automation notes stored under ~/safari/ may retain durable Safari control context that the user no longer wants kept. <br>
Mitigation: Periodically review or delete ~/safari/ when retained Safari automation notes are no longer useful. <br>
Risk: Using the daily Safari profile for repetitive automation can expose personal session state unnecessarily. <br>
Mitigation: Prefer isolated WebDriver mode when real-session browser state is not required. <br>


## Reference(s): <br>
- [Safari Browser Control on ClawHub](https://clawhub.ai/ivangdavila/safari) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Preflight and Permissions](artifact/preflight-and-permissions.md) <br>
- [AppleScript Control](artifact/applescript-control.md) <br>
- [WebDriver and BiDi](artifact/webdriver-and-bidi.md) <br>
- [Screenshot and Visual Loop](artifact/screenshot-and-visual-loop.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell, AppleScript, JavaScript, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no external requests are made by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
