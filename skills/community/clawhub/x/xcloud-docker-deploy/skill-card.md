## Description:

xCloud Docker Deploy helps agents prepare projects for xCloud by detecting application stacks, generating Docker and GHCR deployment files, normalizing xCloud port rules, and gating live API work behind explicit user consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asif2bd](https://clawhub.ai/user/asif2bd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to adapt applications and existing Docker Compose projects for xCloud deployment. It helps prepare compose files, Dockerfile guidance, GitHub Actions workflows, environment templates, and xCloud deployment steps after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated GitHub Actions workflows can publish container images or trigger deployments with insufficient review.

Mitigation: Pin external actions to reviewed commit SHAs and require protected environments or manual approvals before production deploys.

Risk: Deployment webhooks or xCloud API tokens could be exposed or used beyond the intended operation.

Mitigation: Pass secrets through environment variables or secret stores, request least-privilege tokens only for named live operations, and avoid direct shell interpolation.

Risk: Production deploys, migrations, or cache changes can affect live sites and data.

Mitigation: Verify backups, prefer staging validation, and require a final confirmation before production-impacting actions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/asif2bd/skills/xcloud-docker-deploy)
- [GitHub Repository](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill)
- [Latest Release](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1)
- [Security Notes](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/blob/main/SECURITY.md)
- [xCloud Agent Skills](https://app.xcloud.host/agent/skills)
- [xCloud API Docs](https://app.xcloud.host/api/v1/docs)
- [xCloud Docker Deployment Constraints](references/xcloud-constraints.md)
- [xCloud Deployment Paths](references/xcloud-deploy-paths.md)
- [Build-from-Source Scenario](references/scenario-build-source.md)
- [Proxy and Multi-Port Scenario](references/scenario-proxy-conflict.md)
- [Multi-Service Build Scenario](references/scenario-multi-service-build.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, Dockerfile, shell command, and step-by-step deployment sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Docker Compose files, GitHub Actions workflows, .env.example templates, and xCloud deployment steps for review before use.]

## Skill Version(s):

1.4.1 (source: server release evidence, frontmatter, skill.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
