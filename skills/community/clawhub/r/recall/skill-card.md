## Description:

Recall teaches agents to check local skills, workspace files, tools, and memory before answering, using knowledge access patterns to reduce hallucinated or stale responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crewhaus](https://clawhub.ai/user/crewhaus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Recall to make coding or operations agents inspect local context, tool docs, and memory before answering or acting. It is aimed at reducing hallucinations, stale context, and missed tool usage in ClawHub workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to proactively read broad agent-readable workspace memory, identity, task, tool, and skill files that contain sensitive personal, customer, security, or business context.

Mitigation: Install only in workspaces where that context loading is acceptable, keep secrets out of agent-readable files, and require explicit approval before accessing sensitive locations.

Risk: The skill encourages writing session notes for future use, which may persist sensitive information without clear retention controls.

Mitigation: Review memory and task updates regularly, define retention and redaction expectations, and prefer explicit approval before storing personal, customer, security, or business-sensitive information.

## Reference(s):

- [Recall Skill Page](https://clawhub.ai/crewhaus/skills/recall)
- [CrewHaus Certification](https://crewhaus.ai/certify)
- [Knowledge Access Patterns](references/knowledge-patterns.md)
- [Session Checklist](references/session-checklist.md)
- [The 7 Deadly Sins of Agent Knowledge Access](references/anti-patterns.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with checklists, examples, and reference patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill does not define executable scripts; it guides agents to inspect workspace context and update memory or task files when appropriate.]

## Skill Version(s):

1.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
