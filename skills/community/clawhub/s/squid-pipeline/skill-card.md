## Description:

Create, modify, and debug Squid YAML pipelines for multi-agent workflows with spawn adapters, gates, parallel execution, loops, branching, restart loops, sub-pipelines, structured approvals, and tests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dominno](https://clawhub.ai/user/dominno)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to author, review, validate, and test Squid pipeline YAML for agentic workflows that coordinate shell commands, sub-agents, approvals, branching, loops, and sub-pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled examples and generated pipelines may include high-impact repository, GitHub, Docker, Kubernetes, or deployment actions.

Mitigation: Do not run bundled examples unchanged in real repositories or deployment environments; use sandbox or dry-run first and require explicit gate approval conditions before side effects.

Risk: Pipeline commands may interpolate user-provided values into shell commands or deployment arguments.

Mitigation: Validate or safely pass shell arguments, keep tests beside each pipeline, and run Squid validation before execution.

Risk: Authenticated agent, GitHub, Docker, or Kubernetes credentials can affect production resources if exposed to generated workflows.

Mitigation: Use least-privileged credentials in isolated environments and avoid production credentials unless the workflow has been reviewed and approved.

Risk: The server security verdict is suspicious because approval enforcement in examples and templates is inconsistent.

Mitigation: Review each workflow for gate-before-side-effect behavior, explicit approval checks after gates, retries on network calls, bounded loops, and downstream success guards.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dominno/skills/squid-pipeline)
- [Step Types Reference](references/step-types.md)
- [Workflow Patterns](references/patterns.md)
- [Testing Reference](references/testing.md)
- [Squid Getting Started](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/getting-started.md)
- [Squid Step Types Docs](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/step-types.md)
- [Squid Agent Adapters](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/adapters.md)
- [Squid Workflow Patterns Docs](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/workflow-patterns.md)
- [Squid Testing Guide](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/testing.md)
- [Squid Migration Guide](https://raw.githubusercontent.com/dominno/squid/refs/heads/main/docs/migration.md)
- [Squid Workflow Examples](https://github.com/dominno/squid-workflows)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML pipeline and test snippets plus inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be reviewed, validated with Squid, and tested before use against real repositories or deployment targets.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
