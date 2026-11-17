## Description:

Manage sites.friendify.cloud deployment with auth flow, pending states, and owner-based dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mailo037](https://clawhub.ai/user/mailo037)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site operators use this skill to create and manage sites.friendify.cloud deployments through an authenticated agent workflow. It supports pending registration, owner-scoped dashboards, privacy changes, and deletion controls for verified site owners.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create live Docker and Traefik-backed sites from a Telegram-triggered request.

Mitigation: Require explicit user confirmation before deployment and install it only in environments where agent-driven site creation is intended.

Risk: The skill includes actions that can change site privacy or delete owner-managed sites.

Mitigation: Require explicit confirmation before privacy changes or deletion, and rely on the documented owner verification and OpenClaw gateway authentication.

Risk: The workflow depends on real Docker, Traefik, Telegram, and OpenClaw gateway access.

Mitigation: Review the skill before installation and restrict credentials and runtime access to the intended Friendify management environment.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, markdown]

**Output Format:** [Markdown with inline commands, API request details, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENCLAW_GATEWAY_TOKEN for OpenClaw gateway-authenticated management actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
