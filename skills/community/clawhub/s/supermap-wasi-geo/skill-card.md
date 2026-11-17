## Description:

Performs local GIS geometry analysis with SuperMap WebAssembly, including buffer, convex hull, intersection, union, erase, clip, distance, and related GeoJSON operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nestone](https://clawhub.ai/user/nestone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and GIS engineers use this skill to run local SuperMap WebAssembly geometry operations against GeoJSON inputs from the command line or Node.js code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release bundles a SuperMap WebAssembly binary that users must trust locally.

Mitigation: Install only when local GIS geometry processing is needed and review the bundled files through the normal release security process before deployment.

Risk: Geometry results may require review for multipart and MultiPoint edge cases.

Mitigation: Use intended GeoJSON inputs and review generated GeoJSON or JSON results before relying on them in downstream workflows.

Risk: Documentation and runtime messages are primarily Chinese-language.

Mitigation: Ensure operators can understand the prompts, examples, and errors before using the skill in production workflows.

## Reference(s):

- [SuperMap WASI Geometry usage guide](references/usage.md)
- [ClawHub skill page](https://clawhub.ai/nestone/skills/supermap-wasi-geo)

## Skill Output:

**Output Type(s):** [shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON or GeoJSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI operations read GeoJSON strings or files and return GeoJSON Features or JSON Result objects; outputs can be written to stdout or a file.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter and package.json remain 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
