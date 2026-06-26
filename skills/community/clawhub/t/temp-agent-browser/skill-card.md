## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayakolin](https://clawhub.ai/user/ayakolin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser navigation, UI testing, form filling, structured page extraction, screenshots, and session workflows through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act inside logged-in browser sessions and perform high-impact web actions. <br>
Mitigation: Use a dedicated or throwaway browser session, avoid sensitive accounts unless necessary, and require human approval for submissions, uploads, purchases, account changes, or other consequential actions. <br>
Risk: Browser state, cookies, screenshots, recordings, PDFs, and saved authentication files can expose sensitive data. <br>
Mitigation: Store capture and authentication files in protected locations, limit retention, and clear cookies or storage after use. <br>
Risk: The workflow depends on installing and running the external agent-browser package. <br>
Mitigation: Install only when the package source is trusted and review package updates before use in sensitive environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayakolin/temp-agent-browser) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with agent-browser shell commands; command output may be text, JSON, screenshots, PDFs, recordings, or browser state files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser automation may read, modify, save, or clear session state depending on the command used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
