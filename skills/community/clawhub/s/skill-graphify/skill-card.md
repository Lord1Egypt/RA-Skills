## Description:

Turns folders of code, docs, papers, or images into queryable knowledge graphs through a cross-platform wrapper for the graphify CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flobo3](https://clawhub.ai/user/flobo3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to map relationships across unfamiliar codebases or mixed document folders, inspect generated graph artifacts, and query how concepts connect.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically install the unpinned third-party Python package graphifyy.

Mitigation: Install only in an isolated virtual environment or sandbox, and review or pin the graphifyy dependency before use.

Risk: The skill can analyze and write graph outputs in arbitrary target folders.

Mitigation: Run it only on explicit folders approved for indexing, and review graph.json and GRAPH_REPORT.md before sharing generated outputs.

## Reference(s):

- [Skill Graphify on ClawHub](https://clawhub.ai/flobo3/skills/skill-graphify)
- [graphify upstream project](https://github.com/safishamsi/graphify)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated graph/report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Build commands produce graph.html, graph.json, GRAPH_REPORT.md, and cache files in graphify-out/.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
