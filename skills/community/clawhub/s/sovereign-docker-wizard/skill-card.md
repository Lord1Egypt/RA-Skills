## Description:

Docker optimization expert. Analyzes Dockerfiles for security and performance, generates multi-stage builds, optimizes image size, creates docker-compose configs, and identifies container misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryudi84](https://clawhub.ai/user/ryudi84)

### License/Terms of Use:

MIT

## Use Case:

Developers and DevOps engineers use this skill to review Dockerfiles, Docker Compose files, and container deployment plans. It produces scored findings, optimized Dockerfiles, Compose configurations, CI/CD snippets, remediation commands, and practical security guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Docker commands, cleanup commands, CI/CD workflows, or container configuration snippets can affect production hosts, repositories, images, secrets, or publishing credentials if executed without review.

Mitigation: Review generated commands and configuration before use, test changes away from production first, and avoid running cleanup or publishing commands against production systems until approved.

Risk: Copyable guidance involving container escape scenarios, Docker socket access, privileged containers, and secret handling could weaken host or credential security if applied outside a defensive review context.

Mitigation: Treat exploit demonstrations and Docker socket or secret-management advice as review material; remove privileged mode and socket mounts unless there is a specific, reviewed operational need.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryudi84/skills/sovereign-docker-wizard)
- [Project homepage](https://github.com/ryudi84/sovereign-tools)
- [Forge Tools](https://ryudi84.github.io/sovereign-tools/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with tables, Dockerfile and YAML code blocks, before/after examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity ratings, image-size impact estimates, and complete rewritten Docker-related files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
