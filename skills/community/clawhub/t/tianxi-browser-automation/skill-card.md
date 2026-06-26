## Description: <br>
Browser Automation guides an agent through browser-based web navigation, form filling, social media posting, file upload, search, screenshot capture, and data extraction tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangyu68](https://clawhub.ai/user/zhangyu68) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a task requires controlled interaction with real websites through a browser, including navigation, element interaction, form submission, uploads, screenshots, and task-result summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate real websites and accounts through a browser. <br>
Mitigation: Use a separate browser profile where possible and require explicit user confirmation before submitting forms, posting publicly, sending email, registering accounts, uploading files, or accepting dialogs. <br>
Risk: The skill may encounter sensitive account, network, or browser-state data during automation. <br>
Mitigation: Do not enter sensitive information unless the user has explicitly provided it for the task, and confirm before inspecting network data or clearing cookies and cache. <br>
Risk: The artifact describes default confirmation of browser dialogs, which can create unintended side effects. <br>
Mitigation: Pause for user confirmation before accepting dialogs that can change account state, publish content, upload files, or affect privacy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangyu68/tianxi-browser-automation) <br>
- [Publisher profile](https://clawhub.ai/user/zhangyu68) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, shell commands, configuration] <br>
**Output Format:** [Markdown instructions with structured browser tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce progress updates, screenshots, operation summaries, and next-step recommendations when used with a browser MCP server.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
