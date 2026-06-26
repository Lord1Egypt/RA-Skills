## Description: <br>
A browser automation helper that uses Chrome remote debugging to support web operations such as data scraping, form filling, content posting, and screenshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxie48892-jpg](https://clawhub.ai/user/dxie48892-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect to a locally running Chrome remote debugging session and automate browser tasks such as scraping data, filling forms, posting content, and capturing screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome remote debugging gives strong control over the running browser, including logged-in sessions. <br>
Mitigation: Use a separate Chrome profile or test account, keep the debug port local, and close the remote-debugging browser when finished. <br>
Risk: The helper can print a Chrome WebSocket URL that may allow browser control if shared. <br>
Mitigation: Do not share the WebSocket URL and supervise sensitive actions such as form submission or content posting. <br>


## Reference(s): <br>
- [Web Automation Helper on ClawHub](https://clawhub.ai/dxie48892-jpg/web-automation-helper) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct use of a local Chrome remote debugging endpoint and report connection status or WebSocket URL details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
