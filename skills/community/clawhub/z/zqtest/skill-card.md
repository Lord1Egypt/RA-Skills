## Description: <br>
Typed knowledge graph for structured agent memory and composable skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ywqsimmon](https://clawhub.ai/user/ywqsimmon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, query, relate, and validate typed workspace entities such as people, projects, tasks, events, documents, and notes. It is useful when shared local memory or cross-skill state needs a structured graph rather than ad hoc text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill intentionally persists shared workspace memory in local ontology files. <br>
Mitigation: Review memory/ontology files periodically and avoid using this skill for information that should not be shared across agents or workflows. <br>
Risk: Ontology records can describe accounts or credentials by reference. <br>
Mitigation: Store only secret references, not raw passwords, tokens, keys, or other private secrets. <br>
Risk: Broad remember requests can add excessive or unintended personal or project context to the graph. <br>
Mitigation: Confirm the intended scope before recording sensitive or long-lived memory. <br>


## Reference(s): <br>
- [Ontology Schema Reference](references/schema.md) <br>
- [Query Reference](references/queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, Python, YAML, JSON, and JSONL examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local memory/ontology files when the provided CLI workflows are executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
