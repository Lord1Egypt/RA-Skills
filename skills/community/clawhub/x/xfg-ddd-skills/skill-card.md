## Description:

xfg-ddd-skills helps agents design and implement DDD hexagonal architectures, generate Java project structures and templates, and provide Docker-based deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuzhengwei](https://clawhub.ai/user/fuzhengwei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide domain-driven design, create DDD project scaffolds, generate layered Java code patterns, and prepare Docker or docker-compose deployment steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated projects, Maven archetype sources, Docker images, Compose files, SQL scripts, and credentials may carry supply-chain or unsafe-default risks.

Mitigation: Treat templates as untrusted until provenance is verified, dependencies and images are reviewed, credentials are replaced, service bindings are restricted, and SQL is checked against the target environment.

Risk: Deployment guidance may execute shell commands, build images, start services, or initialize databases in a real environment.

Mitigation: Run commands in an isolated workspace first, confirm target paths and environments with the user, review generated files before deployment, and avoid destructive SQL on existing data.

Risk: Server-resolved provenance is unavailable for this release.

Mitigation: Do not rely on inferred source repository provenance; verify publisher, release source, and artifacts through ClawHub and trusted project channels before production use.

## Reference(s):

- [Skill README](README.md)
- [Architecture overview](references/architecture.md)
- [Domain design guide](references/domain-design-guide.md)
- [Domain patterns](references/domain-patterns.md)
- [Infrastructure patterns](references/infrastructure-patterns.md)
- [DevOps deployment](references/devops-deployment.md)
- [Docker images](references/docker-images.md)
- [Project structure](references/project-structure.md)
- [Entity design](references/entity.md)
- [Aggregate design](references/aggregate.md)
- [Value object design](references/value-object.md)
- [Repository pattern](references/repository.md)
- [Port and adapter pattern](references/port-adapter.md)
- [Domain service](references/domain-service.md)
- [Case layer orchestration](references/case-layer.md)
- [Trigger layer](references/trigger-layer.md)
- [Infrastructure layer](references/infrastructure-layer.md)
- [Naming conventions](references/naming.md)
- [Docker image pusher repository referenced by Docker image guidance](https://github.com/fuzhengwei/docker-image-pusher)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create scaffolded project files when the bundled shell script is executed after user confirmation.]

## Skill Version(s):

2.2.3 (source: release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
