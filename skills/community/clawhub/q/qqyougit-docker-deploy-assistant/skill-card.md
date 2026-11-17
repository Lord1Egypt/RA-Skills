## Description:

Docker部署助手 helps developers containerize and deploy applications by drafting Dockerfiles, docker-compose configurations, image build workflows, CI/CD guidance, security hardening checklists, monitoring practices, and troubleshooting steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqyougitcom](https://clawhub.ai/user/qqyougitcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create and review Docker deployment assets for Node.js, Python, Go, Java, frontend, and multi-service applications. It supports containerization, image optimization, docker-compose orchestration, CI/CD integration, security checks, monitoring, backup, rollback, and operational troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated deployment or rollback scripts may be copied into production without review.

Mitigation: Review and harden generated scripts before use, especially deployment, rollback, and cleanup logic.

Risk: Tag inputs, SSH heredocs, and cleanup commands can cause unsafe deployment behavior.

Mitigation: Validate tag inputs, avoid SSH heredoc interpolation, and remove or gate docker system prune -f.

Risk: Production deployments may rely on mutable image tags or committed secret files.

Mitigation: Pin production images by digest and keep real secrets in Docker Secrets or another secret manager instead of committed .env files.

## Reference(s):

- [Docker部署助手 detailed reference](references/details.md)
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/skills/qqyougit-docker-deploy-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Chinese Markdown with Dockerfile, YAML, shell, and configuration code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory deployment artifacts and commands that should be reviewed and hardened before production use.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
