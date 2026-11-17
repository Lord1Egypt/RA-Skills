## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fresh3](https://clawhub.ai/user/fresh3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate browser workflows, including navigation, form filling, data extraction, UI testing, screenshots, PDF generation, recording, and stateful sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global installs can pull a changed package version at install time.

Mitigation: Install in a least-privileged or isolated environment and pin and verify the agent-browser package or source where possible.

Risk: Saved authenticated browser state and captured artifacts may contain sensitive cookies, localStorage, credentials, screenshots, PDFs, videos, traces, or uploaded files.

Mitigation: Treat these artifacts as sensitive, avoid saving auth.json in shared repositories or workspaces, restrict file permissions, and delete saved state when the task is complete.

## Reference(s):

- [Taizi Agent Browser ClawHub page](https://clawhub.ai/fresh3/skills/taizi-agent-browser)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser state files, screenshots, PDFs, videos, traces, cookies, localStorage, and uploaded-file interactions when the documented commands are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
