## Description:

Mission Control connects agents to a local operations dashboard for reporting task progress, publishing documents, requesting approvals, submitting project requests, and coordinating reviews through documented HTTP events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisval1](https://clawhub.ai/user/louisval1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to let agents report lifecycle events, submit work for review, request approvals, publish durable documents, and receive human decisions through a Mission Control dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default dashboard exposes powerful management and agent-dispatch paths without production-grade authentication.

Mitigation: Run it only in a trusted local environment, or add real authentication and network controls before exposing it beyond the local machine.

Risk: Non-local traffic can expose hook events, approvals, review content, and agent-dispatch data if transported without protection.

Mitigation: Use HTTPS/WSS and bind services to loopback or a protected network unless the deployment has been reviewed and hardened.

Risk: Library rendering and dispatch behavior can affect what operators and agents see or act on.

Mitigation: Review Library rendering and agent-dispatch behavior before using the skill with sensitive content or production workflows.

## Reference(s):

- [Mission Control ClawHub listing](https://clawhub.ai/louisval1/skills/tsu-mission-control)
- [README](artifact/README.md)
- [Getting Started](artifact/docs/GETTING-STARTED.md)
- [API Reference](artifact/docs/API-REFERENCE.md)
- [Hook Events](artifact/docs/HOOK-EVENTS.md)
- [Library Guide](artifact/docs/LIBRARY-GUIDE.md)
- [Docker Guide](artifact/docs/DOCKER.md)
- [Troubleshooting](artifact/docs/TROUBLESHOOTING.md)
- [Changelog](artifact/docs/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [guidance, JSON payloads, shell commands, configuration, markdown]

**Output Format:** [Markdown instructions with JSON examples, HTTP endpoint details, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for local dashboard integration; no model weights or datasets are produced.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
