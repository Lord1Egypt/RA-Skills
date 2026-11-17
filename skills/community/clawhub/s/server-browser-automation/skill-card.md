## Description:

Server Browser Automation helps configure OpenClaw browser automation on headless Ubuntu servers using an XFCE virtual desktop, VNC, Chrome remote debugging, and persistent browser profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenzheng9527](https://clawhub.ai/user/shenzheng9527)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to set up a server-hosted browser that OpenClaw agents can control for authenticated web workflows, scraping, testing, scheduled checks, and batch browser operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provisions a server desktop and remotely controllable browser environment with VNC and Chrome debugging surfaces.

Mitigation: Use an isolated development server or VM, restrict network exposure, and do not expose VNC or Chrome debugging ports publicly.

Risk: Persistent browser profiles can retain real login cookies and authenticated sessions.

Mitigation: Protect profile directories, avoid storing sensitive production logins, and clear profiles when credentials should no longer persist.

Risk: The installer expects elevated system access and changes desktop, browser, VNC, and OpenClaw configuration.

Mitigation: Review the installer before running it, avoid running the browser or VNC session as root, and prefer manual installation when tighter change control is required.

## Reference(s):

- [OpenClaw official documentation](https://docs.openclaw.ai)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [VNC documentation](https://www.realvnc.com/en/connect/docs/)
- [XFCE documentation](https://docs.xfce.org/)
- [ClawHub skill page](https://clawhub.ai/shenzheng9527/skills/server-browser-automation)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, usage, troubleshooting, and browser automation instructions for OpenClaw on Ubuntu servers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
