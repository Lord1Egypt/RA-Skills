## Description:

Deployment Kit helps agents prepare Docker-based OpenClaw deployments with CI/CD guidance, Docker Compose configuration, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and deployment engineers use this skill to prepare OpenClaw services for containerized deployment, configure Docker Compose services, run health checks, and outline CI/CD release steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Docker command strings can be built from configuration values and executed on the host.

Mitigation: Review before installing on any real host; replace shell-string execution with argument-based process execution and validate image, container, port, registry, and log parameters.

Risk: Deployment commands can start, stop, remove, and persist Docker services and volumes.

Mitigation: Use only in a controlled environment until production deployments require explicit approval and operator review.

Risk: Container images are referenced with mutable tags such as latest.

Mitigation: Pin images to immutable versions or digests before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-deployment-kit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript code, and Docker Compose configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include host-level Docker operations and deployment configuration that should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
