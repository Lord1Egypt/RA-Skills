## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwqwghksvq-sketch](https://clawhub.ai/user/gwqwghksvq-sketch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate browser tasks such as navigation, form filling, UI testing, structured page inspection, screenshots, PDF export, and session handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate authenticated browser sessions and expose saved state, traces, screenshots, recordings, headers, or auth files. <br>
Mitigation: Use it only for intended browser automation, keep generated state and media out of shared folders and source control, delete sensitive outputs when finished, and avoid sensitive accounts unless that access is intended. <br>
Risk: Browser automation can submit forms, alter session state, or interact with external services in ways that affect real accounts or systems. <br>
Mitigation: Review targets and commands before execution, prefer test accounts or isolated sessions, and confirm actions before using authenticated production services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gwqwghksvq-sketch/tekin) <br>
- [Agent Browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash command examples and optional JSON, screenshots, PDFs, videos, traces, and saved browser state files from the CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser state, screenshots, traces, recordings, headers, and auth files should be treated as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
