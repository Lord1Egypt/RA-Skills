## Description:

Spec-task guides agents through a structured task lifecycle for complex or delegated work, requiring task briefs, specifications, plans, checklists, status transitions, verification, and archiving.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leonardo-lb](https://clawhub.ai/user/leonardo-lb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use spec-task to organize complex or delegated work into traceable task artifacts, explicit lifecycle states, acceptance criteria, and archival records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill strongly shapes agent workflow and may add overhead or inappropriate process requirements to simple tasks.

Mitigation: Install it only where structured task lifecycle enforcement is desired, and review whether its required brief, spec, plan, checklist, and state transitions fit the workspace.

Risk: The skill can create persistent task history, lessons, logs, verification records, and archive files that may retain sensitive project details.

Mitigation: Confirm the configured memory and archive paths before use, review archive contents before approval, and disable or avoid history and lesson generation for sensitive projects.

Risk: The release changelog states the skill has been deprecated due to unstable factors.

Mitigation: Prefer the replacement plugin with the same name for new deployments, or test this skill in a non-sensitive workspace before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leonardo-lb/skills/spec-task)
- [OpenSpec concept mapping](artifact/reference/openspec-mapping.md)
- [Status.yaml format reference](artifact/reference/status-format.md)
- [Agent task schema](artifact/schemas/agent-task/schema.yaml)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown task documents, YAML status/configuration, and concise tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured task artifacts such as brief.md, spec.md, plan.md, checklist.md, status.yaml, logs, verification records, and optional archive notes.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
