## Description: <br>
Enables OpenClaw in WSL2 to detect, launch, and verify a Windows Chrome instance with Chrome DevTools Protocol remote debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[animaiontj](https://clawhub.ai/user/animaiontj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users on Windows with WSL2 use this skill to prepare Chrome for browser automation through CDP without manual startup steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chrome remote debugging can expose browser state and automation control if port 9222 is reachable by untrusted processes or networks. <br>
Mitigation: Keep CDP access restricted to localhost or trusted WSL access, avoid broad firewall exposure, and close the debug Chrome session after use. <br>
Risk: Troubleshooting may require terminating a process that owns port 9222. <br>
Mitigation: Verify the target PID before running taskkill so unrelated processes are not stopped. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/animaiontj/wsl-chrome-cdp) <br>
- [OpenClaw Browser Documentation](https://docs.openclaw.ai/tools/browser) <br>
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/) <br>
- [Troubleshooting Guide](docs/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, PowerShell, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Chrome CDP endpoint checks and troubleshooting steps for Windows + WSL2.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
