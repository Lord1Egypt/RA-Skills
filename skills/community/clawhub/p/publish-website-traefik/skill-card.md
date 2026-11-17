## Description:

Manages static website deployments to subdomains under *.sites.friendify.cloud using Traefik reverse proxy and Docker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailo037](https://clawhub.ai/user/mailo037)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy, list, and delete static websites on configured subdomains backed by Docker, Nginx, and Traefik.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill expects Docker authority and manages Docker-hosted static sites.

Mitigation: Use it only in an isolated environment and confirm Docker permissions, Traefik routing, and deployment paths before execution.

Risk: The skill includes deletion behavior for deployed site resources.

Mitigation: Add explicit delete confirmation or a backup workflow before making deletion scripts runnable.

Risk: The security summary says the Docker and deletion scripts are under-scoped.

Mitigation: Add strict subdomain validation, confine deployments to an approved directory, and protect state-file permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mailo037/skills/publish-website-traefik)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs deployment commands and operational guidance for Docker-backed static website publishing.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
