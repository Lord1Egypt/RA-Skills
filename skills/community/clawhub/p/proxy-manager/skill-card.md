## Description:

Manage the shared nginx-proxy Docker container and its network connections, with automatic discovery of app containers via VIRTUAL_HOST labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pereirajair](https://clawhub.ai/user/pereirajair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to start, stop, inspect, reload, and connect a local nginx-proxy Docker container for development app routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The proxy container mounts the host Docker socket, which gives the container access to Docker daemon state and warrants careful review.

Mitigation: Install only on a trusted local development machine, prefer a restricted docker-socket-proxy or explicit static routing where practical, and stop the proxy when it is not needed.

Risk: The proxy image is referenced by tag rather than digest.

Mitigation: Pin the container image by digest and review image updates before pulling a newer image.

## Reference(s):

- [Proxy Manager ClawHub page](https://clawhub.ai/pereirajair/skills/proxy-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Docker on Linux or macOS.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
