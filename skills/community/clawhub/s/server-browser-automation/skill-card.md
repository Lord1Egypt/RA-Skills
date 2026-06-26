## Description: <br>
Configures OpenClaw browser automation on headless Ubuntu servers using an XFCE/VNC desktop, Chrome remote debugging, and persistent browser profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenzheng9527](https://clawhub.ai/user/shenzheng9527) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to set up server-side Chrome sessions for logged-in website automation, data collection, automated testing, scheduled checks, and batch browser operations through OpenClaw. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may gain persistent control over logged-in browser sessions and sensitive cookies. <br>
Mitigation: Use dedicated or disposable automation hosts, avoid high-value personal accounts, keep separate browser profiles for each account, and stop Chrome/VNC when work is complete. <br>
Risk: Exposed VNC or Chrome remote debugging ports can allow unauthorized browser or host access. <br>
Mitigation: Firewall or SSH-tunnel VNC and Chrome debugging ports, run VNC and Chrome as a non-root user, and limit access to trusted operators. <br>
Risk: Browser automation can submit forms, post content, purchase items, delete data, or otherwise change account state. <br>
Mitigation: Require explicit human approval before posting, submitting forms, purchasing, deleting, or changing account data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shenzheng9527/server-browser-automation) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [VNC documentation](https://www.realvnc.com/en/connect/docs/) <br>
- [XFCE documentation](https://docs.xfce.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operating guidance for host package installation, VNC, Chrome remote debugging, persistent browser profiles, and OpenClaw browser commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
