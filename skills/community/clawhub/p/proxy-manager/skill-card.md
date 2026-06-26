## Description: <br>
Manages the shared nginx-proxy Docker container and network connections for development app containers that expose VIRTUAL_HOST labels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pereirajair](https://clawhub.ai/user/pereirajair) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to start, stop, inspect, reload, and connect a local Docker nginx proxy for development app instances that expose VIRTUAL_HOST routes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proxy container reads Docker daemon state through a read-only Docker socket mount. <br>
Mitigation: Install and run only on trusted development machines, and review the Docker socket access before starting the proxy. <br>
Risk: The skill starts a persistent local Docker nginx proxy and binds host port 80 on localhost. <br>
Mitigation: Confirm local port 80 is appropriate for the environment, and stop the proxy when it is no longer needed. <br>
Risk: Connecting the proxy to project Docker networks can expose app routes through localhost. <br>
Mitigation: Prefer targeted connect commands for known instances; use auto-connect only after confirming the listed PROJECT_PREFIX networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pereirajair/proxy-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides local Docker proxy lifecycle guidance and command usage; no API keys are described in the evidence.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
