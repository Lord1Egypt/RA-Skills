## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwqwghksvq-sketch](https://clawhub.ai/user/gwqwghksvq-sketch)

### License/Terms of Use:


## Use Case:

Developers and AI agents use this skill to automate browser navigation, page inspection, form entry, UI testing, screenshots, PDF export, video recording, and structured page data extraction through agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing mutable global tooling can change behavior over time or introduce unreviewed code into the agent environment.

Mitigation: Pin and verify the agent-browser version or commit, and install it only after review in an isolated account or sandbox.

Risk: Saved browser state, traces, screenshots, videos, cookies, and storage dumps can contain credentials or other sensitive data.

Mitigation: Avoid production credentials where possible, treat generated browser artifacts as secrets, and delete saved authentication state when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwqwghksvq-sketch/skills/tekin)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and command output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May instruct agents to request JSON output from agent-browser for machine-readable browser snapshots and page data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
