## Description: <br>
Auto-discover and catalog all services in a codebase or organization by scanning Dockerfiles, docker-compose files, Kubernetes manifests, package metadata, systemd units, and Procfiles to generate a living service inventory with ownership, dependencies, tech stack, and health status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, platform engineers, and operations teams use this skill to inventory services across a codebase or organization, map dependencies and ownership, and generate service catalog, dependency graph, health, ownership, or drift reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated catalogs can expose sensitive internal metadata such as owner names, repository URLs, dependency URLs, environment-derived service references, and health results. <br>
Mitigation: Review and redact generated reports before sharing them outside the authorized team or environment. <br>
Risk: Discovery and ownership reports rely on repository metadata and heuristics such as CODEOWNERS, package metadata, and git history, which can be incomplete or stale. <br>
Mitigation: Validate service ownership, dependencies, and health endpoints with service owners before using the catalog for operational decisions. <br>
Risk: Health checks may probe local containers, system services, systemd units, and localhost endpoints. <br>
Mitigation: Run health checks only in environments where local probing is authorized and expected. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON service catalog data, Mermaid dependency diagrams, and shell commands for discovery and health checks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include repository paths, service names, owner identifiers, dependency URLs, health endpoints, and local health-check results.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
