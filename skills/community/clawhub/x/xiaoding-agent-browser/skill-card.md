## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asterisk622](https://clawhub.ai/user/asterisk622)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser navigation, form filling, page inspection, UI testing, screenshots, PDFs, recording, storage management, and network-aware web workflows through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved authentication state, cookies, localStorage, screenshots, PDFs, videos, and traces can contain secrets or personal data.

Mitigation: Treat generated browser artifacts and saved state files as sensitive; avoid committing or sharing them and store them only in task-appropriate locations.

Risk: Installing or running an unpinned browser automation CLI can create supply-chain exposure.

Mitigation: Pin and verify the agent-browser package where possible, and avoid elevated installs unless they are necessary.

Risk: Automated browser actions can interact with live sites using existing sessions.

Mitigation: Review target URLs and commands before execution, use isolated sessions for unrelated tasks, and avoid reusing saved auth state across workflows.

## Reference(s):

- [Agent Browser Skill Page](https://clawhub.ai/asterisk622/skills/xiaoding-agent-browser)
- [Agent Browser Skill Issues](https://github.com/TheSethRose/Agent-Browser-CLI)
- [agent-browser CLI](https://github.com/vercel-labs/agent-browser)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser artifacts such as screenshots, PDFs, videos, traces, cookies, localStorage data, and saved auth state through CLI commands.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
