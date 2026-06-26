## Description: <br>
Performs VPS health checks for CPU, memory, disk, network, uptime, and services, then helps generate Ollama-powered operational recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GBlockChainNetwork](https://clawhub.ai/user/GBlockChainNetwork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and system operators use this skill to audit Linux VPS health over SSH or local execution and review concise findings before taking maintenance action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SSH-level access to inspect target servers, which can expose sensitive operational data or affect high-impact systems if used with broad privileges. <br>
Mitigation: Use a non-root account with limited sudo rights, confirm the target host and key path before each run, and treat generated reports as sensitive operational data. <br>
Risk: The included SSH command disables strict host-key checking, weakening protection against connecting to an unexpected host. <br>
Mitigation: Verify host keys before execution and remove disabled host-key checking before using the script in a trusted environment. <br>
Risk: SSH parameters are accepted directly by the script, so incorrect or unsafe host, user, or key values can lead to unintended remote execution. <br>
Mitigation: Validate and quote SSH parameters and require explicit confirmation before running remote checks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GBlockChainNetwork/vps-health-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented diagnostic output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sensitive operational details from the target server.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
