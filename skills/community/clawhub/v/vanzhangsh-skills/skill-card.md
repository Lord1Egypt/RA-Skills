## Description:

A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vanzhangsh](https://clawhub.ai/user/vanzhangsh)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to drive browser automation from an agent, including navigation, form interaction, page snapshots, UI testing, screenshots, PDFs, and structured page data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to install and operate a powerful external browser automation CLI.

Mitigation: Review the package source and release, prefer a pinned trusted version, and avoid elevated privileges during installation and use.

Risk: Saved browser state, cookies, headers, credentials, screenshots, videos, traces, and network logs may contain sensitive data.

Mitigation: Treat captured browser artifacts as secrets, store them securely, clean them up after use, and do not commit them to shared repositories.

Risk: Automated browser actions can change real application state, submit forms, or expose account data.

Mitigation: Use snapshots and waits to verify targets before interaction, prefer test environments where possible, and require human review before destructive or sensitive actions.

## Reference(s):

- [Agent Browser CLI upstream repository](https://github.com/vercel-labs/agent-browser)
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI)
- [ClawHub skill page](https://clawhub.ai/vanzhangsh/skills/vanzhangsh-skills)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and structured CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that create screenshots, PDFs, videos, traces, saved browser state, network logs, cookies, storage data, and JSON output from agent-browser.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
