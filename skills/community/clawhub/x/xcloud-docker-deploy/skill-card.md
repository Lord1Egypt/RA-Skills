## Description: <br>
xCloud Docker Deploy v1.4.1 is a confirmation-gated skill for preparing projects for xCloud by generating Docker and GHCR deployment files, fixing xCloud port rules, and routing live API work only after separate explicit token consent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asif2bd](https://clawhub.ai/user/asif2bd) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and DevOps engineers use this skill to inspect application projects, decide whether xCloud native deployment or Custom Docker is appropriate, and prepare xCloud-ready Docker Compose, GHCR workflow, and environment guidance after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated deployment files, workflows, hooks, or deployment steps could affect a real xCloud environment if applied without review. <br>
Mitigation: Review the exact generated files, use a branch or pull request, confirm staging versus production, and verify backups before applying changes. <br>
Risk: API tokens, webhook secrets, or deployment credentials could enable live actions if added casually. <br>
Mitigation: Add secrets only for a specifically approved deployment action, prefer least-privilege short-lived credentials, and do not print, store, log, or commit tokens. <br>


## Reference(s): <br>
- [GitHub Repository](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill) <br>
- [Latest Release](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/releases/tag/v1.4.1) <br>
- [xCloud Agent Skills](https://app.xcloud.host/agent/skills) <br>
- [xCloud API Docs](https://app.xcloud.host/api/v1/docs) <br>
- [Security Notes](https://github.com/Asif2BD/xCloud-Docker-Deploy-Skill/blob/main/SECURITY.md) <br>
- [xCloud Constraints](references/xcloud-constraints.md) <br>
- [xCloud Deploy Paths](references/xcloud-deploy-paths.md) <br>
- [Scenario: Build From Source](references/scenario-build-source.md) <br>
- [Scenario: Proxy Conflict](references/scenario-proxy-conflict.md) <br>
- [Scenario: Multi-Service Build](references/scenario-multi-service-build.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, Docker Compose, GitHub Actions, environment-variable examples, shell commands, and deployment steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable deployment-preparation output and does not deploy or call live APIs by itself.] <br>

## Skill Version(s): <br>
1.4.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
