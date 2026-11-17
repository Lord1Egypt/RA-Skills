## Description:

Structured spec-first development workflow with multi-role expert review gates for clarifying requirements, authoring specs, generating code from specs, verifying with tests, and keeping specs and code in sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhuaustc](https://clawhub.ai/user/xhuaustc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a spec-first coding workflow for non-trivial features or systems: clarify scope, write requirements, design, and task specs, generate code and tests, verify behavior, and evolve specs alongside implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify project files while generating specs, code, tests, status documents, and implementation maps.

Mitigation: Review generated diffs and run the requested local verification commands before merging or deploying changes.

Risk: Review gates can auto-advance when no Critical or Major issues are found.

Mitigation: Set review preferences to require manual approval when human gate control is needed.

Risk: Spec gaps or incomplete requirements can lead to placeholder behavior or implementation choices that need later review.

Mitigation: Track SPEC-GAP items, resolve them during verification, and keep specs and implementation maps updated before completion.

## Reference(s):

- [Expert Review Protocol](references/expert-review-protocol.md)
- [Spec Lifecycle Management](references/spec-lifecycle.md)
- [Spec Coding - Core Templates](references/templates.md)
- [Spec Coding - Lifecycle & Review Templates](references/templates-lifecycle.md)
- [UI De-AI Aesthetic Checklist](references/ui-design-guidelines.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated files, code snippets, shell commands, and verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or modify project files under specs/, source code, tests, design previews, status documents, implementation maps, and task-level commits.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
