## Description: <br>
Manages the Web Terminal Chrome Extension local backend server for starting, stopping, and checking the local terminal server on port 8989. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yayayahei](https://clawhub.ai/user/yayayahei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and power users use this skill to manage a local backend that exposes a browser-accessible terminal through a Chrome extension. It helps start, stop, check, and explain setup for the local terminal service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A real local shell is reachable from a browser extension through a broadly reachable localhost service with weak controls. <br>
Mitigation: Install only when browser access to a local shell is intentional; restrict use to trusted sites and add authentication plus WebSocket origin checks before broader use. <br>
Risk: Terminal activity and history replay can expose shell output to browser clients. <br>
Mitigation: Avoid using the extension while browsing untrusted pages, and clear or disable terminal history replay when sensitive commands or output may be present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yayayahei/terminal-in-chrome) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local server operation guidance for a Chrome extension terminal workflow.] <br>

## Skill Version(s): <br>
1.1.29 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
