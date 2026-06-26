## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vanzhangsh](https://clawhub.ai/user/vanzhangsh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, interaction, snapshots, UI testing, form filling, data extraction, and session-based web workflows through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external browser automation package that can interact with live websites. <br>
Mitigation: Install only if the external agent-browser package is trusted and review commands before execution. <br>
Risk: Saved browser state, recordings, screenshots, and traces can expose sensitive sessions or data. <br>
Mitigation: Use separate browser sessions for sensitive sites and keep state files, screenshots, recordings, and traces out of shared or version-controlled locations. <br>
Risk: Browser automation can submit forms, upload files, change settings, or make purchases. <br>
Mitigation: Require confirmation before the agent performs sensitive browser actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vanzhangsh/vanzhangsh-skills) <br>
- [Skill publisher profile](https://clawhub.ai/user/vanzhangsh) <br>
- [Agent Browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, json, files] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; uses the external agent-browser CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
