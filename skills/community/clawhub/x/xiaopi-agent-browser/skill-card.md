## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and capture page state through structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a-din](https://clawhub.ai/user/a-din) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill to automate browser workflows, inspect pages, fill forms, capture screenshots or PDFs, and manage browser state from shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-controlled browser automation can interact with websites, forms, authenticated sessions, cookies, storage, and network behavior. <br>
Mitigation: Use only on sites intended for automation, avoid privileged accounts where possible, and review commands before executing actions that submit data or modify state. <br>
Risk: Screenshots, PDFs, videos, traces, saved sessions, and cookies can contain sensitive page or account data. <br>
Mitigation: Treat captured files and saved browser state as sensitive local artifacts; store, share, and delete them according to the deployment's data handling rules. <br>
Risk: The skill installs and invokes an external npm package. <br>
Mitigation: Verify the external npm package before installation and keep the runtime limited to environments where node and npm are expected dependencies. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/a-din/xiaopi-agent-browser) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issues](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser captures, saved state, cookies, screenshots, PDFs, videos, and traces may create sensitive local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
