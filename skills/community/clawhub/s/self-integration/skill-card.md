## Description:

Connect to external apps through Membrane so agents can send messages, create tasks, sync data, manage contacts, and perform API operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bratchenko](https://clawhub.ai/user/bratchenko)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to discover or create Membrane connections and actions, then run those actions against external services after user authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a high-privilege Membrane token and action data to a configurable API endpoint.

Mitigation: Keep MEMBRANE_API_URL fixed to the official HTTPS Membrane API unless intentionally operating a trusted deployment, and scope and rotate MEMBRANE_TOKEN carefully.

Risk: Connected-app actions can post messages, modify records, create tasks, or perform other state-changing operations.

Mitigation: Require explicit user approval before state-changing actions and review action inputs against the target app.

Risk: The ClawHub security verdict is suspicious because endpoint validation is not documented.

Mitigation: Review before installing and use only if the publisher and Membrane access model are trusted for the connected apps.

## Reference(s):

- [Self-Integration on ClawHub](https://clawhub.ai/bratchenko/skills/self-integration)
- [Membrane homepage](https://getmembrane.com)
- [Membrane dashboard](https://console.getmembrane.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Configuration]

**Output Format:** [Markdown with HTTP endpoints and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MEMBRANE_TOKEN and optionally MEMBRANE_API_URL; action outputs depend on connected apps.]

## Skill Version(s):

1.1.2 (source: ClawHub release metadata; artifact frontmatter metadata version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
