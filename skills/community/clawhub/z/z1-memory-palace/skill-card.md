## Description:

Long-term memory system for AI agents using a file-based palace architecture with BGE-M3 vector search, metadata filtering, compound scoring, GraphRAG Lite neighbor expansion, and memory metabolism protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create or upgrade file-based long-term memory for AI agents with vector search, recency and importance scoring, limited graph-neighbor expansion, cold archive handling, and reflection protocols.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can index broad local memory files if the manifest or root path is too permissive.

Mitigation: Run it only in a dedicated, low-privilege workspace and validate manifest paths against the intended memory directory before building an index.

Risk: Python dependency and embedding model revisions are not pinned in the artifact.

Mitigation: Pin the FlagEmbedding package and BAAI/bge-m3 model revision before deployment, then rebuild the index in a controlled environment.

Risk: Recurring maintenance can repeatedly read and update local memory indexes without operator review.

Mitigation: Do not enable scheduled maintenance until file scope, generated index locations, and cold-zone exclusion behavior are reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/z1one0415/skills/z1-memory-palace)
- [Memory Metabolism Protocol](references/memory_metabolism.md)
- [GraphRAG Lite Protocol](references/graphrag_lite.md)
- [Query Memory Palace Protocol](references/query_protocol.md)
- [Read Drawer File Tool Spec](references/read_drawer_file.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python scripts, JSONL manifest examples, and operational protocols]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Query output is designed to return top-ranked JSON records and optional score details from a local memory index.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
