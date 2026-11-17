## Description:

Deploys TeslaMate, a self-hosted Tesla vehicle data logger and Grafana dashboard, to a local machine or remote Debian-family Linux server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[martinbj2008](https://clawhub.ai/user/martinbj2008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and Tesla owners use this skill to install TeslaMate on an existing local or remote Debian-family host, run pre-flight and health checks, and produce a usage document with service access details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad privileged deployment steps on the target host.

Mitigation: Install only on a dedicated, non-shared host after reviewing the bundled scripts.

Risk: Default secrets and service credentials are weak for exposed deployments.

Mitigation: Replace all default secrets and credentials before relying on the deployment.

Risk: TeslaMate, Grafana, and MQTT ports may be exposed directly after startup.

Mitigation: Restrict ports with a firewall, loopback binding, or reverse proxy before startup.

Risk: Password-mode SSH and disabled host-key verification can weaken deployment security.

Mitigation: Prefer SSH key authentication and verify the host independently before deployment.

Risk: The GitHub image fallback relies on third-party pre-packaged Docker image files.

Mitigation: Avoid the fallback unless you independently trust and verify the downloaded images.

Risk: Tesla tokens and API keys are sensitive credentials.

Mitigation: Do not paste Tesla tokens into chat or visible terminal prompts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/martinbj2008/skills/teslamate-deploy)
- [TeslaMate Deploy Troubleshooting](references/troubleshooting.md)
- [Tesla Developer API Access](https://developer.tesla.com/)
- [TeslaMate Backup Guide](https://docs.teslamate.org/docs/guides/backup)
- [Fallback Docker Image Repository](https://github.com/martinbj2008/docker_images)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash code blocks and a generated usage document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local or SSH-based deployment steps, Docker Compose configuration guidance, health checks, and operational warnings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
