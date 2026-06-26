## Description: <br>
Deployment Kit helps agents guide Docker-based OpenClaw deployment with Docker Compose, CI/CD pipeline steps, health checks, security scanning, and optional monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to containerize and deploy OpenClaw services, run health checks, and prepare CI/CD and monitoring guidance for production-style environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configurable values are interpolated into shell commands that can change Docker state. <br>
Mitigation: Review before installing on machines with important Docker access and use only trusted configuration values. <br>
Risk: Monitoring and service ports may be exposed if deployed without network controls. <br>
Mitigation: Avoid exposing monitoring ports publicly; use firewall rules, private networks, and HTTPS for production deployments. <br>
Risk: External container images may change when version tags are not pinned. <br>
Mitigation: Pin external image versions before production use. <br>
Risk: Production use needs operational controls beyond the bundled deployment helpers. <br>
Mitigation: Add branch protection, deployment approvals, rollback steps, and cleanup procedures before using this for production deployment. <br>


## Reference(s): <br>
- [Deployment Kit ClawHub Release](https://clawhub.ai/yuyonghao-123/yuyonghao-deployment-kit) <br>
- [Deployment Kit Source Instructions](artifact/SKILL.md) <br>
- [Docker Compose Configuration](artifact/docker/docker-compose.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, JavaScript, Dockerfile, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Docker and deployment commands that alter local containers, images, ports, and runtime state.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, artifact package.json, and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
