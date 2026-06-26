## Description: <br>
Long-term memory system for AI agents using a file-based palace architecture with BGE-M3 vector search, metadata filtering, compound scoring, GraphRAG Lite neighbor expansion, and memory metabolism protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create or upgrade file-based long-term memory for AI agents with vector search, metadata filtering, temporal weighting, graph-neighbor expansion, and structured memory consolidation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and queries a persistent local memory index, which can expose unintended local content if the manifest scope is too broad. <br>
Mitigation: Keep the manifest limited to the intended memory directory and exclude secrets, credentials, and unrelated workspace files. <br>
Risk: Background maintenance can run local indexing scripts automatically. <br>
Mitigation: Review any scheduled maintenance setup before enabling it, and confirm the commands and paths match the intended environment. <br>
Risk: The artifact scripts include local absolute paths that may not match a new user's filesystem. <br>
Mitigation: Adapt and review paths before execution so indexing and query operations target only the intended local memory palace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/z1one0415/z1-memory-palace) <br>
- [GraphRAG Lite Protocol V1](references/graphrag_lite.md) <br>
- [Z1 Memory Metabolism Protocol V1](references/memory_metabolism.md) <br>
- [Query Memory Palace Protocol V1](references/query_protocol.md) <br>
- [read_drawer_file Tool Spec V1](references/read_drawer_file.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-line query/index records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files and local vector index artifacts; query output is limited to top matches plus up to two graph neighbors per core result.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
