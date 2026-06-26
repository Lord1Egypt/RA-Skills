## Description: <br>
Superviser Ressources monitors CPU, RAM, Docker containers, and site health, and can report status or restart services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to ask an agent for host resource, Docker, and website health status, and to request targeted service restarts. It is intended for operational monitoring workflows where host and container visibility is explicitly permitted. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for operational visibility into host resources and Docker state. <br>
Mitigation: Install only in environments where an agent is explicitly allowed to inspect host and container health. <br>
Risk: The release describes autonomous restarts and self-healing without clear limits or safety controls. <br>
Mitigation: Define allowed services, approval requirements, rate limits, backoff behavior, logs, and a clear disable path before enabling automatic remediation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mrnsmh/supervisorclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text operational status and service-management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include host resource percentages, Docker container status, HTTP target status, and service restart instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
