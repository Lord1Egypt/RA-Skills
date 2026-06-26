## Description: <br>
Automate web browser interactions using natural language via CLI commands for browsing websites, navigating pages, extracting data, taking screenshots, filling forms, clicking buttons, and interacting with web applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[peytoncasper](https://clawhub.ai/user/peytoncasper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to drive a browser from CLI commands when they need an agent to navigate pages, extract structured data, take screenshots, or perform form and click workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad browser and shell-driven authority while reusing sessions, saving page data, and downloading files. <br>
Mitigation: Use a dedicated browser profile, avoid saved passwords and sensitive accounts, confirm before submitting forms or downloading files, and periodically clear screenshots, downloads, cache, and .chrome-profile data. <br>
Risk: The skill can switch between local Chrome and remote Browserbase execution based on available configuration. <br>
Mitigation: Choose local versus Browserbase mode deliberately and verify environment configuration before running sensitive browsing tasks. <br>
Risk: The security verdict is suspicious and the installed CLI source and dependencies are outside the provided evidence bundle. <br>
Mitigation: Install only if you trust the publisher and can inspect the actual CLI source and dependency chain behind the npm install and npm link flow. <br>


## Reference(s): <br>
- [Stagehand Browser CLI on ClawHub](https://clawhub.ai/peytoncasper/stagehand-browser-cli) <br>
- [EXAMPLES.md](EXAMPLES.md) <br>
- [REFERENCE.md](REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots, downloaded files, structured extraction JSON, and persistent browser session data depending on the command used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
