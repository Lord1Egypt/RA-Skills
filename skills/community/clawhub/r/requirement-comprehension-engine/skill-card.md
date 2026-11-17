## Description:

Advanced requirement comprehension and skill orchestration engine that analyzes complex or multi-step user requests, determines which skills to invoke and in what order, and builds task decomposition trees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bustes01](https://clawhub.ai/user/bustes01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to parse ambiguous or multi-intent requests, decompose them into actionable sub-goals, select appropriate companion skills, and coordinate sequential or parallel handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may step in for broad or ambiguous requests and coordinate other skills.

Mitigation: Review the proposed decomposition and orchestration plan, and ask for clarification before executing unclear multi-step actions.

Risk: The memory guidance is not suitable for secrets or personal data.

Mitigation: Keep stored preferences and logs low sensitivity, avoid secrets and personal data in skill memory, and use appropriate secret storage outside the skill.

Risk: The skill delegates memory management and self-iteration behavior to companion skills.

Mitigation: Review the required companion skills separately before relying on delegated memory, logging, or update decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bustes01/skills/requirement-comprehension-engine)
- [ClawDIS homepage](https://clawhub.ai/BusTes01/requirement-comprehension-engine)
- [Memory Management Reference](references/memory-management.md)
- [Orchestration Patterns Reference](references/orchestration-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or structured text with optional handoff templates, task decomposition trees, and lightweight JSON-style execution logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces orchestration guidance and planning artifacts for an agent; companion skill behavior depends on the installed skills available in context.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
