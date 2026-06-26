## Description: <br>
ResmoteConsole helps an agent start, stop, check, and validate a browser-accessible remote console for Claude Code or other CLI tools through ttyd and an SSH tunnel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HaibaraAiAPTX](https://clawhub.ai/user/HaibaraAiAPTX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to expose a local development shell in a mobile or browser workflow, then manage startup, shutdown, status checks, and configuration validation through bundled Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A browser-accessible ttyd console can expose interactive shell access to the host. <br>
Mitigation: Use ttyd authentication and HTTPS, or restrict access through a VPN or firewall allowlist before starting the console. <br>
Risk: The default configuration includes a claude-bypass command that can skip normal permission checks. <br>
Mitigation: Remove the claude-bypass command and avoid using this skill with production systems or sensitive projects. <br>
Risk: ttyd and SSH tunnel processes may remain active after a session. <br>
Mitigation: Run the bundled status and stop scripts after each session to confirm the remote console and tunnel are stopped. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HaibaraAiAPTX/remote-console) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact config.json](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill directs the agent to use Python helper scripts for console lifecycle management and configuration validation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
