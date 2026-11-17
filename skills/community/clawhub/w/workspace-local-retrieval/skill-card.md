## Description:

Builds a local-first workspace retrieval architecture for OpenClaw with explicit corpus boundaries, deny-by-default agent access, separate personal-memory and workspace-knowledge layers, stable search interfaces, and maintenance-aware refresh workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ys-c-23](https://clawhub.ai/user/ys-c-23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and bootstrap safer local retrieval for OpenClaw workspaces. It helps separate personal memory from reusable workspace knowledge, define allowlisted corpora, scope agent access, and plan refresh and smoke-test workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or running the npm entrypoint from an untrusted source could execute local bootstrap logic unexpectedly.

Mitigation: Use a pinned npm version or trusted package source, run the check command first, and review the generated files before continuing.

Risk: Poor corpus boundaries can cause private notes, credentials, logs, generated indexes, or unrelated workspace data to enter retrieval.

Mitigation: Review allowlists and exclusion rules before refresh or embedding workflows, keep personal memory separate, and use deny-by-default agent corpus access.

Risk: Indexing or embedding workflows may be unreliable when required prerequisites are missing.

Mitigation: Run the prerequisite check and stop until required Python, Node.js, and SQLite capabilities pass for the target platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ys-c-23/skills/workspace-local-retrieval)
- [Privacy and Boundaries](references/privacy-and-boundaries.md)
- [Agent Scoping](references/agent-scoping.md)
- [Interface Contract](references/interface-contract.md)
- [Dependencies and Platforms](references/dependencies-and-platforms.md)
- [Preflight and Install Policy](references/preflight-and-install-policy.md)
- [Maintenance Patterns](references/maintenance-patterns.md)
- [Runtime Layout](references/runtime-layout.md)
- [Sanitized Demo](references/sanitized-demo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local retrieval/config templates through the CLI; users should review allowlists and pass prerequisite checks before indexing.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
