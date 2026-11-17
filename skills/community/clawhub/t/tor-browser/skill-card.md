## Description:

Headless browser automation with Tor SOCKS5 proxy support for accessing .onion sites, collecting page snapshots, interacting with elements, taking screenshots, and extracting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[admin4giter](https://clawhub.ai/user/admin4giter)

### License/Terms of Use:

MIT

## Use Case:

Developers, security researchers, and threat intelligence teams use this skill to run Tor-routed browser automation for .onion sites and privacy-preserving web navigation. It supports navigation, element interaction, page text and link extraction, screenshots, and Tor connectivity checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup commands may create persistent Tor services or change local service, Docker, or firewall exposure.

Mitigation: Review sudo, service, Docker, and firewall commands before running them, and only install the skill when Tor-specific browser automation is required.

Risk: Tor proxy or control ports can be exposed beyond the local machine if configured carelessly.

Mitigation: Bind proxy access to localhost, avoid exposing port 9051, and keep Tor control authentication enabled.

Risk: Automation may interact with untrusted web pages reached through Tor.

Mitigation: Avoid entering sensitive credentials into untrusted pages and prefer pinned dependencies or container images when installing runtime components.

## Reference(s):

- [Tor Browser Setup Guide](references/setup-guide.md)
- [Playwright Python documentation](https://playwright.dev/python/)
- [Tor Project](https://www.torproject.org/)
- [ClawHub skill listing](https://clawhub.ai/admin4giter/skills/tor-browser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell and Python commands; CLI results may be JSON, text, or screenshot files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python, Playwright with Chromium, and a Tor SOCKS5 proxy reachable at the configured address.]

## Skill Version(s):

1.1.0 (source: server release and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
