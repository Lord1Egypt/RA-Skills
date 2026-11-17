## Description:

A lightweight workflow orchestration engine for multi-phase task coordination with routing, phase execution, and exception handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to coordinate multi-phase development workflows, route tasks by change metadata, validate phase gates, handle workflow exceptions, and persist workflow state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow state may be saved to local JSON or YAML files that could contain sensitive project context.

Mitigation: Do not store secrets or sensitive project details in persisted workflow files; review saved state before sharing or committing it.

Risk: The security guidance identifies a functional bug in the exception-handling import path.

Mitigation: Verify and fix the exception-handling import path before relying on exception handling in production workflows.

Risk: The skill is described by security guidance as a lightweight local workflow-state helper rather than a full production orchestration engine.

Mitigation: Use it for local workflow tracking unless additional operational controls, monitoring, and reliability checks are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terr123123/skills/workflow-orchestration)
- [Usage Guide](docs/usage-guide.md)
- [API Reference](docs/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Code, Configuration, Guidance]

**Output Format:** [Python objects and serialized JSON or YAML workflow state, with Markdown documentation and inline code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workflow instance status, phase results, routing decisions, exception handling results, and saved workflow state.]

## Skill Version(s):

1.0.0 (source: server release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
