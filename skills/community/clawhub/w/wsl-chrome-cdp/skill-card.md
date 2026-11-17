## Description:

Enables WSL2-based agents to start and connect to Windows Chrome through the Chrome DevTools Protocol for browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[animaiontj](https://clawhub.ai/user/animaiontj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers using OpenClaw in WSL2 use this skill to connect browser tools to Windows Chrome for navigation, screenshots, form interaction, and page-content extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chrome remote debugging on port 9222 can expose powerful browser control if it is reachable beyond the intended local WSL2 environment.

Mitigation: Bind and use the debugging endpoint only for local WSL2 access, avoid broad network exposure, and review firewall changes before enabling the skill.

Risk: A debug browser profile may expose active sessions or sensitive browsing data to automation.

Mitigation: Use a dedicated Chrome debug profile and avoid signing sensitive accounts into that profile.

Risk: The requested OpenClaw config-write permission broadens install-time impact beyond launching Chrome.

Mitigation: Remove or narrowly justify the config-write permission unless the release clearly documents why it is required.

## Reference(s):

- [WSL Chrome CDP on ClawHub](https://clawhub.ai/animaiontj/skills/wsl-chrome-cdp)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser documentation](https://docs.openclaw.ai/tools/browser)
- [Troubleshooting guide](docs/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run local setup checks that launch Chrome with a remote-debugging port.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
