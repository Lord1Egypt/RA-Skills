## Description:

Analyzes Vue 2 and Vue 3 project component dependencies from an entry file, recursively maps component hierarchy, and reports component names, file paths, and props.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baozaibuding](https://clawhub.ai/user/baozaibuding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to understand Vue application structure, inspect component dependency relationships, and generate component maps for architecture review or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recursively reads Vue project source files to build the component map.

Mitigation: Use it only on repositories the user is comfortable having the agent inspect, and keep the analysis scoped to the intended project.

Risk: Generated component maps can be incomplete or inaccurate for unresolved aliases, dynamic components, missing files, or complex TypeScript patterns.

Mitigation: Review the Markdown, JSON, or Mermaid output against the source project before relying on it for architecture or refactoring decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baozaibuding/skills/vue-component-analyzer)
- [Implementation guide](artifact/implementation.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Code, Guidance]

**Output Format:** [Markdown tree, JSON structure, and Mermaid chart]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes component names, file paths, props, async markers, and circular dependency markers when detected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
