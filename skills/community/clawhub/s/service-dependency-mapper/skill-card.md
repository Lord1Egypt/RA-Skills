## Description: <br>
Auto-discovers and maps service dependencies from code, configs, and runtime data, then generates dependency graphs, identifies critical paths and single points of failure, and assesses service blast radius. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to map service dependencies from code, configuration, and runtime data, then identify critical paths, single points of failure, and blast radius during architecture review or incident planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Runtime discovery can expose internal service names, endpoints, ports, and topology. <br>
Mitigation: Use approved repositories and a least-privileged read-only Kubernetes context, confirm the target cluster before runtime discovery, and redact infrastructure details before sharing generated maps. <br>
Risk: The artifact is tagged with unrelated purchase and crypto capability labels. <br>
Mitigation: Do not grant purchase or crypto authority based on this skill; scope the agent to read-oriented service mapping actions only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/service-dependency-mapper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and diagram-format examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces dependency maps, blast-radius tables, critical-path notes, architecture health guidance, and diagram formats such as Mermaid, DOT, PlantUML, and D2.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
