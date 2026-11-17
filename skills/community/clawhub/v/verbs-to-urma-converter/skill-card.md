## Description:

Migrates RDMA Verbs (libibverbs) applications to the URMA API, including API mapping, data structure conversion, build updates, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derricjs](https://clawhub.ai/user/derricjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert RDMA, InfiniBand, RoCE, or libibverbs codebases to URMA while preserving original files and producing migrated output, build changes, and verification notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated URMA examples or migrations may use unsafe remote-memory token handling.

Mitigation: Review generated token handling before installation or deployment, replace fixed tokens, and ensure exported memory and access flags are limited to the intended use.

Risk: Generated client/server examples may expose unauthenticated network control channels.

Mitigation: Add authenticated encrypted control channels and bind listeners only to trusted interfaces before using generated code in production.

Risk: Incorrect URMA migration guidance can create runtime security, resource lifecycle, or memory-access issues.

Mitigation: Have developers who understand the URMA security model audit generated code and follow the skill's phase-based verification checklist before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derricjs/skills/verbs-to-urma-converter)
- [URMA API Mapping Reference](artifact/references/mapping.md)
- [URMA Code Patterns and Best Practices](artifact/references/patterns.md)
- [Common Pitfalls and Solutions](artifact/references/pitfalls.md)
- [URMA Complete Working Example](artifact/references/urma_sample.md)
- [openEuler UMDK source repository](https://atomgit.com/openeuler/umdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code changes, shell commands, build configuration updates, and verification checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces migrated files under an urma_output/ directory and preserves original source files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
