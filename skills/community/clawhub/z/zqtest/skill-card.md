## Description:

Typed knowledge graph for structured agent memory and composable skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ywqsimmon](https://clawhub.ai/user/ywqsimmon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create, query, relate, and validate typed entities for local agent memory, task planning, and cross-skill state sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local memory that other skills may read or write.

Mitigation: Install only in workspaces where shared local memory is acceptable, and review graph contents before relying on them.

Risk: Deleted entities remain in append-only JSONL history.

Mitigation: Do not store passwords, tokens, API keys, or sensitive personal data in the ontology graph.

Risk: Validation may not enforce every documented constraint before writes.

Mitigation: Run validation as a review aid and manually check important constraints before using graph data for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ywqsimmon/skills/zqtest)
- [Schema reference](references/schema.md)
- [Query reference](references/queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON, YAML, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace-local JSONL graph and YAML schema files when its CLI workflows are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
