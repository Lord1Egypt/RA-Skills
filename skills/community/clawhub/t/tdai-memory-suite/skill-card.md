## Description:

Complete local memory system for OpenClaw agents with a four-layer memory pipeline, local vector search, ontology knowledge graph, and Nomic Atlas visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent local conversation memory, semantic recall, structured ontology records, and memory visualization to agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic OpenClaw runtime or configuration changes can grant conversation access with limited user control.

Mitigation: Review the proposed patching and prefer a manually approved configuration before installation.

Risk: Conversation-memory surfaces and optional remote storage/offload can expose sensitive conversation data or host identifiers.

Mitigation: Keep the gateway bound to loopback with authentication or network isolation, and enable remote services only after accepting the data-sharing implications.

Risk: Installer paths that resolve latest dependencies can change behavior across installs.

Mitigation: Avoid unpinned @latest installer paths and review the exact version being installed.

## Reference(s):

- [TDaí Memory Suite on ClawHub](https://clawhub.ai/paudyyin/skills/tdai-memory-suite)
- [paudyyin ClawHub profile](https://clawhub.ai/user/paudyyin)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [sqlite-vec](https://github.com/asg017/sqlite-vec)
- [node-llama-cpp](https://github.com/withcatai/node-llama-cpp)
- [Ontology schema reference](components/tdai-ontology/references/schema.md)
- [Ontology query reference](components/tdai-ontology/references/queries.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell snippets; runtime memory context is text or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local memory records, persona summaries, ontology JSONL, and HTML visualization files during use.]

## Skill Version(s):

1.0.0 (source: server release evidence, frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
