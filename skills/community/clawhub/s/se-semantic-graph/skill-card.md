## Description:

Stores software engineering knowledge such as personas, requirements, constraints, architecture, module logic, and decisions in a graph so agents can retrieve targeted context when fixing bugs, adding features, or refactoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littlelollipop](https://clawhub.ai/user/littlelollipop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to maintain a project-level semantic graph and query upstream rationale or downstream impact before code changes. It is intended for project planning, debugging, feature work, and refactoring where concise traceability context is more useful than broad source dumping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable third-party dependency code may execute locally through the configured graph engine path.

Mitigation: Review and pin the lobster-memory and axolotl revisions before installation, and treat SE_SEMANTIC_ENGINE as a trusted-code path.

Risk: Project graph entries could accidentally capture secrets, proprietary source, or excessive document content.

Mitigation: Record only field-level summaries and references, and review graph content before sharing or publishing.

Risk: Using a shared graph directory can mix context between unrelated projects.

Mitigation: Set SE_SEMANTIC_DIR to a dedicated project-scoped directory for each workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/littlelollipop/skills/se-semantic-graph)
- [Server-Resolved Source Repository](https://github.com/LittleLollipop/se-semantic-graph)
- [lobster-memory Dependency](https://github.com/LittleLollipop/lobster-memory.git)
- [Node Templates](artifact/templates/node-templates.md)
- [Onboarding Dialogue Template](artifact/templates/onboarding-dialogue.md)
- [Requirement Dimensions Template](artifact/templates/requirement-dimensions.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands and structured graph records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses project-scoped graph files and field-level summaries; avoids full source or document dumps.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
