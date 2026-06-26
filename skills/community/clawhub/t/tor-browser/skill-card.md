## Description: <br>
Headless browser automation with Tor SOCKS5 proxy support for accessing .onion sites and anonymous browsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Admin4Giter](https://clawhub.ai/user/Admin4Giter) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, security researchers, and threat intelligence teams use this skill to automate Tor-routed browsing, inspect public .onion resources, collect page text or links, interact with page elements, and capture screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tor proxy or control ports could be exposed beyond the local machine. <br>
Mitigation: Keep Tor services bound to localhost and avoid exposing ports 9050 or 9051. <br>
Risk: Automated clicks and form fills can perform unintended actions on sensitive sites. <br>
Mitigation: Supervise browser actions, review target pages before interaction, and use the headed mode when manual confirmation is needed. <br>
Risk: Screenshots, extracted links, and page text may contain sensitive browsing data. <br>
Mitigation: Store generated files locally with appropriate access controls and delete them when no longer needed. <br>
Risk: Unpinned or untrusted dependencies can alter browser automation behavior. <br>
Mitigation: Use trusted or pinned dependencies and install Playwright browser binaries from expected sources. <br>


## Reference(s): <br>
- [Tor Browser Setup Guide](references/setup-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/Admin4Giter/tor-browser) <br>
- [Playwright Python documentation](https://playwright.dev/python/) <br>
- [Tor Project](https://www.torproject.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands, Python examples, JSON command output, extracted text or links, and screenshot files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local Tor SOCKS5 proxy and Playwright Chromium; screenshots and extracted content may contain sensitive browsing data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
