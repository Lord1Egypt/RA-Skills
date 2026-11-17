## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to drive browser sessions, inspect page structure, interact with forms, capture screenshots or PDFs, and test web UIs through structured agent-browser commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents unpinned installation of a third-party browser automation package.

Mitigation: Review and trust the upstream agent-browser package before installation, or pin the package version in local deployment instructions.

Risk: Saved authenticated browser state can expose access to accounts if auth.json is mishandled.

Mitigation: Avoid saved auth state for high-privilege accounts and protect auth.json as sensitive data.

Risk: Screenshots, PDFs, videos, and traces can capture sensitive page content.

Mitigation: Store generated browser artifacts only in approved locations and handle them as sensitive data.

Risk: Passing real passwords as plain command arguments can expose credentials through shell history or process inspection.

Mitigation: Avoid real passwords in plain command arguments unless that exposure risk is explicitly accepted.

## Reference(s):

- [Temp Agent Browser ClawHub skill page](https://clawhub.ai/ayakolin/skills/temp-agent-browser)
- [agent-browser upstream CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser screenshots, PDFs, videos, traces, saved state files, and JSON command output when the documented CLI options are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
