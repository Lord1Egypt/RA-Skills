## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent operators use this skill to drive browser workflows for navigation, form filling, UI testing, structured page extraction, screenshots, PDFs, video recording, and session reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad control over authenticated browser sessions and persistent session files. <br>
Mitigation: Use isolated test accounts where possible, protect or delete saved state files such as auth.json, and require explicit approval for uploads, submissions, account changes, cookie or storage edits, and JavaScript execution on logged-in sites. <br>
Risk: Command examples may encourage passing sensitive credentials directly through browser automation workflows. <br>
Mitigation: Avoid real passwords in command lines; use test credentials or approved secret-handling practices before automating login flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-agent-browser) <br>
- [agent-browser upstream project](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser CLI skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands; command output may be text, JSON, screenshots, PDFs, videos, traces, or saved browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; uses the agent-browser CLI and can persist browser session state.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
