## Description: <br>
Control the user's real Safari browser on macOS using AppleScript and screencapture to read pages, click elements, type text, take screenshots, and navigate tabs through the user's actual browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SDLLL](https://clawhub.ai/user/SDLLL) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users on macOS use this skill to operate an existing Safari session for browsing, page inspection, screenshots, form entry, and tab navigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real logged-in Safari browser session, including authenticated pages, cookies, open tabs, clicks, forms, and screenshots. <br>
Mitigation: Install it only when this broad browser authority is intended, supervise actions, and require explicit confirmation before reading authenticated pages, taking screenshots, executing JavaScript, clicking, filling forms, making purchases, sending messages, or changing accounts. <br>
Risk: Browser automation may expose sensitive personal or business data from the user's active Safari profile. <br>
Mitigation: Use a dedicated or non-sensitive browser profile where possible and avoid granting access to sessions that contain data outside the task scope. <br>
Risk: macOS Automation and Screen Recording permissions can continue to grant browser control after the immediate task is finished. <br>
Mitigation: Revoke Automation or Screen Recording permissions when the skill is no longer needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash, AppleScript, JavaScript, and Swift code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser page text and screenshots when its commands are executed against Safari.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
