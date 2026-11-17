## Description:

Author, run, and operate skelm pipelines: typed TypeScript workflows that combine deterministic code, LLM inference, and agent loops behind a default-deny permission model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottgl9](https://clawhub.ai/user/scottgl9)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold, author, validate, run, inspect, schedule, and debug skelm TypeScript pipelines, including workflows that combine code, LLM calls, MCP-backed tools, and agent steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold helper substitutes user-provided descriptions into executable TypeScript pipeline files.

Mitigation: Use trusted descriptions only, then inspect generated .pipeline.mts files before validation or execution.

Risk: Agent workflows may receive filesystem or shell permissions that are broader than a user expects.

Mitigation: Run agent steps inside an OS sandbox, container, or bounded workspace and keep permission scopes minimal.

Risk: Environment values inherited by agents or MCP servers may expose secrets.

Mitigation: Avoid placing real secrets in inherited .env values and scope any required credentials to the smallest necessary workflow.

Risk: Installing the gateway as a systemd service creates a persistent local service.

Mitigation: Install the systemd gateway only when persistent local operation is intended.

## Reference(s):

- [skelm documentation](https://scottgl9.github.io/skelm/)
- [skelm npm package](https://www.npmjs.com/package/skelm)
- [ClawHub skelm release](https://clawhub.ai/scottgl9/skills/skelm)
- [Pipeline Authoring Reference](references/pipeline-authoring.md)
- [Agent Step Reference](references/agent-step.md)
- [Permissions Reference](references/permissions.md)
- [Config Reference](references/config.md)
- [Gateway Reference](references/gateway.md)
- [CLI Reference](references/cli.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May scaffold or modify skelm pipeline and configuration files when the agent applies the provided workflow guidance.]

## Skill Version(s):

0.4.3 (source: server release metadata; artifact text also states skelm v0.4.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
