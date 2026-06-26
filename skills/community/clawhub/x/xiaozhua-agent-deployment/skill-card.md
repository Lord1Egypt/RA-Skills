## Description: <br>
Guides agents and developers through deploying and managing an OpenClaw-based AI agent on WSL2/Linux, including GitHub Copilot authentication, gateway startup, workspace initialization, port configuration, and common recovery steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mirowangl-ops](https://clawhub.ai/user/mirowangl-ops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install OpenClaw, authenticate GitHub Copilot, configure and start a local gateway, initialize workspace documentation, and troubleshoot common deployment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands download and execute third-party installation tooling. <br>
Mitigation: Inspect the remote nvm install script and confirm the OpenClaw npm package before installing. <br>
Risk: Gateway access can be exposed if tokens are leaked or the service is bound beyond localhost without controls. <br>
Mitigation: Keep gateway tokens private and leave the gateway bound to localhost unless remote access is intentionally secured. <br>
Risk: Workspace markdown files can accidentally capture secrets or sensitive personal data. <br>
Mitigation: Avoid putting secrets or sensitive personal data in USER.md, SOUL.md, TASKS.md, COLLABORATION.md, or related workspace files. <br>


## Reference(s): <br>
- [nvm install script](https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh) <br>
- [ClawHub skill page](https://clawhub.ai/mirowangl-ops/xiaozhua-agent-deployment) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash code blocks and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses placeholders for local port and token values that users replace for their environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
