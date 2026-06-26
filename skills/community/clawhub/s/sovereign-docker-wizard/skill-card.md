## Description: <br>
Docker optimization expert. Analyzes Dockerfiles for security and performance, generates multi-stage builds, optimizes image size, creates docker-compose configs, and identifies container misconfigurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryudi84](https://clawhub.ai/user/ryudi84) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to analyze Dockerfiles, docker-compose files, and container architecture for security, performance, reliability, and maintainability. It produces scored findings and concrete before/after fixes for production-ready container deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose deployment code or Docker commands that materially change container behavior, exposed ports, volumes, privileges, or cleanup state. <br>
Mitigation: Review generated Dockerfiles, compose files, secrets handling, port mappings, volumes, privileged settings, Docker socket mounts, and cleanup commands before applying them. <br>
Risk: Docker prune examples can remove unused volumes, images, and build cache. <br>
Mitigation: Run cleanup commands only after confirming what data and cache will be removed in the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ryudi84/sovereign-docker-wizard) <br>
- [Publisher profile](https://clawhub.ai/user/ryudi84) <br>
- [Project homepage](https://github.com/ryudi84/sovereign-tools) <br>
- [Forge Tools](https://ryudi84.github.io/sovereign-tools/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, inline code, fenced Dockerfile, YAML, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include severity ratings, 0-100 dimension scores, size impact estimates, complete rewritten Dockerfiles, docker-compose files, .dockerignore recommendations, and CI/CD snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
