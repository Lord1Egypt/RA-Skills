## Description: <br>
WSL2 HTTP proxy setup via Windows host. Automatically detects proxy running on Windows (Clash/V2Ray/SS/Surge etc.) and configures WSL2 environment variables. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ham-5on](https://clawhub.ai/user/ham-5on) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers working in WSL2 use this skill to detect a Windows-hosted HTTP proxy, set shell proxy environment variables, check connectivity, and clear those settings when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command-line traffic may be routed through a Windows-hosted proxy after the environment variables are set. <br>
Mitigation: Install only when WSL2 traffic is intended to use the Windows proxy, inspect the detected host and port before eval, and persist shell snippets only when ongoing proxy routing is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ham-5on/wsl-proxy) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may emit shell exports for the current session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
