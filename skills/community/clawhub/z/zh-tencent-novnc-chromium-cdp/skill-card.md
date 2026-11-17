## Description:

Provides an agent workflow for deploying or attaching to a visible browser using noVNC, Chromium, and CDP on Linux, or Edge/Chrome CDP on Windows, so users and agents can share browser state during web automation and manual verification steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangleizhui](https://clawhub.ai/user/kangleizhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a remote, visible browser that an agent can control through CDP while a human handles login, CAPTCHA, slider, or other verification steps. It is aimed at web automation workflows that need a shared visual browser session rather than headless-only execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad root-level control to install packages, write service files, and configure persistent browser services.

Mitigation: Use a disposable or dedicated host, review commands before execution, avoid blanket passwordless sudo, and remove any temporary elevated access after deployment.

Risk: A noVNC endpoint can expose an interactive browser session if reachable by unauthorized users.

Mitigation: Keep noVNC off the public Internet unless protected by an SSH tunnel, VPN, TLS, strong access control, and firewall source restrictions.

Risk: Persistent remote access services may remain available after the automation task is complete.

Mitigation: Disable and remove noVNC, VNC, Chromium/CDP, and related system services when finished.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangleizhui/skills/zh-tencent-novnc-chromium-cdp)
- [Publisher profile](https://clawhub.ai/user/kangleizhui)
- [noVNC project](https://github.com/novnc/noVNC.git)
- [Google Chrome Linux package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational instructions for browser deployment, CDP connection checks, status reporting, and screenshots.]

## Skill Version(s):

1.0.45 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
