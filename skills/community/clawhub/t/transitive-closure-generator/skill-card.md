## Description:

Computes transitive closure over graph edges for reachability, dependency, hierarchy, and knowledge-graph expansion workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fisa712](https://clawhub.ai/user/fisa712)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to infer reachable node pairs, expand dependency or hierarchy chains, and support impact analysis over graph-shaped data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised cycle detection, Floyd-Warshall, incremental, memoization, and materialization support may not match the implemented behavior.

Mitigation: Review and validate the implementation on representative graphs before relying on it for dependency or hierarchy validation.

Risk: Applying transitive closure to a relation that is not actually transitive can produce misleading inferred edges.

Mitigation: Confirm the relation semantics and test with small known examples before using generated closure data downstream.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fisa712/skills/transitive-closure-generator)
- [Publisher Profile](https://clawhub.ai/user/fisa712)
- [ClawHub Homepage](https://clawhub.com)
- [Transitive Closure Algorithms & Patterns](references/closure-patterns.md)
- [Transitive Closure Examples](examples/closure-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with Python code examples and optional graph-analysis results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local graph-analysis utility; no credentials, MCP tools, or external API calls were detected.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
