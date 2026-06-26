## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and drive the agent-browser CLI for web navigation, structured page extraction, form filling, UI testing, screenshots, PDFs, recordings, and saved browser sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can submit forms, upload files, navigate authenticated sessions, or change data on live sites. <br>
Mitigation: Supervise actions with side effects and prefer isolated sessions, test accounts, or non-production sites for sensitive workflows. <br>
Risk: Saved browser state and captured artifacts can contain cookies, localStorage, credentials, private page content, screenshots, PDFs, recordings, or traces. <br>
Mitigation: Protect generated files, delete them when no longer needed, and avoid uploading private files unless the action is intended. <br>
Risk: The skill depends on an external agent-browser npm package. <br>
Mitigation: Install only when browser automation is needed and the package source is trusted for the target environment. <br>


## Reference(s): <br>
- [Agent Browser on ClawHub](https://clawhub.ai/asterisk622/xiaoding-agent-browser) <br>
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Text, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell command examples; agent-browser commands can return text or JSON and save screenshots, PDFs, recordings, traces, and browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm, then installs and runs the external agent-browser CLI.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
