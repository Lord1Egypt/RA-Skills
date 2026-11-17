## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a-din](https://clawhub.ai/user/a-din)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to automate web navigation, page inspection, form filling, UI testing, and structured data extraction through the agent-browser CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation can operate on authenticated sessions and save reusable login state.

Mitigation: Use the skill only on sites and accounts intended for automation, avoid saving authenticated state unless necessary, and treat any saved state files as secrets.

Risk: Screenshots, PDFs, and video recordings can capture sensitive page or account content.

Mitigation: Store captures securely, review them before sharing, and clean them up after use.

Risk: Installing a global latest-version CLI can introduce unreviewed behavior changes.

Mitigation: Prefer a pinned version or isolated install and review the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a-din/skills/xiaopi-agent-browser)
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue tracker](https://github.com/TheSethRose/Agent-Browser-CLI)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON, Files]

**Output Format:** [Markdown guidance with shell command examples, optional JSON CLI output, screenshots, PDFs, and recording files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm; browser state files, screenshots, PDFs, and recordings may contain sensitive page or account data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
