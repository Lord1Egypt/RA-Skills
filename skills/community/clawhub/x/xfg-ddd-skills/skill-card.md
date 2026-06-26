## Description: <br>
DDD hexagonal architecture skill pack for Domain, Case, and Infrastructure layer design patterns, code templates, and Docker deployment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzhengwei](https://clawhub.ai/user/fuzhengwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design and implement Java applications with DDD and hexagonal architecture, including entities, aggregates, value objects, repositories, services, case orchestration, infrastructure adapters, and deployment steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to generate files and scaffold Java DDD projects in a user-selected directory. <br>
Mitigation: Confirm the target directory before execution, run the scaffolding script interactively, and review generated files before committing or deploying them. <br>
Risk: Deployment guidance can lead to Docker changes and database initialization that may affect existing services or data. <br>
Mitigation: Do not run docker stop/rm commands or initialization SQL against production or existing data without backups, a clear rollback plan, and explicit operator approval. <br>
Risk: Examples include sample passwords and root-style database credentials. <br>
Mitigation: Replace all sample passwords, avoid root database credentials, and verify environment-specific secrets before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fuzhengwei/xfg-ddd-skills) <br>
- [Publisher Profile](https://clawhub.ai/user/fuzhengwei) <br>
- [README](README.md) <br>
- [DDD Architecture Reference](references/architecture.md) <br>
- [Domain Layer Design Guide](references/domain-design-guide.md) <br>
- [Domain Layer Design Patterns](references/domain-patterns.md) <br>
- [Infrastructure Layer Patterns](references/infrastructure-patterns.md) <br>
- [DevOps Deployment Guide](references/devops-deployment.md) <br>
- [Docker Images Reference](references/docker-images.md) <br>
- [Docker Image Pusher Repository](https://github.com/fuzhengwei/docker-image-pusher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, configuration, and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide interactive Java DDD project scaffolding after the user confirms the target directory.] <br>

## Skill Version(s): <br>
2.2.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
